from ncclient import manager


def main():
    with manager.connect_ssh("10.99.7.0", username="cisco", password='cisco') as m:
        sla_schema = m.get_schema('oc-acl-cisco')
        print(sla_schema)


if __name__ == "__main__":
    main()
