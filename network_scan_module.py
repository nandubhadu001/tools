import scapy.all as scap
import optparse
def my_help():
	print("-t specify target ip or network range")
	print("scan(ip) returns scap.srp(arp_request_packet,timeout=1,verbose=False)[0]=answered packets")
	print("get_claint_dict() returns claint_dict{\"index\":i,\"ip\":claint[0].pdst,\"mac\":claint[1].src}")
def get_args():
	parser = optparse.OptionParser()
	parser.add_option("-t","--target",dest="target",help="specify target ip or network range")
	options = parser.parse_args()[0]
	target = options.target
	return target
def scan(ip,timeout=1):
	arp_request = scap.ARP(pdst=ip)
	broadcast = scap.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_packet = broadcast/arp_request
	ans = scap.srp(arp_request_packet,timeout=timeout,verbose=False)[0]
	return ans
def get_claint_dict(ans):
	i = 1
	claint_dict = []
	for claint in ans:
		claint_dict.append({"index":i,"ip":claint[0].pdst,"mac":claint[1].src})
		i +=1
	return claint_dict
def print_all(claint_dict):
	print("index\t\tTarget_IP\t\t\tTarget_Mac")
	for claint in claint_dict:
		print(str(claint["index"])+"\t\t"+claint["ip"]+"\t\t\t"+claint["mac"])
#print_all(get_claint_dict(scan(get_args())))
