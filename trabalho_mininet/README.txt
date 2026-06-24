TRABALHO FINAL - REDES DE COMPUTADORES
Tema: DevOps – Infra Virtualizada para Aplicações

Aluno: João Victor Nascimento

====================================================
DESCRIÇÃO
====================================================

Projeto desenvolvido utilizando a ferramenta Mininet para simulação de uma infraestrutura virtualizada contendo:

- DMZ (Zona Desmilitarizada)
- Firewall/NAT
- Rede de Clientes Internos
- Rede de Serviços
- Rede de Banco de Dados
- API Web Flask para gerenciamento de estoque
- Serviço SSH
- Serviço FTP
- Banco de Dados MongoDB

====================================================
TOPOLOGIA IMPLEMENTADA
====================================================

DMZ
- CE (Cliente Externo)
- SDMZ (Switch DMZ)
- FW (Firewall/NAT)

Rede de Clientes Internos
- c1
- c2
- c3
- c4
- c5

Rede de Serviços
- servidorSSH
- servidorFTP
- estoqueAPI

Rede de Banco de Dados
- servidorMongoDB

Roteadores
- R1
- R2
- R3

====================================================
ENDEREÇAMENTO IP
====================================================

DMZ:                    172.17.0.0/12
Rede Serviços:          192.168.26.0/24
Rede Banco de Dados:    192.168.48.0/24
Rede Clientes:          192.168.117.0/24
Link R1-R2:             10.1.0.0/16
Link R1-R3:             10.6.0.0/16
Link R2-R3:             10.9.0.0/16

====================================================
SEGURANÇA IMPLEMENTADA
====================================================

Firewall configurado utilizando regras iptables.

PERMITIDO:
- CE -> servidorSSH (porta 22)
- CE -> servidorFTP (porta 21)
- CE -> estoqueAPI (porta 5000)

BLOQUEADO:
- CE -> Clientes Internos (c1 a c5)
- CE -> servidorMongoDB
- Clientes Internos -> servidorSSH
- Clientes Internos -> servidorFTP
- Clientes Internos -> estoqueAPI

Apenas o Cliente Externo (CE) possui acesso aos serviços disponibilizados na Rede de Serviços.

====================================================
API WEB
====================================================

Tecnologia:
- Python 3
- Flask

Tema:
Estoque-Produtos

Estrutura dos registros:

{
    "id": "P001",
    "quantidade": 10,
    "descricao": "Mouse Gamer",
    "preco": 99.90
}

Operações CRUD implementadas:

GET
- Listar produtos
- Buscar produto por ID

POST
- Criar produto

PUT
- Atualizar produto

DELETE
- Remover produto

====================================================
DEPENDÊNCIAS
====================================================

Python:
pip3 install flask
pip3 install pyftpdlib

Pacotes Linux:
sudo apt update

sudo apt install openssh-server -y

sudo apt install netcat-openbsd -y

====================================================
EXECUÇÃO
====================================================

Limpar ambiente Mininet:

sudo mn -c

Executar o projeto:

sudo python3 projeto_final.py

====================================================
ARQUIVOS ENTREGUES
====================================================

- projeto_final.py
- api_estoque.py
- README.txt

====================================================
TESTES REALIZADOS
====================================================

Serviços acessíveis pelo Cliente Externo (CE):
- SSH OK
- FTP OK
- API Flask OK

Serviços bloqueados:
- CE -> Clientes Internos OK
- CE -> MongoDB OK
- Clientes Internos -> SSH OK
- Clientes Internos -> FTP OK
- Clientes Internos -> API OK

CRUD da API:
- GET OK
- POST OK
- PUT OK
- DELETE OK

