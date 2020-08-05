import requests
import json
import os


class LCGClient:

    def __init__(self, host='ec2-18-223-106-170.us-east-2.compute.amazonaws.com', port=8080):
        self._host = host
        self._port = str(port)
        self._endpoint = '/api/v1/lcg/config/base'

        self._url = f'http://{self._host}:{self._port}{self._endpoint}'

    def gen_base_config(self, data):
        resp = requests.post(
            url=f'{self._url}?template_type=ios_base_node',
            headers={'Content-Type': "application/json"},
            data=json.dumps(data)
        )
        return resp.text


CONFIG_DIR = os.getenv('CONFIG_DIR', '../configs')


def get_filenames():
    dirpath = os.walk(CONFIG_DIR)
    filenames = list(dirpath)[0][2]
    return filenames


client = LCGClient()

for filename in get_filenames():
    with open(f'{CONFIG_DIR}/{filename}', 'r') as f:
        data = json.loads(f.read())

        config = client.gen_base_config(data)
        with open(f'../output/{filename.replace(".json", ".cfg")}', 'w') as fw:
            fw.write(config)
        print(config)
