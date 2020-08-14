import re
import time
import logging

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


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
    return data


def parse_jitter_threshold(string):
    """
    Parses the output of the 'show ip sla statistics' command and returns a dict cointaiing the min, avg, max jitter
    values

    :param string:
    :return:
    """
    PATTERN_SRC_TO_DEST_JITTER = re.compile('Over Threshold:\n.*: (\d*).*\((\d*)')

    match = PATTERN_SRC_TO_DEST_JITTER.findall(string)
    data = match.pop()

    rtt = data[0]
    over_threshold = data[1]

    data = {
        'over_threshold': int(over_threshold),
        'rtt': int(rtt),

    }
    return data


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


def get_ip_sla_stats(mgmt_ip):
    connect_data = {
        'device_type': 'cisco_ios',
        'host': f'{mgmt_ip}',
        'username': 'cisco',
        'password': 'cisco',
    }

    handler = ConnectHandler(**connect_data)
    try:
        sla_stats = handler.send_command("show ip sla statistics")
        jitter_data = parse_jitter_threshold(sla_stats)

        cef_output = handler.send_command(f"show ip cef vrf MGMT 10.99.0.254")
        cef_data = parse_cef_next_hop(cef_output)

        if jitter_data.get('rtt') > 20:
            logger.error(
                f'Host: {mgmt_ip} having issues on uplink: "{cef_data.get("link")}" Over threshold: {jitter_data.get("over_threshold")}%')

        handler.disconnect()
        return sla_stats, cef_data

    except NetmikoTimeoutException:
        pass


def get_ip_cef_nexthop(mgmt_ip, next_hop):
    connect_data = {
        'device_type': 'cisco_ios',
        'host': f'{mgmt_ip}',
        'username': 'cisco',
        'password': 'cisco',
    }

    handler = ConnectHandler(**connect_data)
    try:
        output = handler.send_command(f"show ip cef vrf MGMT {next_hop}")
        handler.disconnect()
        return output
    except NetmikoTimeoutException:
        pass


def main():
    hosts = ['10.99.7.0', '10.99.8.0', '10.99.9.0', '10.99.10.0']
    while True:

        for host in hosts:
            time.sleep(.5)
            logger.info(f"Connecting to Host: {host}")

            output = get_ip_sla_stats(host)
            logger.info(output)


if __name__ == "__main__":
    main()
    # with open('dev_files/show_ip_sla_stat_output.txt', 'r') as f:
    #     buffer = f.read()
    #     res = parse_jitter_threshold(buffer)
    #     print(res)
