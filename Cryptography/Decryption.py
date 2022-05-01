from cryptography.fernet import Fernet
import os

encrypted_dir = input("Enter Directory name here: ")
#encrypted_dir = "C:\\Users\\Public\\Libraries\\Keylogger_python\\"
key = input("Enter Key here: ")
#key = "BhbZu8TldX1E7eFjhfkppHVmbu7xZaW0XKMOI-eLXU4="  # enter key here

folders = [j for j in os.listdir(encrypted_dir) if os.path.isfile(os.path.join(encrypted_dir, j))]
for j in folders:
    try:
        x = "\\"
        z = encrypted_dir+x+j
        with open(z, 'rb') as f:
            # print(fileName)
            data = f.read()
        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)

        os.remove(z)
        with open(z, 'wb') as f:
            f.write(decrypted)
            print("Files in folder decrypted")

    except:
        print("incorrect key")








