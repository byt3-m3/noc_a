from ncclient import manager


def main():
    with manager.connect_ssh("10.99.7.0", username="cisco", password='cisco') as m:
        for i in m.server_capabilities:
            print(i)

        sla_schema = m.get_schema(
            'urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSLA-JITTER-MIB?module=CISCO-IPSLA-JITTER-MIB&revision=2007-07-24')
        print(sla_schema)


if __name__ == "__main__":
    main()
