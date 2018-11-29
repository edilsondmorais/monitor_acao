#coding: utf-8
__autor__= "Edilson S.M"
#connect.py

##OBS: Necessario instalar o modulo abaixo
#pip install paramiko

from paramiko import SSHClient
import paramiko
from config import ip_host, user_host, passwd_host, user_mysql, passwd_mysql, select_mysql, ip_host_nginx, user_host_nginx, passwd_host_nginx

class SSHMysql:
    def __init__(self):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=ip_host, username=user_host, password=passwd_host)

    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        if stderr.channel.recv_exit_status() == 0 or stderr.channel.recv_exit_status() == 3:
            retorno = str(stdout.read())
            return retorno

        else:
            retorno = str(stderr.read())
            return retorno


class SSHNginx:
    def __init__(self):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=ip_host_nginx, username=user_host_nginx, password=passwd_host_nginx)

    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        if stderr.channel.recv_exit_status() == 0 or stderr.channel.recv_exit_status() == 3:
            retorno = str(stdout.read())
            return retorno

        else:
            retorno = str(stderr.read())
            return retorno

class SSHServNginx:
    def __init__(self):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=ip_host_nginx, username=user_host_nginx, password=passwd_host_nginx)

    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        if stderr.channel.recv_exit_status() == 0 or stderr.channel.recv_exit_status() == 3:
            return 0

        else:
            return 1