oe1downloader
=============

Downloads selected radio programms from yesterday, from the Austrian Radio Station Ö1, meant to be run via cron

The Programm is written in Python, and allthogh its poorly written, it does what it is supposed to do...

At the moment the Program consists of three files:

1. oe1grabber <- obviosly the code
2. programme.csv <- a simple CSV file, containing a list of programms titels to be downloaded(e.g Nachrichten)
3. bibliographie.bib <- a bibtex file serving as DB for the downloaded mp3s

TODOs:

-multiple DB support
-command line arguments , e.g select date
-clean code
