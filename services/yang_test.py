from ncclient import manager

def main():
    with manager.connect_ssh("10.99.7.0", username="cisco", password='cisco') as m:
        print(m.server_capabilities)


if __name__ == "__main__":
    main()
