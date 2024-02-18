import requests
from requests.auth import HTTPDigestAuth
import datetime
import time
import smtplib, ssl
from pathlib import Path
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
from config import config
from logger import logger as logerInit
import os
from PIL import Image

try:
    logerInit().info(f"Runs execution")

    def send_to_email(files = []):
        logger = logerInit()
        logger.info(f"Trying to send pictures on email")

        try:
            send_to = [config['email-to']]
            assert isinstance(send_to, list)

            msg = MIMEMultipart()
            msg['From'] = config['email-from']
            msg['To'] = COMMASPACE.join(send_to)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = f"Motion Detected, IP: {config['IP-address-for-cam']}, channel: {config['channel-id-for-cam']}"

            text = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, IP: {config['IP-address-for-cam']}, channel: {config['channel-id-for-cam']}"

            msg.attach(MIMEText(text))

            for path in files or []:
                if os.path.exists(path):
                    part = MIMEBase('application', "octet-stream")
                    with open(path, 'rb') as file:
                        part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment; filename={}'.format(Path(path).name))
                    msg.attach(part)

            if config['email-smtp-port'] != '25':
                context = ssl.create_default_context()
                smtp = smtplib.SMTP_SSL(config['email-smtp-host'], config['email-smtp-port'], context=context, timeout=10)
            else:
                smtp = smtplib.SMTP(config['email-smtp-host'], config['email-smtp-port'], timeout=10)
            smtp.login(config['email-smtp-login'], config['email-smtp-password'])
            smtp.sendmail(config['email-from'], send_to, msg.as_string())
            smtp.quit()

            logger.info(f"Successed send pictures on email")
            
        except Exception as inst:
            logger.exception(inst)
            logger.error(f"Execution stopped")
        finally:
            for path in files or []:
                if os.path.exists(path): os.remove(path)

        read() # recurse ...

    def savePic():
        logger = logerInit()
        logger.info(f"Trying to save pictures")

        files = []
        for n in range(config['how-many-screenshots-to-take']):
            try:
                n = n+1
                r = requests.get(f"http://{config['IP-address-for-cam']}/ISAPI/Streaming/channels/{config['channel-id-for-cam']}01/picture", auth=HTTPDigestAuth(config['login-for-cam'], config['password-for-cam']),  stream=True)
                if r.status_code == 200:
                    with open(f'temp/img{n}.jpeg', 'wb') as f:
                        for chunk in r:
                            f.write(chunk)
                    if config['picture-wight'] > 0 and config['picture-height'] > 0:
                        size = config['picture-wight'], config['picture-height']
                        im = Image.open(f'temp/img{n}.jpeg')
                        im_resized = im.resize(size, Image.LANCZOS)
                        im_resized.save(f'temp/img{n}.jpeg', 'JPEG')
                    files.append(f'temp/img{n}.jpeg')
                    logger.info(f'{n} a picture save: temp/img{n}.jpeg')
                else:
                    logger.error(f'{n} a picture not save, status code {str(r.status_code)}')
            except Exception as inst:
                logger.exception(inst)
                logger.error(f'{n} a picture not save')
            finally:
                r.close()
                time.sleep(2)
        if (config['time-delay']): time.sleep(config['time-delay'])
        
        logger.info(f"Successed save pictures")

        send_to_email(files)

    def read():
        logger = logerInit()
        logger.info('=================================')
        logger.info(f"Trying to connect to alertStream")

        r = requests.get(f"http://{config['IP-address-for-cam']}/ISAPI/Event/notification/alertStream", auth=HTTPDigestAuth(config['login-for-cam'], config['password-for-cam']),  stream=True)
        if r.encoding is None: r.encoding = 'utf-8'

        if r.status_code == 200:
            logger.info(f"Successed connect to alertStream")

            logger.info(f"Starts to read the alertStream")

            motion = False
            for line in r.iter_lines(decode_unicode=True):
                if line and line == '<eventDescription>Motion alarm</eventDescription>':
                    logger = logerInit()
                    logger.info(f"MOTION DETECTED! Stop to read the alertStream")
                    motion = True
                    r.close()
                    break
            if motion == True: savePic()
            motion = False
        else:
            logger.error(f"Status code {str(r.status_code)}")

    read()
except Exception as inst:
    logerInit().exception(inst)
    logerInit().error(f"Execution stopped")
