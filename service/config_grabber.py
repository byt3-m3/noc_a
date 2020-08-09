from netmiko import ConnectHandler
import json

with open('hosts.json', 'r') as hosts_file:
    print("Opening hosts.json")
    data = json.load(hosts_file)
    hosts = data.get('lab_hosts')

    for host in hosts:

        connect_data = {
            'device_type': 'cisco_ios',
            'host': f'{host}',
            'username': 'cisco',
            'password': 'cisco',
        }

        handler = ConnectHandler(**connect_data)
        print(f"Getting {host} Config")
        config = handler.send_command("show run")
        with open(f'../backups/{host}_bkup.txt', 'w') as config_file:
            print(f"Saving Config to: ../backups/{host}_bkup.txt")
            config_file.write(config)