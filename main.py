from dotenv import load_dotenv

from datetime import datetime
from json import load,dumps
from os import getenv,popen
from exceptions import InvalidIPv4
from regex_patterns import IPV4_PATTERN

load_dotenv()

DNS_SERVER = getenv("DNS_SERVER")
DOMAIN = getenv("DOMAIN")
PASSWORD = getenv("PASSWORD")


def is_valid_ipv4(ip:str) -> bool:
    """validates if valid ipv4 ip"""
    if not bool(IPV4_PATTERN.search(ip)): raise InvalidIPv4(ip)
    return ip
  

def load_ip():
    """"""
    try:
        return load(open('ip.json','r'))
    except FileNotFoundError:
        store_ip({"ip" : "","is_confirmed" : True})
        return load(open('ip.json','r'))
  

def store_ip(ip):
    """"""
    open('ip.json','w').write(dumps(ip))


def log_error():
    """"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    open('error.log','a').write(f"{now} [Error]: couldn't connect to the DNS_SERVER = {DNS_SERVER}\n")


def curl(host,method:str = "PUT",body:dict = {}, connect_timeout:int = 5,max_time:int = 10,retry:int = 7,retry_delay = 0,retry_max_time:int = 40):
    """"""

    payload = f'-H "Content-Type: application/json" -d \'{ dumps(body) }\'' if body else ""
    print(payload)
    return popen(f'curl -s -X {method.upper()} \
                        {payload}\
                        "{host}"\
                        --connect-timeout {connect_timeout}\
                        --max-time {max_time}\
                        --retry {retry}\
                        --retry-delay {retry_delay}\
                        --retry-max-time {retry_max_time}\
                ')


def check_public_ip():
    """"""
    externalIP = is_valid_ipv4(curl("ifconfig.me", method="GET").read())
    stored_ip = load_ip()

    if stored_ip["ip"] != externalIP or not bool(stored_ip['is_confirmed']):
        
        stored_ip["ip"] = externalIP
        stored_ip["is_confirmed"] = False
        store_ip(stored_ip)
        
        res = update_ddns(stored_ip["ip"])
        if res["response"] == "Confirm":
            stored_ip["is_confirmed"] = True 
            store_ip(stored_ip)
        else :
            log_error()


def update_ddns(ip):
    """"""
    return load(curl(DNS_SERVER,body={'password':PASSWORD,'domain':DOMAIN,'ip':ip}, method="PUT"))

if __name__ == '__main__':
    check_public_ip()
    # log_error()