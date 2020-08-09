import requests
import json
import os


class LCGClient:

    def __init__(self, host='ec2-18-223-106-170.us-east-2.compute.amazonaws.com', port=8080,
                 template_type='ios_base_node'):
        self._host = host
        self._port = str(port)
        self._endpoint = '/api/v1/lcg/config/base'
        self._template_type = template_type

        self._url = ''

    def gen_base_config(self, data):
        self._endpoint = '/api/v1/lcg/config/ios/base'

        resp = requests.post(
            url=f'{self.url}?return_type=text',
            headers={'Content-Type': "application/json"},
            data=json.dumps(data)
        )
        return resp

    def gen_netplan(self, data):
        self._endpoint = '/api/v1/lcg/config/linux/netplan'

        resp = requests.post(
            url=f'{self.url}?return_type=text',
            headers={'Content-Type': "application/json"},
            data=json.dumps(data)
        )
        return resp

    @property
    def url(self):
        return f'http://{self._host}:{self._port}{self._endpoint}'


JSON_CONFIGS = os.getenv('JSON_CONFIGS', '../configs')


def get_filenames():
    dirpath = os.walk(JSON_CONFIGS)
    filenames = list(dirpath)[0][2]
    return filenames


lcg_client = LCGClient()


def gen_configs():
    for filename in get_filenames():
        with open(f'{JSON_CONFIGS}/{filename}', 'r') as f:
            data = json.loads(f.read())
            node_obj = type('Node', (object,), data)
            print(f'Generated Config for {node_obj.hostname}')
            config = lcg_client.gen_base_config(data)
            with open(f'../output/{filename.replace(".json", ".cfg")}', 'w') as fw:
                fw.write(config.content.decode())
            # print(config)


def gen_netplan():
    # lcg_client = LCGClient(host="127.0.0.1", port=5002, template_type='linux_netplan_base')

    with open('../configs/linux/netplan_netman.json', 'r') as file_h:
        data = json.load(file_h)
        # print(data)

        resp = lcg_client.gen_netplan(data)
        print(resp.content.decode())


gen_configs()
