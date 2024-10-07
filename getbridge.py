import requests
import subprocess

def request_bridges():
    bridges = []
    params = {
        'transport': 'obfs4',
    }
    response = requests.get('https://bridges.torproject.org/bridges', params=params)
    text = response.text
    for line in text.split('\n'):
        if line.strip().startswith('obfs4'):
            bridges.append(line)
    return bridges


def read_config():
    with open('config.txt') as file:
        config_text = file.read()
    return config_text
    
    
def form_config_text(config, bridges):
    config_text = config.replace('bridge_1', bridges[0]).replace('bridge_2', bridges[1])
    return config_text
    
    
def modify_tor_config(config_text):
    # subprocess.run('./edit_tor_config.sh')
    # subprocess.getoutput(f'chmod o+w /etc/tor/torrc')
    # subprocess.getoutput(f'{config_text} >> /etc/tor/torrc')
    # subprocess.getoutput(f'chmod o-w /etc/tor/torrc')
    

if __name__=='__main__':
    config = read_config()
    bridges = request_bridges()
    config_text = form_config_text(config, bridges)
    print(f'adding {config_text}')
    modify_tor_config(config_text)
