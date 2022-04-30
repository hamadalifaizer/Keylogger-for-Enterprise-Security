from browser_history import get_history
from browser_history.browsers import Firefox
from browser_history.utils import default_browser

file_path = "D:\\Stuff\\D studies\\Adv dip of it\\Semester 5\\Applied projects\\Keylogger-for-Enterprise-Security\\Project\\log_files\\"

f = Firefox()
outputs = f.fetch_history()
his = outputs.histories
outputs.save(file_path + 'history.json', output_format="json")

#BrowserClass = default_browser()

#if BrowserClass is None:
#    print("Could not retrieve default browser")

#else:
#    b = BrowserClass()
#    his = b.fetch_history().histories
#    his.save(file_path + 'history.json', output_format="json")

