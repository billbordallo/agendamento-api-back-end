from sqlalchemy import Column, String, Integer, UniqueConstraint

from model import Base


class Agendamento(Base):
    __tablename__ = 'agendamentos'

    id = Column("pk_id_agendamento", Integer, primary_key=True)
    nome_cliente = Column(String(300), unique=False)
    email_cliente = Column(String(300), unique=False)
    celular_cliente = Column(String(300), unique=False)
    endereco_cliente = Column(String(500), unique=False)
    data_cliente = Column(String(10), unique=False)
    hora_cliente = Column(String(5), unique=False)
    servico_cliente = Column(String(300), unique=False)
    mensagem_cliente = Column(String(500), unique=False)
    status_agendamento = Column(String(100), unique=False)

    # Criando um requisito de unicidade envolvendo uma par de informações
    __table_args__ = (UniqueConstraint("data_cliente", "hora_cliente", name="data_hora_unico"),)

    def __init__(self, nome_cliente:str, email_cliente:str, celular_cliente:str, endereco_cliente:str, data_cliente:str, hora_cliente:str, servico_cliente:str, mensagem_cliente:str, status_agendamento:str):
        """
        Cria um Agendamento com os dados fornecidos.

        Arguments:
            nome_cliente: Nome do cliente
            email_cliente: E-mail do cliente.
            celular_cliente: Celular do cliente
            endereco_cliente: Endereço do cliente
            data_cliente: Data do agendamento
            hora_cliente: Horário do agendamento
            servico_cliente: Serviço solicitado pelo cliente
            mensagem_cliente: Mensagem enviada pelo cliente no ato do agendamento
            status_agendamento: Status do agendamento (agendado, cancelado, etc)
        """
        self.nome_cliente = nome_cliente
        self.email_cliente = email_cliente
        self.celular_cliente = celular_cliente
        self.endereco_cliente = endereco_cliente
        self.servico_cliente = servico_cliente
        self.data_cliente = data_cliente
        self.hora_cliente = hora_cliente
        self.mensagem_cliente = mensagem_cliente
        self.status_agendamento = status_agendamento