#!/usr/bin/env python
#Author: Geetika Gopi

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Target interface for MAC address change")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        #code to handle null value error
        parser.error("[-] please enter a value for interface to be changed, use --help for more info.")

    elif not options.new_mac:
        #code to handle null value error
        parser.error("[-] please enter a value for new MAC address, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    # SANITIZED CODE
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] Could not find a MAC address.")


#BELOW BLOCK OF CODE LACKS INPUT SANITIZATION
# subprocess.call("ifconfig " + interface + " down",shell=True)
# subprocess.call("ifconfig " + interface + " hw ether" + new_mac,shell=True)
# subprocess.call("ifconfig " + interface + " up",shell=True)

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))
change_mac(options.interface, options.new_mac)
changed_mac = get_current_mac(options.interface)

if changed_mac == options.new_mac:
    print("[+] MAC Address changed successfully to" + changed_mac)
else:
    print("[-] ERROR: MAC Address unchanged")
