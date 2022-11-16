#import datetime
from datetime import datetime
import email
import imaplib
import mailbox

import time
import paramiko
from subprocess  import STDOUT
import os
import glob



EMAIL_ACCOUNT = "koteswararao.nayudu@edgeq.io"
PASSWORD = "n2ycvLJe@123"

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL_ACCOUNT, PASSWORD)
mail.list()
mail.select('inbox')

#since1 = datetime.strftime('%d-%b-%Y %H:%M:%S')
#print(since1)

now = datetime.now()
date_time = now.strftime("%d-%b-%Y")
#date_time="28-Oct-2022"
#date_time="27-Oct-2022"
print("date and time:",date_time)
#dateandtime="(" + "'" +  "SINCE" + " " +  date_time + "'"  + ")"
dateandtime="SINCE" + " " +  date_time
print(dateandtime)


subject1="EDGEQ MAINLINE E2E SOFTWARE JENKINS"
sender_name="ci.admin@edgeq.io"
#sender_name="koteswararao.nayudu@edgeq.io"

search_list = []
#search_list += ['UNSEEN']
search_list += ['ALL']
search_list += ['FROM', '"%s"' % sender_name]
search_list += ['SUBJECT', '"%s"' % subject1]

string="'(SINCE 27-Sep-2022)' , '(SUBJECT \"EDGEQ GNB PLATFORM JENKINS\")'"
#result, data = mail.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
#result, data = mail.uid('search',  '(SINCE 27-Sep-2022)' , '(SUBJECT "EDGEQ GNB PLATFORM JENKINS")')
#result, data = mail.uid('search',  dateandtime , '(SUBJECT "EDGEQ GNB PLATFORM JENKINS"), UNSEEN')
#result, data = mail.uid('search', *search_list1 ,  *search_list)
result, data = mail.uid('search',  dateandtime , *search_list)
i = len(data[0].split())

print(i)

for x in range(i):
	latest_email_uid = data[0].split()[x]
	print(latest_email_uid)
	result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
	# result, email_data = conn.store(num,'-FLAGS','\\Seen')
	# this might work to set flag to seen, if it doesn't already
	raw_email = email_data[0][1]
	raw_email_string = raw_email.decode('utf-8')
	email_message = email.message_from_string(raw_email_string)

	# Header Details
	date_tuple = email.utils.parsedate_tz(email_message['Date'])
	if date_tuple:
		local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
		local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
	email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
	email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
	subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
	print(subject)
	
	# Body details
	for part in email_message.walk():
		print("email part")
		#if part.get_content_type() == "text/plain":
		if part.get_content_type() == 'application/msword':
			#body = part.get_payload(decode=True)
			name = part.get_param('name')
			f = open(name, 'wb')
			f.write(part.get_payload(None, True))
			f.close()
		else:
			continue


print(subject)

if subject.find("SUCCESS") != -1 :
	print("subject line matches Success string")
	host = "192.168.3.110"
	username = "equser"
	password = "Password$2021"
	client = paramiko.client.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(host, username=username, password=password)
	build_date = now.strftime("%d%m%y")
	print(build_date)
	subject_split_lst = subject.split()
	build_number = subject_split_lst[6]
	print(build_number)
	command_ssh="/usr/bin/sh /home/equser/lava_master_uramdisk_img.sh" + " " +  build_number 
	print(command_ssh)
	_stdin, _stdout, _stderr = client.exec_command( str(command_ssh) ) 
	ssh_job_id = _stdout.read().decode()
	print(ssh_job_id)
else:
	print("FAIL to match the Success string in subject line")
