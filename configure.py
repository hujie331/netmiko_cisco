#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

from getpass import getpass
import json
import netmiko
#from netmiko import ConnectHandler
#from netmiko.cisco import CiscoIosBase (device type: "cisco_ios", "cisco_xe")
#from netmiko.cisco import CiscoIosBase (device type: "cisco_xe")
import sys
import signal

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

def get_input(prompt=''):
    try:
        line = raw_input(prompt)
    except NameError:
        line = input(prompt)
    return line

def get_credentials():
    """Prompt for and return a username and password."""
    username = get_input('Username(Please input your adm credentials): ')
    password = getpass()
    return username, password

if len(sys.argv) < 3:
    print('Usage: conf.py commands.txt devices.json')
    exit()


netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

username, password = get_credentials()

with open(sys.argv[1]) as config_file:
    commands = config_file.readlines()

with open(sys.argv[2]) as dev_file:
    devices = json.load(dev_file)


for device in devices:
    device['username'] = username
    device['password'] = password
    try:
        print('~' * 80)
        print('Connecting to device:', device['ip'])
        connection = netmiko.ConnectHandler(**device)
        print(connection.send_config_set(commands))
        print('Saving configuration...')
        connection.send_command('write')
        """To keep 2 lines space between 2 devices"""
        print()
        print()
        connection.disconnect()
    except netmiko_exceptions as e:
        print('Failed to ', device['ip'], e)

