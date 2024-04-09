import requests
from datetime import datetime

def clima():
    # link do open_weather: https://openweathermap.org/

    API_KEY = "b8f089bf2fa25263137cadf78d409b41"
    cidade = "rio de janeiro"
    link = f"https://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={API_KEY}&lang=pt_br&units=metric"

    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()

    # Na lista fornecida pelo open_weather, a posição 0 é a atual, depois, cada posição é de 3 em 3 horas
    # Portanto, a posição 6 é daqui a 18 horas aproximadamente
    dia = requisicao_dic['list'][6]['dt_txt']
    descricao = requisicao_dic['list'][6]['weather'][0]['description']
    temperatura = requisicao_dic['list'][6]['main']['temp']
    # Formata a temperatura para ter apenas uma casa decimal
    temperatura = "{:.1f}".format(temperatura)

    

    return cidade, dia, descricao, f"{temperatura}ºC"