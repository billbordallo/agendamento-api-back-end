from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy import func

from sqlalchemy.exc import IntegrityError

from model import Session, Agendamento
from logger import logger
from schemas import *
from flask_cors import CORS

from clima import clima

info = Info(title="API de agendamento", version="1.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
agendamento_tag = Tag(name="Agendamento", description="Adição, visualização e remoção de agendamentos da base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/agendamento', tags=[agendamento_tag],
          responses={"200": AgendamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_agendamento(form: AgendamentoSchema):
    """Adiciona um novo Agendamento à base de dados

    Retorna uma representação do agendamento.
    """
    print(form)
    agendamento_feito = Agendamento(
        nome_cliente=form.nome_cliente,
        email_cliente=form.email_cliente,
        celular_cliente=form.celular_cliente,
        endereco_cliente=form.endereco_cliente,
        data_cliente=form.data_cliente,
        hora_cliente=form.hora_cliente,
        servico_cliente=form.servico_cliente,
        mensagem_cliente=form.mensagem_cliente,
        status_agendamento=form.status_agendamento
    )
    
    logger.info(f"Adicionando agendamento: '{agendamento_feito.nome_cliente}', '{agendamento_feito.data_cliente}', '{agendamento_feito.hora_cliente}'")
    try:
        # criando conexão com a base
        session = Session()

        # adicionando agendamento
        session.add(agendamento_feito)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.info("Adicionado agendamento: %s" % agendamento_feito)
        return apresenta_agendamento(agendamento_feito), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Não foi possível agendar, pois o dia e horário já estão ocupados :/"
        logger.warning(f"Erro ao adicionar agendamento, dia e horários já ocupados '{agendamento_feito.nome_cliente}', '{agendamento_feito.data_cliente}', '{agendamento_feito.hora_cliente}', {error_msg}, {e}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível realizar o agendamento :/"
        logger.warning(f"Erro ao adicionar agendamento '{agendamento_feito.nome_cliente}', '{agendamento_feito.data_cliente}', '{agendamento_feito.hora_cliente}', {error_msg}, {e}")
        return {"message": error_msg}, 400
    finally:
        session.close()


@app.get('/agendamentos', tags=[agendamento_tag],
         responses={"200": ListagemAgendamentoSchema, "404": ErrorSchema})
def get_agendamentos():
    """Faz a busca por todos os Agendamentos existentes

    Retorna uma representação da listagem de agendamentos.
    """
    logger.debug(f"Coletando agendamentos ")
    # criando conexão com a base
    session = Session()
    try:
        # fazendo a busca
        agendamentos = session.query(Agendamento).all()

        if not agendamentos:
            # se não há agendamentos cadastrados
            msg = "Não há agendamentos cadastrados :/"
            return {"message": msg}, 200
        else:
            logger.debug(f"%d agendamentos econtrados" % len(agendamentos))
            # retorna a representação de agendamento
            print(agendamentos)
            return apresenta_agendamentos(agendamentos), 200
    finally:    
        session.close()

@app.get('/agendamentos-dia', tags=[agendamento_tag],
         responses={"200": ListagemAgendamentoSchema, "404": ErrorSchema})
def get_agendamentos_dia(query: AgendamentoBuscaDiaSchema):
    """Faz a busca por todos os Agendamentos existentes em um mesmo dia

    Retorna uma representação da listagem de agendamentos.
    """
    logger.debug(f"Coletando agendamentos ")
    # criando conexão com a base
    session = Session()
    try:
        # fazendo a busca
        agendamento_dia = query.data_cliente
        # Busca todas as datas únicas
        agendamentos = session.query(Agendamento).filter(Agendamento.data_cliente == agendamento_dia).all()

        if not agendamentos:
            # se não há agendamentos cadastrados
            msg = "Não há agendamentos para esta data."
            return {"message": msg}, 200
        else:
            logger.debug(f"%d agendamentos econtrados" % len(agendamentos))
            # retorna a representação de agendamento
            print(agendamentos)
            return apresenta_agendamentos(agendamentos), 200
    finally:    
        session.close()

@app.get('/agendamentos-nome', tags=[agendamento_tag],
         responses={"200": ListagemAgendamentoSchema, "404": ErrorSchema})
def get_agendamentos_nome(query: AgendamentoBuscaNomeSchema):
    """Faz a busca por todos os Agendamentos existentes em um mesmo dia

    Retorna uma representação da listagem de agendamentos.
    """
    logger.debug(f"Coletando agendamentos ")
    # criando conexão com a base
    session = Session()
    try:
        # fazendo a busca
        agendamento_nome = query.nome_cliente
        # Busca por agendamentos com o mesmo nome
        agendamentos = session.query(Agendamento).filter(Agendamento.nome_cliente == agendamento_nome).all()

        if not agendamentos:
            # se não há agendamentos cadastrados
            msg = "Não há agendamentos para clientes com esse nome."
            return {"message": msg}, 200
        else:
            logger.debug(f"%d agendamentos econtrados" % len(agendamentos))
            # retorna a representação de agendamento
            print(agendamentos)
            return apresenta_agendamentos(agendamentos), 200
    finally:    
        session.close()

@app.delete('/agendamento', tags=[agendamento_tag],
            responses={"200": AgendamentoDelSchema, "404": ErrorSchema})
def del_agendamento(query: AgendamentoBuscaSchema):
    """Deleta um Agendamento a partir do id do agendamento

    Retorna uma mensagem de confirmação da remoção.
    """
    agendamento_id = query.id
    print(agendamento_id)
    logger.debug(f"Deletando dados sobre agendamento #{agendamento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Agendamento).filter(Agendamento.id == agendamento_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando agendamento #{agendamento_id}")
        return {"mesage": "Agendamento removido", "id": agendamento_id}, 200
    else:
        # se o agendamento não foi encontrado
        error_msg = "Agendamento não encontrado na base :/"
        logger.warning(f"Erro ao deletar agendamento #'{agendamento_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.put('/agendamento', tags=[agendamento_tag],
         responses={"200": AgendamentoViewSchema, "404": ErrorSchema})
def put_agendamento(query: AgendamentoBuscaSchema, form: AgendamentoAtualizaSchema):
    """Altera o status de um Agendamento a partir do id do agendamento

    Retorna uma representação do agendamento.
    """
    agendamento_id = query.id
    logger.debug(f"Alterando dados sobre agendamento #{agendamento_id}")
    # criando conexão com a base
    session = Session()
    try:
        # fazendo a busca
        agendamento = session.query(Agendamento).filter(Agendamento.id == agendamento_id).first()

        if not agendamento:
            # se o agendamento não foi encontrado
            error_msg = "Agendamento não encontrado na base :/"
            logger.warning(f"Erro ao buscar agendamento '{agendamento_id}', {error_msg}")
            return {"mesage": error_msg}, 404
        else:
            # alterando os dados
            agendamento.status_agendamento = form.status_agendamento
            # mesclando a instância atualizada com a sessão e confirmando a transação
            session.merge(agendamento)
            session.commit()
            logger.debug(f"Agendamento econtrado: '{agendamento.id}'")
            # retorna a representação de agendamento
            return apresenta_agendamento(agendamento), 200
    finally:
        session.close()

@app.get('/clima', tags=[agendamento_tag])
def get_clima():
    """Acessa a API OpenWeather para obter informações sobre o clima

    Retorna uma representação do clima para daqui a 24 horas, aproximadamente.
    """
    logger.debug(f"Acessando a previsão do tempo ")
        
    try:
        # acessando a API OpenWeather
        cidade, dia, descricao, temperatura = clima()
        logger.debug(f"Previsão do tempo: {cidade}, {dia} {descricao}, {temperatura}")
        # retorna a representação do clima
        return {"cidade": cidade, "Dia e hora":dia, "previsão": descricao, "temperatura": temperatura}, 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível acessar a previsão do tempo :/"
        logger.warning(f"Erro ao acessar a previsão do tempo, {error_msg}, {e}")
        return {"message": error_msg}, 400