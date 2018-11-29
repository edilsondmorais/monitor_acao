#coding= utf-8
#Python3
__autor__= "Edilson S.M"
#status/ver_status.py

import os
diretorio = os.path.abspath(os.path.dirname(__file__))

arq_alert_lat = "{dir}/status/.status_alert_latencia".format(dir=diretorio)
arq_status_aciona = "{dir}/status/.status_aciona".format(dir=diretorio)
arq_status = "{dir}/status/.status_proxy".format(dir=diretorio)
arq_status_mysql = "{dir}/status/.status_mysql".format(dir=diretorio)
arq_init_mysql = "{dir}/tmp/init_mysql".format(dir=diretorio)


def ver_status(arq):
    if arq == "latencia":
        arquivo = arq_alert_lat
    if arq == "aciona":
        arquivo = arq_status_aciona

    op_arq_alert = open(arquivo, "r")
    for i in op_arq_alert:
        return i


def ver_status_proxy():
    init_arq = open(arq_status, "a")
    init_arq.close()
    op_arq_status = open(arq_status, "r")
    for i in op_arq_status:
        dic_arq_status = i.split(" ")
        return dic_arq_status[1]
    init_arq.close()
#print(ver_status_proxy())

def resp_init_mysql():
    op_arq_init_mysql = open(arq_init_mysql, "r")
    for i in op_arq_init_mysql:
        dic_arq_init_mysql = i.split("\\n")
        for p in dic_arq_init_mysql:
            if "Active: " in p:
                return (p)

def status_mysql():
    op_arq_status_mysql = open(arq_status_mysql, "r")
    stat = op_arq_status_mysql.readlines()
    op_arq_status_mysql.close()
    print(stat)


#print(status_mysql())