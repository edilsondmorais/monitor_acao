#Python3
__autor__= "Edilson S.M"
#monitor_web.py

import json, requests
from registra import registra

def consult_web():
    try:
        #response = requests.get("https://login.wifimax.com.br/admin/user.do?action=qa&id=5")
        response = requests.get("http://177.66.156.43:9125/admin/user.do?action=qa&id=5")
        if response.status_code != 400:
            registra("status_web", "web_fora")
            registra("log_geral", "Acesso web com falha\n")
            #print("WEB FAIL")
            return "FAIL"
        else:
            registra("status_web", "web_ok")
            #registra("log_geral", "Acesso web OK\n")
            return "OK"
    except requests.exceptions.ConnectionError:
        registra("status_web", "web_dns_error")
        registra("log_geral", "Erro de DNS no acesso Web\n")
        return "DNS_FAIL"


#print(consult_web())