from cryptography.fernet import Fernet
import os


folderName = "D:\\Stuff\\D studies\\Adv dip of it\\Semester 5\\Applied projects\\Keylogger-for-Enterprise-Security\\Project\\log_files"
key = "BhbZu8TldX1E7eFjhfkppHVmbu7xZaW0XKMOI-eLXU4="  # enter key here

folders = [j for j in os.listdir(folderName) if os.path.isfile(os.path.join(folderName, j))]
for j in folders:
    x = "\\"
    z = folderName+x+j
    with open(z, 'rb') as f:
        # print(fileName)
        data = f.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    os.remove(z)
    with open(z, 'wb') as f:
        f.write(decrypted)

print("Files in folder decrypted")
