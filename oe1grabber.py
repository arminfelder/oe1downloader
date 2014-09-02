#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 Armin Felder <armin.felder@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import json
from subprocess import call
from pprint import pprint
import urllib2
import time
import pycurl
import csv
import datetime
import unicodedata
import sys
import getopt


#config
programms_csv_path = "programme.csv"
mp3_dir = "" #use a trailing slash
bibtech_file = "bibliographie.bib"
logfile = "log.txt"


#Program
date = datetime.date.fromordinal(datetime.date.today().toordinal()-1).strftime("%Y%m%d")

oe1_json_url= 'http://oe1.orf.at/programm/konsole/tag/'+date



c = pycurl.Curl()
programms = list()
fp_bib = open(bibtech_file,'a+')

with open(programms_csv_path, 'rb') as csvfile:
	programms_csv = csv.reader(csvfile, delimiter='\"', quotechar=';')
	for csv_row in programms_csv:
		programms.append(csv_row[0].decode('utf-8'))

for i in range(0, 10):
	try :
		urlresponse = urllib2.urlopen(oe1_json_url)
		break
	except:  
		print('can not fetch url: '+oe1_json_url +'\n waiting 30s to try again')
		sleept(30)
		if(i==10):
			writelog('failed to download: '+oe1_json_url)
			sys.exit()
	

data = json.loads(urlresponse.read())


for uri in data['list']:
	if uri['short_title'] in programms:
		time.strptime(uri['day_label']+' '+uri['time'],"%d.%m.%Y %H:%M")
		filename = time.strftime("%Y%m%d%H%M")+"_"+uri['short_title']+"_"+uri['id']
		
		fp = open(mp3_dir+filename+'.mp3','wp')
		
		c.setopt(pycurl.URL, uri['url_stream'])
		c.setopt(pycurl.CONNECTTIMEOUT,1800)
		c.setopt(pycurl.TIMEOUT,1800)
		c.setopt(pycurl.WRITEDATA, fp)
		c.perform()
		fp.close()
		print(uri['info'])
		bibentry = u'@HOERFUNK{\n'+filename+','+'title = {'+uri['title']+'}'+',\n'+'abstract = {'+uri['info']+'}'+',\n'+'url = {http://oe1.orf.at/programm/'+uri['id']+'}'+',\n'+'year = {'+time.strftime("%Y")+'}'+',\n'+'month = {'+time.strftime("%m")+'}'+',\n'+'note = {OE1},\n'+'series = {'+uri['short_title']+'}'+',\n'+'keywords = {Datenschutz, EU},\nowner = {gugu},\n'+'timestamp = {'+time.strftime("%Y.%m.%d %H:%M")+'}'+'}\n\n';
		fp_bib.write(bibentry.encode('utf8'))

fp_bib.close()

def writelog(newline):
	logp = open(logfile,'wp')
	logp.write('['+strftime("%Y%m%d %H:%M")+']: '+newline)
	logp.close()
