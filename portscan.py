import threading
import socket
from optparse import OptionParser

class ip():

	def __init__(self):
		self.initialize_variable()

		self.multithread('portscan',self.ipaddr,self.portrange)

		if open_ports:
			print("\n[+] %s Open Ports found!" % len(open_ports))
			print("[+] Do you want to banner grab?")
			bg = 'y'#raw_input("Enter y or n : ")
			if bg.lower() == 'y':
				self.multithread('bannergrab',self.ipaddr,open_ports)
			else: pass
		
	def initialize_variable(self):
		# This function is for initializing the necessary command arguments and automate default values when one is empty
		# For target argument, the default value is 'Localhost' ('127.0.0.1')
		# As for port range, I think it's just necessary to scan from port 20 to 1024
		
		# Generate a list and assign it to self.portrange
		global open_ports
		open_ports = []
		# to record the open ports for the purpose of banner grabbing

		if option.target:
			self.ipaddr = option.target
		elif not option.target:
			print("\n[!] --target argument is not supplied, default value (localhost) is taken\n")
			self.ipaddr = '127.0.0.1'

		if option.portrange:
			if option.portrange != 'a':
				self.highrange = int(option.portrange.split('-')[1])
				self.lowrange = int(option.portrange.split('-')[0])
				self.portrange = [i for i in range(self.lowrange,(self.highrange+1))]
			elif option.portrange == 'a':
				self.portrange = [i for i in range(1,5000)]

		elif not option.portrange:
			print("\n[!] --portrange argument is not supplied, default value (20-1024) is taken\n")
			self.highrange = 1024
			self.lowrange = 20
			self.portrange = [i for i in range(self.lowrange,self.highrange)]

		

	def scan(self,ipaddr,port):
		# Accepts ipaddress parameter, and port to scan is accepted as port(type=int)
		# Only prints when the port is OPEN
		# Or set your own error message to display with "else" code block

		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		status = s.connect_ex((ipaddr,port))
		if (status == 0):
			print "[+] ~[%s]~ Port Open" % port
			open_ports.append(port)
		else:
			# print("[+] Port Closed")
			pass

	def multithread(self,operation,ipaddr,ports):
		if operation == 'portscan':
			# Handles port scanning operation with multi-threading
			# If operation is portscanning, then ports argument is (List)
			threads = []
			for i in ports:
				t = threading.Thread(target=self.scan,args=(ipaddr,i,))
				threads.append(t)
				t.start()

		elif operation == 'bannergrab':
			# Handles bannergrabbing operation, since trying one after one is not beneficial
			# because some ports just do not return anything, and we can't just wait forever
			# to print the response.

			threads = []
			for i in ports:
				t = threading.Thread(target=self.bannergrab,args=(ipaddr,i))
				threads.append(t)
				t.start()

	def bannergrab(self,ipaddr,port):
		# ipaddr variable = STR
		# port variable = INT
		try:
			s = socket.socket()
			s.connect((ipaddr,port))
			s.send('hello')
			response = s.recv(64)
			if response:
				print("[Banner Information PORT=%s ]\n%s" % (port,response))
			else:
				print("[!] Cannot Grab Banner Information PORT=%s" % (port))
		except:
			print("[!] Cannot Grab Banner Information PORT=%s" % (port))

def parseArgs():

	parser = OptionParser()

	parser.add_option("-t","--target",dest="target",
	help="IP Address to scan within quote",metavar='"127.0.0.1"')
	
	parser.add_option("-p","--port range",dest="portrange",
	help="Port Range to scan separated with - or 'a' for all ports",metavar="20-1024")

	return parser

def main():
	global option

	parser = parseArgs()
	(option, args) = parser.parse_args()
	# Just assign the class function to do the rest
	app = ip()

if __name__ == '__main__':
	main()
