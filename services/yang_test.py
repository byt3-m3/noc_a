from ncclient import manager
from xml.etree import ElementTree as et


def main():
    with manager.connect_ssh("10.99.7.0", username="cisco", password='cisco') as m:
        # for i in m.server_capabilities:
        #     print(i)
        # sla_schema = m.get_schema('ENTITY-MIB')
        # print(sla_schema)
        hostname_filter = '''
                              <filter>
                                  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                  </native>
                              </filter>
                              '''

        ENTITY_FILTER = """
        <filter>
          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                    <interface/>
                    </native>
        </filter>
        """
        results = m.get(ENTITY_FILTER).data_xml
        # print(results)
        xml_doc = et.fromstring(results)
        root = xml_doc[0]
        for el in root:
            print(el.tag, el.text)

if __name__ == "__main__":
    main()
