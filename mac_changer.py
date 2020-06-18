#! /usr/bin/env python

import subprocess
import argparse
import re

def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--interface",dest="interface",help="Specifies the interface to be modified")
    parser.add_argument("-m","--mac",dest="new_mac",help="Specifies the new mac for the selected interface")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[!] You haven't specified the interface!")
    elif not options.new_mac:
        parser.error("[!] You haven't specified the new mac address")
    return options

def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface,"down"])
    subprocess.call(["ifconfig", interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig", interface,"up"])

def check_current_mac(interface):
    result = subprocess.check_output(["ifconfig",interface])
    current_mac = re.search(r"\ww:\ww:\ww:\ww:\ww:\ww",result)
    if current_mac:
        return current_mac
    else:
        print("[-!-] "+interface+" has no mac address specified or please check the name of the interface")
    
options = get_input()
current_mac = check_current_mac(options.interface)
print("[*] Changing MAC from "+ current_mac+" to "+ options.new_mac)
change_mac(options.interface,options.new_mac)
current_mac = check_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Successfully Changed MAC from "+ current_mac+" to "+ options.new_mac)
else:
    print("[!] Operation Failed, Please try again with different MAC address")