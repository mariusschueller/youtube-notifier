import urllib.request
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

channels = [c.strip().strip("'\"") for c in os.environ.get("channels", "").split(",") if c.strip()]
email = os.environ.get("email", "").strip().strip("'\"")
password = os.environ.get("app_password", "").strip().strip("'\"")

for channel in channels:
    print("checking " + channel)
    url = urllib.request.urlopen(channel)

    html_code = url.read().decode()

    target = "{\"webCommandMetadata\":{\"url\":\"/watch?v="

    position = html_code.find(target)+len(target)
    end = html_code[position:position+100].find("webPageType") - 3
    video_id = html_code[position:position+end]

    if html_code[position:position+end+2000].find("hour") != -1:
        print("recent video found!")
        link = ("xoutu.be/" + video_id)
        print(link)

        msg = MIMEText(link)
        msg['Subject'] = "New Youtube Video " + channel[channel.find("@"): channel.find("/videos")]
        msg['From'] = email
        msg['To'] = email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(email, password)
            smtp_server.sendmail(email, email, msg.as_string())
        print("Email sent!")
    else:
        print("no recent videos")

    print()

