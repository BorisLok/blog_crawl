import io

import yaml

if __name__ == '__main__':
    with open('config.yml', 'r') as stream:
        data = yaml.safe_load(stream=stream)
        print(data)