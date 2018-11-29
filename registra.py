#coding= utf-8
#Python3
__autor__= "Edilson S.M"
#registra.py

import time
import os

diretorio = os.path.abspath(os.path.dirname(__file__))



nome_arq_g = time.strftime("%m-%Y")
arq_log_geral = "{dir}/logs/monitoramento.log-{mes}".format(dir=diretorio, mes=nome_arq_g)
nome_arq_l = time.strftime("%d-%m-%Y")
arq_lat = "{dir}/logs/latencia-{dia}".format(dir=diretorio, dia=nome_arq_l)

#Arquivos de status
arq_alert_lat = "{dir}/status/.status_alert_latencia".format(dir=diretorio)
arq_alert_web = "{dir}/status/.status_alert_web".format(dir=diretorio)
arq_status_aciona = "{dir}/status/.status_aciona".format(dir=diretorio)
arq_status_mysql = "{dir}/status/.status_mysql".format(dir=diretorio)
arq_init_mysql = "{dir}/tmp/init_mysql".format(dir=diretorio)

#Funcao para registrar log do evento
def registra(tipo, msg):
    momento = time.strftime("%d-%m-%Y %H:%M:%S ")
    hora = time.strftime("%H:%M:%S ")
    if tipo == "status_lat":
        op_arq_alert = open(arq_alert_lat, "a")
        op_arq_alert.close()
        op_arq_alert = open(arq_alert_lat, "w")
        op_arq_alert.write(msg)
        op_arq_alert.close()

    if tipo == "status_web":
        op_arq_alert = open(arq_alert_web, "a")
        op_arq_alert.close()
        op_arq_alert = open(arq_alert_web, "w")
        op_arq_alert.write(msg)
        op_arq_alert.close()

    if tipo == "latencia":
        op_arq_lat = open(arq_lat, "a")
        op_arq_lat.writelines("{mm} Latencia media : {lt} ms\n".format(mm=momento, lt=msg))
        op_arq_lat.close()

    if tipo == "log_geral":
        log = open(arq_log_geral, "a")
        log.write(momento + msg)
        log.close()

    if tipo == "status_aciona":
        op_arq_aciona = open(arq_status_aciona, "a")
        op_arq_aciona.close()
        op_arq_aciona = open(op_arq_aciona, "w")
        op_arq_aciona.write(msg)
        op_arq_aciona.close()

    if tipo == "init_mysql":
        op_init_mysql = open(arq_init_mysql, "a")
        op_init_mysql = open(arq_init_mysql, "w")
        op_init_mysql.write(msg)
        op_init_mysql.close()

    if tipo == "status_mysql":
        op_arq_mysql = open(arq_status_mysql, "a")
        op_arq_mysql = open(arq_status_mysql, "w")
        op_arq_mysql.write(msg)
        op_arq_mysql.close()