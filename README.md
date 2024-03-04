# Notification on email from IP cam about motion detected 
## What it do?  
 * Read the text stream (e.g. "alertStream") from IP a camera by HiWatch / Hikvision (e.g. "ISAPI" families, exempl URL: http://{IP}/ISAPI/Event/notification/alertStream);  
 * Looking for it in the text stream:
```xml
<eventDescription>Motion alarm</eventDescription>
```
 * Saves N a screenshot, one per two second (exempl URL: http://{IP}/ISAPI/Streaming/channels/{CAM_ID}/picture);  
 * Send their on Email;  
 * And next again read the text stream, for again search "Motion alarm" (recurse)...


## Install
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.example.py config.py
chmod u+x main.sh
mkdir temp
mkdir logs
```
Edit "config.py"...

## Run
```bash
./main.sh start
```
Also can use: start | stop | restart | status

## Add in: "crontab -e"? If you need...
```
* * * * * /{PATH}/main.sh start
```

## Conf for Logrotate
```
/{PATH}/logs/*log {
    su {USERNAME} {USERGROUP}
    missingok
    notifempty
    daily
    rotate 100
    compress
    sharedscripts
    postrotate
        sudo -u {USERNAME} /{PATH}/main.sh restart
    endscript
}
```
Add in: /etc/logrotate.d/camNotification
