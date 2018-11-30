#README

###############################################################
### OBS : E NECESSARIO INSTALAR OS PACOTES ABAIXO
###############################################################
#pip2.7 install requests
#pip install paramiko
#pip install pingparsing
###############################################################
#
# OBS: No modulo config.py e onde estao os parametros que devem ser ajustado
#
# OBS: Por questao de seguranca durante a homologacao, no modulo mysql.py os comandos de stop e start no mysql,
# foram alterados para status, e quando for para producao deve ser alterado para o correto
#
###############################################################################################################################

Este programa sera usado para solucionar problema gerado no cluster de banco de dados devido a latencia alta entre o Node que esta em Manaus e os demais Nodes que estão em SP, este problema gera fila no sincronismo e conseguentemente o cluster entra em pausa aguardando o node de Manaus alcanca-los, como efeito também o acesso web fica fora.

Para tratar este problema criei este programa:

O modulo "monitor_latencia" obtem a media da latencia no periodo informado no modulo "config.py" e caso esteja alta durante o periodo configurado, sera consultado se o proxy_pass esta ativo e caso sim, sera acionado o modulo "principal" que consulta o acesso web acionando o monulo "monitor_web", e caso o acesso web esteja fora, o mesmo acionara o modulo "proxy_nginx" que desativa o proxy_pass no nginx e restarta o serviço, e apos o proxy_pass esta desativado o modulo "principal" aciona o modulo "mysql" e envia um stop parando o banco.

No modulo config.py deve ser configurado o tempo necessario que a latencia esteja normal, para poder fazer as etapas de recuperacao.
Para recuperacao o modulo "principal" primeiro aciona o modulo "mysql" enviando um start para banco e consulta ate o banco esta sincronizado no cluster e apos ele aciona o modulo "proxy_nginx" e ativa o proxy_pass retornando a normalizadade.


OBS: O Modulo que deve ficar em execução é o "monitor_latencia" e ele aciona os demais.

Caso queira, voce pode configurar o supervisor para executar este modulo, e entao ficara executando em segundo plano.

###############################################################################################################################
