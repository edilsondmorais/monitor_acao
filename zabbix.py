#coding=utf-8
#python3
__autor__="Edilson S.M"
#zabbix.py
#
import argparse
import os

###############################
# Para monitorar com o zabbix:#
###############################
# No server que estara com o programa em execucao, voce cria o arquivo userparameter_monitor_acao.conf no diretorio do agente do zabbix, caso nao saiba, acesse o zabbix.conf e veja o caminho.
# No arquivo userparameter_monitor_acao.conf voce coloca este texto abaixo, caso o script zabbix.py esteja em outro caminho e so alterar:
#
#UserParameter=monitor.acao[*],/usr/bin/python /usr/local/etc/zabbix_agentd.conf.d/zabbix.py --status $1
#
#
###########################
# No acesso web do Zabbix:#
###########################
# Voce deve criar itens no host que estara monitorando o programa, e usar a chave "monitor.acao[]" e dentro do colchete voce coloca o parametro que vc quer consultar exemplo "monitor.acao[web]" ou "monitor.acao[latencia]" o script  ira retornar o valor confirme os IFs abaixo;
# Apos feito isso so falta criar os triggers para gerar os alertas, o valor recebido e do tipo "caracter" devido ao "."ponto
#
## OBS: ####
# Os caminhos abaixo devem ser o caminho do diretorio "status" dentro do projeto
#
STATUSLAT = "/usr/local/etc/app_py/status/.status_alert_latencia"
STATUSWEB = "/usr/local/etc/app_py/status/.status_alert_web"
STATUSPRO = "/usr/local/etc/app_py/status/.status_proxy"
STATUSMYS = "/usr/local/etc/app_py/status/.status_mysql"

def consulta_status():
    parser = argparse.ArgumentParser()
    parser.add_argument( '--status',action='store', required=False, dest='status', help='Digite latencia ou web ou proxy ou mysql')
    args = parser.parse_args()
    if args.status == "latencia":
        cons = open(STATUSLAT, "r")
        op_cons = cons.readlines()
        cons.close()
        for i in op_cons:
            op_cons = i

        if op_cons == "latencia_normal":
            print(0.0)
        if op_cons == "latencia_alta":
            print(0.1)
        if op_cons == "host_fora":
            print(0.2)

    if args.status == "web":
        cons = open(STATUSWEB, "r")
        op_cons = cons.readlines()
        cons.close()
        for i in op_cons:
            op_cons = i
        if op_cons == "web_ok":
            print(1.0)
        if op_cons == "web_fora":
            print(1.1)
        if op_cons == "web_dns_error":
            print(1.2)

    if args.status == "proxy":
        cons = open(STATUSPRO, "r")
        op_cons = cons.readlines()
        cons.close()
        for i in op_cons:
            op_cons = i
        if op_cons == "Status True ":
            print(2.0)
        if op_cons == "Status False ":
            print(2.1)
        if op_cons == "Status Unknown ":
            print(2.2)

    if args.status == "mysql":
        cons = open(STATUSMYS, "r")
        op_cons = cons.readlines()
        cons.close()
        for i in op_cons:
            op_cons = i
        if op_cons == "Status True":
            print(3.0)
        if op_cons == "Status False":
            print(3.1)
        if op_cons == "Status Unknown":
            print(3.2)



if __name__ == "__main__":
    consulta_status()


