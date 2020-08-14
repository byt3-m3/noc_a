from ncclient import manager


def main():
    with manager.connect_ssh("10.99.7.0", username="cisco", password='cisco') as m:
        # for i in m.server_capabilities:
        #     print(i)
        # sla_schema = m.get_schema('ietf-interfaces')
        # print(sla_schema)
        print(m.get("""
        <filter>
            <top xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interfaces>
                    <interface>
                        <name>GigabitEthernet1</name>
                    </interface>
                </interfaces>
            </top>
        </filter>
        """))


if __name__ == "__main__":
    main()
