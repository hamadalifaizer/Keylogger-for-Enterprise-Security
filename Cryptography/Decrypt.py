from cryptography.fernet import Fernet
import os


folderName = "D:\Stuff\D studies\Adv dip of it\Semester 5\Applied projects\Keylogger\Project\log_files"
encrypted_dir = f"{folderName}"
key = "BhbZu8TldX1E7eFjhfkppHVmbu7xZaW0XKMOI-eLXU4="  # enter key here

folders = [j for j in os.listdir(encrypted_dir) if os.path.isfile(os.path.join(encrypted_dir, j))]
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


