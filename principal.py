#coding= utf-8
#Python3
__autor__= "Edilson S.M"
#principal.py

from proxy_nginx import desativar_proxy_nginx, ativar_proxy_nginx
from mysql import registra_status_mysql, exec_mysql , ver_status_cluster
from ver_status import ver_status_proxy
from monitor_web import consult_web
from registra import registra
import os
import time

diretorio = os.path.abspath(os.path.dirname(__file__))

arq_alert_lat = "{dir}/status/.status_alert_latencia".format(dir=diretorio)
#arq_status_aciona = "/home/edilson/PycharmProjects/wifimax/status/.status_aciona"

def ver_status_alert(a):
    op_arq_alert = open(a, "r")
    for i in op_arq_alert:
        return i

# Funcao para executar a acao no proxy
def func_proxy(acao):
    if acao == "off":
        print("Desativar Proxy pass")
        msg_log = "Atencao - O proxy_pass sera desativado - latencia alta\n"
        registra("log_geral", msg_log)
        desativar_proxy_nginx()
    if acao == "on":
        print("Ativar Proxy pass")
        msg_log = "Atencao - O proxy_pass sera ativado - latencia normalizou\n"
        registra("log_geral", msg_log)
        ativar_proxy_nginx()

def verifica_aciona():
    try:
        resp_sit_lt = ver_status_alert(arq_alert_lat)
        if resp_sit_lt == "latencia_alta":
            resp_sit_wb = consult_web() # consultar
            if resp_sit_wb == "FAIL":
                func_proxy("off")
                status_proxy = ver_status_proxy() ## Consultar Proxy, se desativou entao pare o mysql
                if status_proxy == "False":
                    resp_mysql = registra_status_mysql()
                    if resp_mysql == "Status True":
                        exec_mysql("stop")
                    elif resp_mysql == "Status False":
                        registra("log_geral", "Atencao - O Mysql ja esta stop -  Nada feito feito....")

            if resp_sit_wb == "OK":
                registra("log_geral","Latencia alta mas Web ainda OK\n")

            if resp_sit_wb == ("DNS_FAIL"):
                registra("log_geral", "Atencao - Acesso Web com erro de DNS\n")

        elif resp_sit_lt == "latencia_normal":
            resp_mysql = registra_status_mysql() # Consultar status do Mysql
            if resp_mysql == "Status False":
                exec_mysql("start")     # Iniciar mysql
            elif resp_mysql == "Status True":
                registra("log_geral", "Atencao - O Mysql ja esta em execucao...\n")

            resp_cluster = ver_status_cluster()# consultar se o Mysql esta sincronizado com o cluster
            if resp_cluster == "tSynced":
                registra("log_geral","Mysql Sincronizado\n")
                resp_sit_wb = consult_web()  # consultar se acesso web esta ok
                if resp_sit_wb == "FAIL":
                    registra("log_geral", "Status da recuperacao | Latencia normal | Mysql Sincronizado | Web ainda esta Fora\n")
                if resp_sit_wb == "OK":
                    func_proxy("on")
                    registra("log_geral", "Status da recuperacao | Latencia normal | Mysql Sincronizado | Proxy_pass Ativo\n")
                    #registra("log_geral", "Latencia normalizado - Acesso Web Ok\n")
                if resp_sit_wb == ("DNS_FAIL"):
                    registra("log_geral", "Atencao -Latencia normal, mas Acesso Web com erro de DNS\n")

            else:
                registra("log_geral", "Status de recuperacao | Latencia normal | Mysql Nao sincronizado\n")



        elif resp_sit_lt == "host_fora":
            registra("log_geral", "Servidor nao responde a ping, nada a fazer\n")

    finally:
        pass

#verifica_aciona()