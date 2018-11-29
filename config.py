#coding: utf-8
__autor__= "Edilson S.M"
#config.py


#####################################################################################################################
#DADOS DE ACESSO AO BANCO MYSQL PARA USO DO MODULO CONNECT
####################################################################################################################
user_mysql = "usuario" # usuario do mysql
passwd_mysql = "senha" # senha do  mysql
select_mysql = "\'show status like \"wsrep_local_state_comment%\";\'" # select para conferir se o node esta sinc

####################################################################################################################
#DADOS DE ACESSO AO SERVIDOR ONDE ESTA MYSQL PARA USO MODULO CONNECT
####################################################################################################################
ip_host = str("177.66.156.55") # IP do servidor onde esta o mysql
user_host = str("root")        # Usuario para conexao via ssh
passwd_host = "<senha>"      # Senha do usuario

####################################################################################################################
#DADOS DE ACESSO AO SERVIDOR ONDE ESTA O NGINX PARA USO NO MODULO PROXY_NGINX
####################################################################################################################

ip_host_nginx = str("187.103.139.100") # IP do servidor onde esta o nginx
user_host_nginx = str("root") # Usuario para conexao via ssh 
passwd_host_nginx = "<senha>" # Senha

#####################################################################################################################
# PARAMETROS PARA USO DO MODULO monitor_latencia
####################################################################################################################
# DESCRICAO:
# ip_destino = "177.66.156.55" #Ip do host onde esta o node do cluster a ser monitorado
# interv_ping = 10 # a cada N segundos sera enviado um ping, use valor inteiro para segundos
# qt_interv_ping = 3 # quantidade de vezes que a cada interv_ping sera obtido a media da latencia
# Exemplo: se no interv_ping tiver com 30 e o qt_interv_ping tiver 2, a cada 60 segundos será fornecido a media
# latencia_avg_limite = 62  # Valor maximo permitido da latencia
# tmp_permit_alta = 60 # Sera tolerado a latencia alta ate este valor # Em segundos 180 = 3minutos
# tmp_recuper = 120 # Necessario a latencia permanecer normal durante no minimo este valor # Em segundos  600 = 6minutos
####################################################################################################################

ip_destino = "177.66.156.41" # IP QUE SERA MONITORADO
interv_ping = 10
qt_interv_ping = 3
latencia_avg_limite = 62
tmp_permit_alta = 60
tmp_recuper = 120


#####################################################################################################################
# PARAMETROS PARA USO DO MODULO proxy_nginx
# Nomes dos arquivos a serem renomeados
####################################################################################################################

sem_proxy = "/etc/nginx/sites-available/login.dominio.com.br.vhost"         # Arquivo sem o proxy_pass
sem_proxy_tmp = "/etc/nginx/sites-available/login.dominio.com.br.vhost-old"
com_proxy = "/etc/nginx/sites-available/login.dominio.com.br-com-proxy.vhost"  # Arquivo com o proxy_pass ativo
com_proxy_tmp = "/etc/nginx/sites-available/login.dominio.com.br-com-proxy.vhost-old"

## FIM
