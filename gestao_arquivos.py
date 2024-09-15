from pathlib import Path
import json
from unidecode import unidecode 
import glob
import os

# cria pasta de historico no diretorio parent
pasta_historico = Path(__file__).parent / 'mensagens'
pasta_historico.mkdir(exist_ok=True)



    
    
def converte_nome_historico(nome_mensagem):
    nome_arquivo = unidecode(nome_mensagem).lower().replace(" ", "")
    return nome_arquivo

def salva_historico(historico_conversa):
    if len(historico_conversa) == 0:
        return False
    
    nome_mensagem = ''
    for mensagem in historico_conversa:
        if mensagem['role'] == 'user':
            nome_mensagem = mensagem['content'][:30]
            break
        
    nome_arquivo = converte_nome_historico(nome_mensagem)
    
    arquivo = {
        'nome mensagem': nome_mensagem,
        'nome_arquivo':nome_arquivo,
        'mensagem': historico_conversa
    }

    with open(pasta_historico / nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(arquivo, f, ensure_ascii=False, indent=4)
        
def listar_conversas():
    conversas = [os.path.basename(x) for x in glob.glob(str(pasta_historico) + "/*")]
    return conversas

def ler_mensagem_por_nome_arquivo(pasta, nome_arquivo, key='mensagem'):
    with open(pasta / nome_arquivo, 'rb') as f:
        mensagens = json.load(f)
    return mensagens[key]

def deleta_historico(pasta, nome_arquivo):
    os.remove(str(pasta) + '/' + nome_arquivo)
    
    
def renomeia_arquivo(pasta, nome_atual, nome_novo):
    nome_arquivo_atual = str(pasta)+'/'+ nome_atual
    nome_arquivo_novo = str(pasta)+'/'+ nome_novo
    os.rename(nome_arquivo_atual, nome_arquivo_novo)