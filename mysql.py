#coding: utf-8
__autor__= "Edilson S.M"
#mysql.py
#opcao alternativa
#os.system("/usr/bin/ssh -P'SENHA' USUARIO@177.66.156.55")


##OBS: Necessario instalar o modulo abaixo
#pip install paramiko

###################################################################################################
# OBS:
# Por questao de seguranca durante a homologacao, o comandos de stop e start no mysql,
# forama alterados para status, e quando for para producao deve ser alterado para o correto
#
####################################################################################################
import argparse
from registra import registra
from ver_status import status_mysql, resp_init_mysql
from connect import SSHMysql
from config import user_mysql,passwd_mysql,select_mysql


### A ideia e este modulo consultar, filtrar e direcionar o status para o arquivo
def registra_status_mysql():
    ssh = SSHMysql()
    resp = str(ssh.exec_cmd("/etc/init.d/mysql status")) # direciona a resposta para o arq init_mysql
    registra("init_mysql",resp)
    resp_init = str(resp_init_mysql())  #Busca a resposta obtida para filtrar
    list_resp = resp_init.split(" ")
    pos4 = list_resp[4]
    pos5 = list_resp[5]
    #print(pos4)
    if pos4 == "(exited)" or pos4 == "(running)" or pos5 == "(exited)" or pos5 == "(running)":
        registra("status_mysql", "Status True")
        return "Status True"
    elif pos4 == "failed" or pos4 == "stop"or pos5 == "failed" or pos5 == "stop":
        registra("status_mysql", "Status False")
        return "Status False"
    else:
        registra("status_mysql", "Status Unknown")
        return "Status Unknown"

def ver_status_cluster():
    ssh = SSHMysql
    comando = str("mysql -u{u} -p{p} -e {cm} ".format(u=user_mysql,p=passwd_mysql,cm=select_mysql))
    resp_ver = str(ssh.exec_cmd(comando))
    list_resp = resp_ver.split("\\")
    status_sinc = list_resp[3]
    return status_sinc

#print(ver_status_cluster())

#Funcao para chamada interna
def exec_mysql(acao):

    if acao == "start":
        ssh = SSHMysql()
        ssh.exec_cmd("/etc/init.d/mysql status")
        status = str(ssh.exec_cmd("/etc/init.d/mysql status"))
        registra("init_mysql", status)
        registra_status_mysql()
        registra("log_geral", "/etc/init.d/mysql start Executado\n")
        print("")

    if acao == "stop":
        ssh = SSHMysql()
        ssh.exec_cmd("/etc/init.d/mysql status")
        status = str(ssh.exec_cmd("/etc/init.d/mysql status"))
        registra("init_mysql", status)
        registra_status_mysql()
        registra("log_geral", "/etc/init.d/mysql stop Executado\n")

    if acao == "status":
        ssh = SSHMysql()
        status = str(ssh.exec_cmd("/etc/init.d/mysql status"))
        registra("init_mysql", status)
        print(registra_status_mysql())

    if acao == "cluster":
        ssh = SSHMysql()
        status = str(ssh.exec_cmd("/etc/init.d/mysql status"))
        registra("init_mysql", status)
        print(registra_status_mysql())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mysql', action='store', required=True, dest='mysql', help='Digite --mysql e stop ou start ou status')
    args = parser.parse_args()
    if args.mysql == "start":
        ssh = SSHMysql()
        ssh.exec_cmd("/etc/init.d/mysql status")
        status = str(ssh.exec_cmd("/etc/init.d/mysql status"))
        registra("init_mysql", status)
        registra_status_mysql()

    if args.mysql == "stop":
        ssh = SSHMysql()
        ssh.exec_cmd("/etc/init.d/mysql status")
        status = str(ssh.exec_cmd("/etc/init.d/mysql status"))
        registra("init_mysql", status)
        registra_status_mysql()

    if args.mysql == "status":
        ssh = SSHMysql()
        status = str(ssh.exec_cmd("/etc/init.d/mysql status"))
        registra("init_mysql", status)
        print(registra_status_mysql())




if __name__ == "__main__":
    main()

'''
                                                                
def acao_mysql(acao):                                           
    if acao == "start":                                         
        ssh = SSH()                                             
        ssh.exec_cmd("/etc/init.d/mysql start")                 
        status = str(ssh.exec_cmd("/etc/init.d/mysql status"))  
        registra("init_mysql", status)                          
                                                                
    if acao == "stop":                                          
        ssh = SSH()                                             
        ssh.exec_cmd("/etc/init.d/mysql stop")                  
        status = str(ssh.exec_cmd("/etc/init.d/mysql status"))  
        registra("init_mysql", status)                          
                                                                
    if acao == "status":                                        
        ssh = SSH()                                             
        status = str(ssh.exec_cmd("/etc/init.d/mysql status"))  
        registra("init_mysql", status)                          
                                                                
'''
#acao_mysql("status")


#if __name__ == '__main__':
#    ssh = SSH()
#    ssh.exec_cmd("/etc/init.d/mysql status")