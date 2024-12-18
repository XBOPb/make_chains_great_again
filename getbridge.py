import requests
import subprocess

config_template = 'config.txt'
torrc_config = '/etc/tor/torrc'
torrc_backup = '/etc/tor/torrc_backup'


def request_bridges():
    bridges = []
    params = {
        'transport': 'obfs4',
    }
    response = requests.get('https://bridges.torproject.org/bridges', params=params)
    text = response.text
    for line in text.split('\n'):
        if line.strip().startswith('obfs4'):
            bridges.append(line.strip().replace(' <br/>', ''))
    return bridges


def read_template():
    with open(config_template) as file:
        config_text = file.read()
    return config_text
    
    
def form_config_text(config_template, bridges):
    config_text = config_template.replace('bridge_1', bridges[0]).replace('bridge_2', bridges[1])
    return config_text
    
    
def modify_tor_config(config_text):
    subprocess.getoutput(f'echo "{config_text}" >> {torrc_config}')


def backup_existing_config():
    subprocess.getoutput(f'cp {torrc_config} {torrc_backup}')


if __name__=='__main__':
    config_template = read_template()
    bridges = request_bridges()
    config_text = form_config_text(config_template, bridges)
    backup_existing_config()
    modify_tor_config(config_text)
