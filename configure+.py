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
import os

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

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

username, password = get_credentials()

#os.system('ls -la *.conf')
os.system('find *.conf')
os.system('echo')
os.system('echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"')
commandfile = raw_input("Please select what command you want to run: \n")

#os.system('ls -la *.json')
os.system('find *.json')
os.system('echo')
os.system('echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"')
devicegroup = raw_input("Please select what device-group you want to apply to: \n")


with open(commandfile) as config_file:
    commands = config_file.readlines()

with open(devicegroup) as dev_file:
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

