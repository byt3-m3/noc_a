from ncclient import manager


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
          <ENTITY-MIB xmlns="urn:ietf:params:xml:ns:yang:smiv2:ENTITY-MIB"/>
        </filter>
        """
        print(m.get(hostname_filter).data_xml)


if __name__ == "__main__":
    main()
