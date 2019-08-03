#sudo useradd -m kali
#xhost +
#sudo -u kali chromium
import subprocess
import optparse
import re
import random
def my_help():
	print("-i(--interface) for interface 'wlan0','eth0'")
	print("-m(--mac) new mac adress not needed if -r is specified")
	print("-r(--random) use a random mac 00:xx:xx:xx:xx:xx")
	print("call _modual_.mac_change(_modual_.get_args())")
def get_args():
	parser = optparse.OptionParser()
	parser.add_option("-i","--interface",dest="interface",help="please enter interface")
	parser.add_option("-m","--mac",dest="new_mac",help="provide a mac adress or use -r for random mac")
	parser.add_option("-r","--random",action="store_true",dest="random",help="generate random mac adress")
	options,args = parser.parse_args()
	return options
def crrunt_mac(interface):
	ifconfig_interface = subprocess.check_output(["ifconfig",interface])
	crrunt_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_interface)
	return crrunt_mac.group(0)
def mac_change(options):
	interface = options.interface
	random = options.random
	if random:
		new_mac = random_()
	if not random:
		new_mac = options.new_mac
	print("[+] crrunt mac adress for {} is {}".format(interface,str(crrunt_mac(interface))))
	print("[+] Changing mac adress for {} from {} to {}".format(interface,str(crrunt_mac(interface)),new_mac))
	subprocess.call(["ifconfig",interface,"down"])
	subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
	subprocess.call(["ifconfig",interface,"up"])
	print("[+] crrunt mac adress for {} is {}".format(interface,str(crrunt_mac(interface))))
def random_():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        00,
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )
#mac_change(get_args())
#print(crrunt_mac("wlan0"))