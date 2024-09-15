import openai
from secrets_openai import *

openai_key = get_secret()
client = openai.Client(api_key=openai_key)

def gera_resposta(historico_conversa, modelo='gpt-3.5-turbo', temperatura=0, max_tokens=1000, stream=False):
    resposta = client.chat.completions.create(
        messages=historico_conversa,
        model=modelo,
        max_tokens=max_tokens,
        temperature=temperatura
    )
    return resposta