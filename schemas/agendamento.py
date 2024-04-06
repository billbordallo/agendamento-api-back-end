from pydantic import BaseModel
from typing import Optional, List
from model.agendamento import Agendamento


class AgendamentoSchema(BaseModel):
    """ Define como um novo agendamento a ser inserido deve ser representado
    """
    id: Optional[int] = 1
    nome_cliente: str = "Maria"
    email_cliente: str = "nome@email.com"
    celular_cliente: str = "11999999999"
    endereco_cliente: str = "Avenida dos Eucaliptos, 815. Moema, São Paulo, SP"
    data_cliente: str = "2024-03-30"
    hora_cliente: str = "12:45"
    servico_cliente: str = "Corte de cabelo"
    mensagem_cliente: str = "Tocar o interfone"
    status_agendamento: str = "Aguardando confirmação"


class AgendamentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do agendamento.
    """
    id: int = 5

class AgendamentoBuscaDiaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por uma data (dia). Que será
        feita apenas com base na informação data_cliente.
    """
    data_cliente: str = "2024-03-30"


class AgendamentoBuscaNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do cliente.
    """
    nome_cliente: str = "Maria"

class AgendamentoAtualizaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca e a atualização do status.
      Que será feita apenas com base no id do agendamento.
    """
    id: int = 5
    status_agendamento: str = "Confirmado"

class ListagemAgendamentoSchema(BaseModel):
    """ Define como uma listagem de agendamentos será retornada.
    """
    agendamentos:List[AgendamentoSchema]


def apresenta_agendamentos(agendamentos: List[Agendamento]):
    """ Retorna uma representação do agendamento seguindo o schema definido em
        AgendamentoViewSchema.
    """
    result = []
    for agendamento in agendamentos:
        result.append({
            "id": agendamento.id,
            "nome_cliente": agendamento.nome_cliente,
            "email_cliente": agendamento.email_cliente,
            "celular_cliente": agendamento.celular_cliente,
            "endereco_cliente": agendamento.endereco_cliente,
            "data_cliente": agendamento.data_cliente,
            "hora_cliente": agendamento.hora_cliente,
            "servico_cliente": agendamento.servico_cliente,
            "mensagem_cliente": agendamento.mensagem_cliente,
            "status_agendamento": agendamento.status_agendamento,
        })

    return {"agendamentos": result}


class AgendamentoViewSchema(BaseModel):
    """ Define como um agendamento será retornado.
    """
    id: int = 1
    nome_cliente: str = "Maria"
    email_cliente: str = "nome@email.com"
    celular_cliente: str = "11999999999"
    endereco_cliente: str = "Avenida dos Eucaliptos, 815. Moema, São Paulo, SP"
    data_cliente: str = "2024-03-30"
    hora_cliente: str = "12:45"
    servico_cliente: str = "Corte de cabelo"
    mensagem_cliente: str = "Corte de cabelo curto"
    status_agendamento: str = "Aguardando confirmação"
    


class AgendamentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome_cliente: str
    email_cliente: str
    celular_cliente: str
    data_cliente: str
    hora_cliente: str

def apresenta_agendamento(agendamento: Agendamento):
    """ Retorna uma representação do agendamento seguindo o schema definido em
        AgendamentoViewSchema.
    """
    return {
        "id": agendamento.id,
        "nome_cliente": agendamento.nome_cliente,
        "email_cliente": agendamento.email_cliente,
        "celular_cliente": agendamento.celular_cliente,
        "endereco_cliente": agendamento.endereco_cliente,
        "data_cliente": agendamento.data_cliente,
        "hora_cliente": agendamento.hora_cliente,
        "servico_cliente": agendamento.servico_cliente,
        "mensagem_cliente": agendamento.mensagem_cliente,
        "status_agendamento": agendamento.status_agendamento
        }
