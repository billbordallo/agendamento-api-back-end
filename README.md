# API do sistema de agendamentos
_versão: 1.0_

Este repositório contém o microsserviço referente à funcionalidade de agendamento do MVP para a Sprint _Desenvolvimento Back-End Avançado_, da PUC-RIO.

Trata-se de um sistema de agendamento de clientes para profissionais liberais. O sistema completo engloba quatro microsserviços, cada um com seu próprio repositório.

## Repositórios necessários para rodar a aplicação

Para rodar o sistema completo, é necessário clonar os 4 repositórios, localizados em:

- **Repositório 1** - agendamento-api-front-end-admin: é a interface principal, que será utilizada pelo profissional liberal. Nele, é possível visualizar os agendamentos existentes, confirmar ou não a data, e inserir o compromisso no Google Agenda, através da API do mesmo.

- **Repositório 2** - [agendamento-api-back-end-admin](https://github.com/billbordallo/agendamento-api-back-end-admin): contém uma API com o back-end do sistema de administração e se comunica com o Repositório 1. Contém os bancos de dados referentes à autenticação do usuário (profissional liberal) e a tabela de serviços oferecidos.

- **Repositório 3** - agendamento-api-front-end: é a interface pela qual os clientes do profissional liberal poderão realizar agendamentos. O sistema vai informar se o horário desejado está liberado ou não para agendamento.

- **Repositório 4** (**este repositório**) - agendamento-api-back-end: contém uma API com o back-end do sistema de agendamentos e se comunica com o Repositório 3. Contém o banco de dados com os agendamentos realizados, informações do cliente que realizou o agendamento (nome, telefone, e-mail, endereço, serviço desejado, dia e hora desejados), bem como o status do agendamento.

## Como instalar e executar este repositório usando o Docker

Para rodar este repositório usando o Docker (método recomendado), após clonar o mesmo, siga os passos:

1. Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

2. Navegue até o diretório que contém o `Dockerfile` e o `requirements.txt` no terminal.

3. Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t agendamento-api-back-end .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 5000:5000 agendamento-api-back-end
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.

## Como instalar e executar este repositório usando o Flask

Os requisitos para rodar o sistema são ter o **Python** instalado e as libs listadas no arquivo `requirements.txt`.

> É recomendado usar um ambiente virtual para rodar o sistema. Veja aqui como instalar o [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

```
(env)$ pip install -r requirements.txt
```

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) ou [http://127.0.0.1:5000/#/](http://127.0.0.1:5000/#/) no navegador para verificar o status da API em execução.

## Sobre o banco de dados

O banco de dados deste repositório utiliza o SQLite e será criado na primeira vez que o ambiente rodar. Os detalhes de criação do banco de dados estão em `model/__init__.py` e em `model/agendamento.py`. 

## Sobre o projeto

Este MVP foi desenvolvido por Fabiano Bordallo como trabalho final para a Sprint "Desenvolvimento Full Stack Avançado", da Pós-Graduação em Desenvolvimento Full Stack, do Departamento de Informática da PUC-Rio.