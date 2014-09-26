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
import urllib.request
import time
import pycurl
import csv
from datetime import datetime 
import sys

class oe1grabber():
        
    def __init__(self, *args):
        
        # config
        self.programms_csv_file = 'programme.csv'
        self.mp3_dir = "" #use a trailing slash
        self.bibtex_file = 'bibliographie.bib'
        self.logfile = 'log.txt'
        self.oe1_json_path = 'http://oe1.orf.at/programm/konsole/tag/'
        self.date = datetime.fromordinal(datetime.today().toordinal()-1)
        print(self.date)
        programms = self.load_programms_csv(self.programms_csv_file)
        online_available_programms = self.fetch_online_programms_by_date(self.date,self.oe1_json_path)
        self.percentage_prev = 0
        
        for programm in online_available_programms:
            if programm['short_title'] in programms:
                mp3filename =  time.strftime("%Y%m%d%H%M")+"_"+programm['short_title']+"_"+programm['id']
                self.download_mp3(programm['url_stream'],self.mp3_dir,mp3filename)
                entry = programm
                entry['filename'] = mp3filename 
                self.update_bib_db(self.bibtex_file,entry)
    
    
    def load_programms_csv(self,csv_file):
        programms = list()
        with open(self.programms_csv_file, 'r') as csvfile:
            programms_csv = csv.reader(csvfile, delimiter='\"', quotechar=';')
            for csv_row in programms_csv:
                programms.append(csv_row[0])
        return programms
    
    def fetch_online_programms_by_date(self,date,uri):
        
        date_string = date.strftime("%Y%m%d")
        oe1_json_url= uri+date_string
        
        for i in range(0, 10):
            try :
                urlresponse = urllib.request.urlopen(oe1_json_url)
                break
            except:  
                print(('can not fetch url: '+oe1_json_url +'\n waiting 30s to try again'))
                time.sleep(30)
                if(i==10):
                    self.write_log('failed to download: '+oe1_json_url)
                    sys.exit()
        data = json.loads(urlresponse.read().decode('utf-8'))
        return data['list']
            
    def download_mp3(self,uri,path,filename):
        
        mp3_dest = self.mp3_dir+filename+'.mp3'
        mp3_dest.encode(sys.getfilesystemencoding())
        fp = open(mp3_dest,'wb')
        c = pycurl.Curl()
        c.setopt(pycurl.URL, uri)
        c.setopt(pycurl.CONNECTTIMEOUT,1800)
        c.setopt(pycurl.TIMEOUT,1800)
        c.setopt(pycurl.WRITEDATA, fp)
        c.setopt(c.NOPROGRESS, 0)
        c.setopt(c.PROGRESSFUNCTION, self.curl_progress)
        c.perform()
    
    def update_bib_db(self,bibfile,entry):
        fp_bib_db = open(self.bibtex_file,'a+')
        bibentry = '@HOERFUNK{\n'+entry['filename']+','+'title = {'+entry['title']+'}'+',\n'+'abstract = {'+entry['info']+'}'+',\n'+'url = {http://oe1.orf.at/programm/'+entry['id']+'}'+',\n'+'year = {'+time.strftime("%Y")+'}'+',\n'+'month = {'+time.strftime("%m")+'}'+',\n'+'note = {OE1},\n'+'series = {'+entry['short_title']+'}'+',\n'+'keywords = {Datenschutz, EU},\nowner = {gugu},\n'+'timestamp = {'+time.strftime("%Y.%m.%d %H:%M")+'}'+'}\n\n';
        fp_bib_db.write(bibentry)
        fp_bib_db.close()
        
    def write_log(self,newline):
        logp = open(self.logfile,'wp')
        logp.write('['+self.datetime.strftime("%Y%m%d %H:%M")+']: '+newline)
        logp.close()
        
    def curl_progress(self,download_t,download_d,upload_t,upload_d):
        if download_t > 0:
            percentage = int(100/download_t*download_d)
            if percentage != self.percentage_prev:
                self.percentage_prev = percentage
                print(percentage,'%')
            if percentage == 100:
                self.percentage_prev = 0
                

if __name__ == "__main__":
    main = oe1grabber()
    main()
