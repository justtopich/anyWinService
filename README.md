# AnyWinService

Start any program or srcipt as Windows service!



## Settings

Configure your application in **settings.cfg** Example for some java:

```ini
[service]
name = myApp-svc
displayname = myApp service wrapper
description = myApp service wrapper

[logger]
enable=True
logMaXSizeMb=200
logMaxFiles=20

[app]
exe = java
exePath = C:\app\myApp
exeKey = -jar "C:\app\myApp\app.jar"
stopSignal = ctrl+c
```



##### service

* **name** - service name (this will showed in task manager)
* **displayName** (this will showed in task manager)
* **description**

##### logger

* **enable** - redirect application output to **app.log**
* **logMaxSizeMb** - old files will be zipped
* **logMaxFiles**

##### app

* **exe** - running application
* **exePath** - application working directory
* **exeKey** - command line arguments
* **stopSignal** - stop event for you application. Use `kill` or `ctr+c`



## Install

Execute anyWinService

> anyWinService.exe ***key***

Where **key** is one of:

| Key     | action                 |
| ------- | ---------------------- |
| install | install service        |
| remove  | delete service by name |
| update  | update service by name |
| run     | start application      |

After installing you service will appear in task manager and can be configured in **Services**

## Building from sources

Use **python3.6+** and **pyinstaller 4**

> WARNING:  If you require Windows 7 support, please install Python <= 3.7.9. See PEP 11



```shell
python --version
# Python 3.9.6

python -m venv .venv
.venv/Scripts/activate

pip install -r requirements.txt
python __build_pyInst.py
```

