from ncclient import manager


def main():
    with manager.connect_ssh("10.99.7.0", username="cisco", password='cisco') as m:
        # for i in m.server_capabilities:
        #     print(i)
        sla_schema = m.get_schema('ietf-interfaces')
        print(sla_schema)
        print(m.get("""
        <filter>
            <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>{{INTF_NAME}}</name>
      <config>
      </config>
      <subinterfaces/>
    </interface>
</interfaces>
        </filter>
        """))


if __name__ == "__main__":
    main()
