#!/usr/bin/env python3

import datetime
#import os
import subprocess
import re
from time import gmtime, strftime


sessione_str = ""
sessione = input("    sessione - premere 1 per entrata, 2 per uscita :")
if sessione == "1":
	sessione_str = "Entrata"
elif sessione == "2":
	sessione_str = "Uscita"
else:
	sessione_str = sessione

i = 0

while 1:
	input_var = input("    Magnetic Card:")
	error = "";
	t_string = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	row = str(i)+","+t_string+","+input_var+"\n"
	file = open('magneticCardLog.txt','a')
	file.write(row)
	file.close()

	p = re.compile(r'%([a-z]{6}[0-9]{2}[a-z]{1}[0-9]{2}\w{5})([\w\s]+)\?', re.IGNORECASE)
	m = p.match(input_var)
	#print(m)
	if m is not None:
		#      session    id              time           cf               nome             raw
		row2 = '"%s","%s","%s","%s","%s","%s"' % (sessione_str,str(i),t_string,m.group(1),m.group(2),input_var)
		#row2 = '"'+str(i)+'","'+t_string+'","'+m.group(1)+'","'+m.group(2)+'","'+input_var+'"'+"\n"
		file = open('magneticCardData.csv','a')
		file.write(row2+"\n")
		file.close()
		print (row2)
		p = subprocess.Popen('play ./audios/beep.mp3', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	else:
		p2 = re.compile(r'%(\d+)([\w]+).?([\w]+)', re.IGNORECASE)
		m2 = p2.match(input_var)
		if m2 is not None:
			#         id          time  cf               nome                 raw
			row3 = '"%s","%s","%s","","%s %s","%s"' % (sessione_str,str(i),t_string,m2.group(2),m2.group(3),input_var)
			#row3 = str(i)+","+t_string+",,"+m2.group(2)+" "+m2.group(3)+","+input_var+"\n"
			file = open('magneticCardData.csv','a')
			file.write(row3+"\n")
			file.close()
			print (row3)
			p = subprocess.Popen('play ./audios/beep.mp3', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		else:
			print('Tessera non riconosciuta')
			row4 = '"%s","%s","%s","","","%s"' % (sessione_str,str(i),t_string,input_var)
			#row4 = str(i)+","+t_string+",,,"+input_var+"\n"
			file = open('magneticCardData.csv','a')
			file.write(row4+"\n")
			file.close()
			print (row4)
			p = subprocess.Popen('play ./audios/inquisitiveness.mp3', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	i += 1
