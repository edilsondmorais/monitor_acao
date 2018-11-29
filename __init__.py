#coding= utf-8
#Python3
__autor__= "Edilson S.M"
#

##OBS: Necessario instalar o modulo abaixo
#pip install paramiko
#pip install pingparsing

###############################################################
## Este e o modulo que ser executado para a app iniciar
# python __init_.py
#
###############################################################

# OBS:
# O modulo config.py e onde estao os parametros que devem ser ajustado

# OBS:
# Por questao de seguranca durante a homologacao, no modulo mysql.py os comandos de stop e start no mysql,
# foram alterados para status, e quando for para producao deve ser alterado para o correto

import monitor_latencia

monitor_latencia