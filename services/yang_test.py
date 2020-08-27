from ncclient import manager
from xml.etree import ElementTree as et
import xmltodict
from pprint import pprint
import json


def get_ncmanager(host, uname, pword, hostkey_verify) -> manager.Manager:
    try:
        return manager.connect_ssh(host=host, username=uname, password=pword, hostkey_verify=hostkey_verify)

    except Exception:
        raise


def list_server_capabilities(manager_: manager.Manager):
    return list(manager_.server_capabilities)


def get_ios_native(manager_: manager.Manager):
    FILTER = '''
            <filter>
                <native xmlns='http://cisco.com/ns/yang/Cisco-IOS-XE-native'>

                </native>
            </filter>
            '''

    response = manager_.get(FILTER)
    if len(response.data) == 1:
        return xmltodict.parse(response.data_xml)['data']['native']


def get_snmp(manager_: manager.Manager):
    FILTER = '''
                <filter>
                    <top xmlns='http://cisco.com/ns/yang/cisco-xe-openconfig-system-ext'>
                    
                    </top>
                </filter>
                '''

    response = manager_.get(FILTER)
    print(response)
    if len(response.data) == 1:
        return xmltodict.parse(response.data_xml)['data']['native']


def get_interfaces(manager_: manager.Manager):
    """
    Vendor Neutral Query of list of current interfaces

    :param manager_:
    :return:
    """
    FILTER = '''
                    <filter>
                        <interfaces-state xmlns='urn:ietf:params:xml:ns:yang:ietf-interfaces'>
                            <interface>
                                <name />
                            </interface>
                            
                        </interfaces-state>
                    </filter>
                    '''

    response = manager_.get(FILTER)

    if len(response.data) == 1:
        xml_to_dict = xmltodict.parse(response.data_xml)['data']['interfaces-state']['interface']

        return [i['name'] for i in xml_to_dict if 'Control Plane' not in i['name']]


def get_global_rt_table(manager_: manager.Manager):
    FILTER = '''
                        <filter>
                            <routing-state xmlns='urn:ietf:params:xml:ns:yang:ietf-routing'>
                          
                            </routing-state>
                        </filter>
                        '''

    response = manager_.get(FILTER)

    if len(response.data) == 1:
        xml_to_dict = xmltodict.parse(response.data_xml)['data']['routing-state']['routing-instance']

        return json.loads(json.dumps(xml_to_dict[0]['ribs']))


def is_present(data, key):
    if key in data.keys():
        return True
    else:
        return False


def list_keys(data):
    return [el for el in data.keys()]


def main():
    with manager.connect_ssh("192.168.1.160", username="cisco", password='cisco', hostkey_verify=False) as m:
        # for i in m.server_capabilities:
        #     if 'ietf' in i:
        #
        #         print(i)
        sla_schema = m.get_schema('Cisco-IOS-XE-arp')
        # print(sla_schema)
        hostname_filter = '''
                              <filter>
                                  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                  </native>
                              </filter>
                              '''

        XE_NATIVE_FILTER = """
        <filter>
            <top xmlns='ENTITY-MIB''>
                
            </top>
        </filter>
        """
        INTERFACES_FILTER = '''
        <filter>
            <native xmlns='http://cisco.com/ns/yang/Cisco-IOS-XE-native'>
              
            </native>
        </filter>
        '''

        results = m.get(INTERFACES_FILTER)
        print(len(results.data))
        if len(results.data) == 1:
            root = results.data[0]
            xml_to_dict = xmltodict.parse(results.data_xml)

            pprint(xml_to_dict['data']['native'].keys())


def dev():
    m = get_ncmanager(host="192.168.1.160", uname="cisco", pword='cisco', hostkey_verify=False)
    interfaces = get_interfaces(m)
    print(interfaces)
    rib = get_global_rt_table(m)
    pprint(rib)
    m.close_session()

    # pprint(default_table)
    # for k, v in default_table.items():
    #     # pprint(type(route))
    #     pprint(v)


if __name__ == "__main__":
    dev()
