import re
from netmiko import ConnectHandler


def parse_src_to_dest_jitter(string):
    """
    Parses the output of the 'show ip sla statistics' command and returns a dict cointaiing the min, avg, max jitter
    values

    :param string:
    :return:
    """
    PATTERN_SRC_TO_DEST_JITTER = re.compile('Source to.*Jitter.Min/Avg/Max:.(\d{1,9}\/\d{1,9}\/\d{1,9})')

    match = PATTERN_SRC_TO_DEST_JITTER.findall(string)
    data = match.pop()
    data_list = data.split('/')
    jitter_min = data_list[0]
    jitter_avg = data_list[1]
    jitter_max = data_list[2]

    data = {
        'jitter_min': int(jitter_min),
        'jitter_avg': int(jitter_avg),
        'jitter_max': int(jitter_max)
    }


def parse_cef_next_hop(string):
    """
    Parses the 'show ip cef {{ next_hop }}' output and returns a dict of the nexthop and outgoing interface

    :param string:
    :return:
    """
    PATTERN_CEF_NEXT_HOP = re.compile('nexthop\W(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\W(.*Ethernet\d)')

    results = PATTERN_CEF_NEXT_HOP.search(string)

    matched_data = results.groups()
    return {
        'next_hop': matched_data[0],
        'link': matched_data[1],
    }


def get_ip_sla_jitter(mgmt_ip):
    connect_data = {
        'device_type': 'cisco_ios',
        'host': f'{mgmt_ip}',
        'username': 'cisco',
        'password': 'cisco',
    }

    handler = ConnectHandler(**connect_data)

    ip_sla_statics_output = handler.send_command("show ip sla statistics")

    return ip_sla_statics_output


def main():
    output = get_ip_sla_jitter('10.99.7.0')
    print(output)

if __name__ == "__main__":
    main()
