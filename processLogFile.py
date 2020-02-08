import os
import sys
import time
import psutil
import urllib.request as urllib2
import smtplib
import schedule
from sys import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def is_connected():
	try:
		urllib2.urlopen('http://216.58.192.142',timeout=1)
		return True
	except urllin2.URLError as err:
		return False
def MailSender(filename, time):
	try:
		urllib2.urlopen('http://216.58.192.142',timeout=1)
		fromaddr = "senderMail@gmail.com"
		toaddr = "receiverMail@gmail.com"
	
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['to'] = sys.argv[1]

		body = """
		Hello %s, Please find attached document which contains log of Running process.
		Log file is created at :%s	
		
		This is auto generated mail
		Thanks & Regards,
		Akshay Pawar."""%(toaddr,time)

		Subject = """Akshay Pawar Process log generated at :%s"""%(time)

		msg['Subject'] = Subject

		msg.attach(MIMEText(body,'plain'))

		attachment = open(filename, "rb")
		p = MIMEBase('application','actet-stream')
		p.set_payload((attachment).read())
		encoders.encode_base64(p)
		p.add_header('Content-Disposition',"attachment;filename= %s" % filename)
	
		msg.attach(p)
		s = smtplib.SMTP('smtp.gmail.com',587)
		s.starttls()
		s.login(fromaddr,"senderMailPassword")
		text = msg.as_string()
		s.sendmail(fromaddr,toaddr,text)
		s.quit()
		print("log file successfully send thruogh mail...")
		
	except Exception as E:
		print("Unable to send mail",E)


def ProcessLog(log_dir = 'LogFile'):
	listprocess = []
	if not os.path.exists(log_dir):
		try:
			os.mkdir(log_dir)
		except:
			pass

	separator = "-" * 70
	log_path = os.path.join(log_dir,"AkshayPawar%s.log"%(time.ctime()))
	f = open(log_path,'w')
	f.write(separator + "\n")
	f.write("process logger: "+time.ctime() + "\n")
	f.write(separator + "\n")
	f.write("\n")

	for proc in psutil.process_iter():
		try:
			pinfo = proc.as_dict(attrs = ['pid','name','username'])
			vms = proc.memory_info().vms/(1024*1024)
			pinfo['vms'] = vms
			listprocess.append(pinfo)
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass

	for element in listprocess:
		f.write("%s\n"%element)

	print("Log file is successfuly generated at location %s"%(log_path))
	connected  = is_connected()

	if connected:
		starttime = time.time()
		MailSender(log_path, time.ctime())
		endtime = time.time()
		print("Took %s seconds to send mail"%(endtime-starttime))
	else:
		print("There is no Internet connection")
	

def main():
	print("Application name:"+argv[0])
	if(len(argv) != 2):
		print("Invalid number of argument...")
		exit()
	if(argv[1] == "-h") or (argv[1] == "-H"):
		print("This srcipt is used log record of running processess...")
		exit()
	if(argv[1] == "-u") or (argv[1] == "-U"):
		print("ApplicationName.py AbsolutePath_of_Directory")
		exit()

	try:
		ProcessLog()
		#schedule.every(int(argv[1])).minutes.do(ProcessLog)
		#while True:
		#	schedule.run_pending()
		#	time.sleep(1)
	except ValueError:
		print("Error : Invalid input",E)

if __name__=="__main__":
	main()
