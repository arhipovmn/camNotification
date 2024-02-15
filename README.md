# Notification on email from IP cam about motion detected 
## What it do?  
 * Read the text stream (e.g. "alertStream") from IP a camera by HiWatch / Hikvision (e.g. "ISAPI" families, exempl URL: http://{IP}/ISAPI/Event/notification/alertStream);  
 * Looking for it in the text stream:
```xml
<eventDescription>Motion alarm</eventDescription>
```
 * Saves N a screenshot, ~one per second (exempl URL: http://{IP}/ISAPI/Streaming/channels/{CAM_ID}/picture);  
 * Send their on Email;  
 * And next again read the text stream, for again search "Motion alarm" (recurse)...


## Install
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.example.py config.py
chmod u+x main.sh
```
edit "config.py"...

## Run
```bash
./main.sh
```

## Add in crontab:
```
* * * * * root /{PATH}/main.sh
```
