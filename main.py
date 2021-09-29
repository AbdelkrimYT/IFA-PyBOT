from multiprocessing import Process
from chromebrowser import ChromeBrowse
import json

def main():
    chrome_browser = ChromeBrowse()
    chrome_browser.login()
    chrome_browser.run()


if __name__ == '__main__':
    with open('settings.json', 'r') as f:
         cpu = json.load(f)['cpu']
    process = [Process(target=main) for i in range(cpu)]
    for p in process:
        p.start()
    for p in process:
        p.join()
