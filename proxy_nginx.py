#coding: utf-8
__autor__= "Edilson S.M"
#proxy_nginx.py
#
# O modulo ira renomear arquivos de configuracao do nginx ou apache2 para ativar ou desativar o proxy_pass.
# Funcionara assim; Em um arquivo o proxy_pass estara ativado e no outro o proxy_pass esta desativado.
# Quando for para ativar, sera passado o arqumento "--bemol ON" onde ira executar a funcao que renomeia o arquivo sem os
#parametros do proxy_pass para ".vhost-old" , e o arquivo com os parametros do proxy_pass renomeia para ".vhost"
#e da um reload no serviço, se ocorrer erro ao dar reload ele desfaz a alteração de nome

import os
import time
import argparse
from paramiko import SSHClient
from registra import registra
from ver_status import ver_status_proxy
from connect import SSHNginx, SSHServNginx
from config import sem_proxy, sem_proxy_tmp, com_proxy, com_proxy_tmp


###########################################################################################
# Nao e necessario alterar nada deste ponto para baixo
###########################################################################################

#Esta funcao retorna a string do comando que sera usado no acesso ssh
def arq_exist(arq):
    if arq == "sem_proxy":
        resposta = "if [ -e {sp} ]; then echo True; else False; fi".format(sp=sem_proxy)
    if arq == "sem_proxy_tmp":
        resposta= "if [ -e {spt} ]; then echo True; else False; fi".format(spt=sem_proxy_tmp)
    if arq == "com_proxy":
        resposta = "if [ -e {cp} ]; then echo True; else False; fi".format(cp=com_proxy)
    if arq == "com_proxy_tmp":
        resposta = "if [ -e {cpt} ]; then echo True; else False; fi".format(cpt=com_proxy_tmp)
    return resposta

#Esta funcao retorna a string do comando que sera usado no acesso ssh
def rename_arq(arq1,arq2):
    if arq1 == "sem_proxy_tmp" and arq2 == "sem_proxy":
        return "mv {spt} {sp}".format(spt=sem_proxy_tmp,sp=sem_proxy)
    if arq1 == "com_proxy" and arq2 == "com_proxy_tmp":
        return "mv {cp} {cpt}".format(cp=com_proxy,cpt=com_proxy_tmp)
    if arq1 == "sem_proxy" and arq2 == "sem_proxy_tmp":
        return "mv {sp} {spt}".format(sp=sem_proxy,spt=sem_proxy_tmp)
    if arq1 == "com_proxy_tmp" and arq2 == "com_proxy":
        return "mv {cpt} {cp}".format(cpt=com_proxy_tmp,cp=com_proxy)


diretorio = os.path.abspath(os.path.dirname(__file__))

#criar o arquivo farol caso nao exista
arq_status = "{dir}/status/.status_proxy".format(dir=diretorio)
init_arq = open(arq_status, "a")
init_arq.close()

#Funcao para verificar se o arquivo ja esta renomeado
def consulta_proxy():
    ssh = SSHNginx()
    arq1 = arq_exist("sem_proxy")
    result1 = ssh.exec_cmd(arq1)
    arq2 = arq_exist("com_proxy_tmp")
    result2 = ssh.exec_cmd(arq2)
    print(result2)
    if result1 == "b\'True\\n\'" and result2 == "b\'True\\n\'":
        return 1 # Desativado
    else:
        return 0 # Ativado

#Funcao para consultar o status atual
def status():
    op_arq_status = open(arq_status, "r")
    #arq_status = op_arq_status.readlines()
    for i in op_arq_status:
        dic_arq_status = i.split(" ")
        print("Status atual :", dic_arq_status[1])
        return dic_arq_status[1]

def registra_status(msg):
    ope_arq_status = open(arq_status, "w")
    ope_arq_status.write(msg)
    ope_arq_status.close()

def regist_status_proxy():
    #op_arq_status = open(arq_status, "r")
    #cont_arq_status = op_arq_status.readlines()
    #qt_arq_status = int(len(cont_arq_status))
    #init_arq.close()
    c_proxy = arq_exist("com_proxy")
    s_proxy = arq_exist("sem_proxy")
    ssh = SSHNginx()
    c_proxy = ssh.exec_cmd(c_proxy)
    s_proxy = ssh.exec_cmd(s_proxy)

    if c_proxy == "b\'True\\n\'" and s_proxy == "b\'bash: False: command not found\\n\'":
        status = "Status True "
        registra_status(status)
    if s_proxy == "b\'True\\n\'" and c_proxy == "b\'bash: False: command not found\\n\'":
        status = "Status False "
        registra_status(status)
    if c_proxy == "b\'bash: False: command not found\\n\'" and s_proxy == "b\'bash: False: command not found\\n\'":
        status = "Status Unknown "
        registra_status(status)

#Funcao para desativar o proxy_pass, quando a bemol esta com problema de latencia
def desativar_proxy_nginx():
    registra("log_geral","Requisicao para Desativar o proxy da bemol, aguarde confirmacao....\n")
    consultar_status = ver_status_proxy()
    if consultar_status == "True":
        try:
            ssh = SSHNginx()
            com1 = rename_arq("sem_proxy_tmp", "sem_proxy")
            ssh.exec_cmd(com1)
            com2 = rename_arq("com_proxy", "com_proxy_tmp")
            ssh.exec_cmd(com2)
            consulta = consulta_proxy()
            if consulta == 1:
                resultado = "Arquivo com proxy_pass foi renomeado para (-old)\n"
                registra("log_geral", resultado)
                ssh_rest = SSHServNginx()
                resp_rest = ssh_rest.exec_cmd("/etc/init.d/nginx reload")
                if resp_rest == 0 :
                    registra("log_geral", "Servicos do NGINX reiniciado - Proxy_pass Desativado com sucesso\n")
                    status = "Status False "
                    registra_status(status)
                    #return "Desativado-OK"
                else:
                    registra("log_geral", "Ocorreu erro ao reiniciar o servico\n")
                    # Tenta desfazer a alteracao do arquivo acima
                    desf1 = rename_arq("sem_proxy", "sem_proxy_tmp")
                    ssh.exec_cmd(desf1)
                    desf2 = rename_arq("com_proxy_tmp", "com_proxy")
                    ssh.exec_cmd(desf2)
                    consulta_p = consulta_proxy()
                    if consulta_p == 0:
                        registra("log_geral", "Desfeito a alteracao anterior - Desativacao abortada\n")
                        status = "Status True "
                        registra_status(status)
                    else:
                        status = "Status Unknown "
                        registra_status(status)
                        #return "Desativado-Unknown"

        except OSError:
            #resp_error_zabbix = 3 #Nada foi feito
            #print(resp_error_zabbix)
            resultado = "Ocorreu erro ao renomear\n"
            registra("log_geral", resultado)
            retorno = consulta_proxy()
            if retorno == 1:
                registra("log_geral", "Arquivo Sem o proxy_pass ja esta em uso!\n")
                status = "Status False "   # Alterando o status, pois se estivesse correto ele nao entrava no bloco
                registra_status(status)

            if retorno == 0:
                registra("log_geral","Arquivo Com proxy_pass ainda esta uso - Verifique!!\n")
    else:
        registra("log_geral", "Nada foi feito !! O proxy ja esta Desativado!\n")
        print("Proxy pass ja esta desativado - Nada foi feito")

def ativar_proxy_nginx():
    registra("log_geral","Requisicao para Desativar o proxy da bemol, aguarde confirmacao....\n")
    consultar_status = ver_status_proxy()
    if consultar_status == "False":
        try:
            ssh = SSHNginx()
            com1 = rename_arq("sem_proxy", "sem_proxy_tmp")
            ssh.exec_cmd(com1)
            com2 = rename_arq("com_proxy_tmp", "com_proxy")
            ssh.exec_cmd(com2)
            consulta = consulta_proxy()
            if consulta == 0:
                resultado = "Arquivo Sem proxy_pass foi renomeado para (-old)\n"
                registra("log_geral", resultado)
                ssh_rest = SSHServNginx()
                resp_rest = ssh_rest.exec_cmd("/etc/init.d/nginx reload")
                if resp_rest == 0:
                    registra("log_geral", "Servicos do NGINX reiniciado - Proxy_pass Ativado com sucesso\n")
                    status = "Status True "
                    registra_status(status)

                else:
                    registra("log_geral", "Ocorreu erro ao reiniciar o servico\n")
                    # Tenta desfazer a alteracao do arquivo acima
                    desf1 = rename_arq("sem_proxy_tmp", "sem_proxy")
                    ssh.exec_cmd(desf1)
                    desf2 = rename_arq("com_proxy", "com_proxy_tmp")
                    ssh.exec_cmd(desf2)
                    consulta_p = consulta_proxy()
                    if consulta_p == 0:
                        registra("log_geral", "Desfeito a alteracao anterior - Ativacao abortada\n")
                        status = "Status False "
                        registra_status(status)
                    else:
                        status = "Status Unknown "
                        registra_status(status)
                        #return "Desativado-Unknown"

        except OSError:
            registra("log_geral", "Ocorreu erro ao renomear\n")
            retorno = consulta_proxy()
            if retorno == 0:
                registra("log_geral", "Arquivo Com o proxy_pass ja esta em uso!\n")
                status = "Status True "   # Alterando o status, pois se estivesse correto ele nao entrava no bloco
                registra_status(status)

            if retorno == 1:
                registra("log_geral","Arquivo Sem proxy_pass ainda esta uso - Verifique!!\n")
    else:
        registra("log_geral", "Nada foi feito !! O proxy ja esta Ativado!\n")
        print("Proxy pass ja esta Ativado - Nada foi feito")


def acao_proxy(acao):
    eval(acao)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--proxy', action='store', required=True, dest='proxy', help='Digite --proxy e ON ou OFF ou status')
    args = parser.parse_args()
    if args.proxy == "ON" or args.proxy == "on":
        acao_proxy("ativar_proxy_nginx()")
    if args.proxy == "OFF" or args.proxy == "off":
        acao_proxy("desativar_proxy_nginx()")
    if args.proxy == "status":
        acao_proxy("status()")

if __name__ == "__main__":
    main()


#acao_proxy("ativar_proxy_nginx()")
#acao_proxy("ver_status()")

