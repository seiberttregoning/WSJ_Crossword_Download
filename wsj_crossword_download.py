#!/usr/bin/python3.9
# coding: utf-8

import requests
import datetime as dt
from datetime import datetime
import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# Get tomorrow's date and the WSJ url for the crossword for that date

tomorrow = (dt.date.today() + dt.timedelta(days=1)).strftime('%m%d%Y')
wsj_url = f'https://s.wsj.net/public/resources/documents/XWD{tomorrow}.pdf'

# Check if tomorrow's date is M-F

if (datetime.strptime(tomorrow, '%m%d%Y').weekday() in [0, 1, 2, 3, 4]):

    # Download the crossword PDF and write to this directory

    r = requests.get(wsj_url, stream=True)

    chunk_size = 2000

    with open(f'wsj_crossword_{tomorrow}.pdf', 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


    # Upload to google drive folder, Super Note -> Documents

    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    file_to_upload = f'wsj_crossword_{tomorrow}.pdf'

    gfile = drive.CreateFile({'parents': [{'id': '1Mawb_kpIzVyNyURWbF9qYq9o69Ztm-Yh'}]})

    gfile.SetContentFile(file_to_upload)

    gfile.Upload()

    # Delete pdf from directory

    os.remove(f'wsj_crossword_{tomorrow}.pdf')
else:
    pass