import streamlit as st
from gestao_arquivos import *
from open_ai import *


def inicializacao():
    # cria o historico de conversa no session state (se não houver)
    if not 'historico_conversa' in st.session_state:
        st.session_state.historico_conversa = []
    
    if not 'conversa_atual' in st.session_state:
        st.session_state.conversa_atual = ''
        
    if not 'modelo' in st.session_state:
        st.session_state.modelo = 'gpt-4o-mini'

def seleciona_conversa(nome_arquivo):   
    if nome_arquivo == '':
        st.session_state.historico_conversa = []
    else:
        historico_conversa = ler_mensagem_por_nome_arquivo(pasta_historico,nome_arquivo)
        st.session_state['historico_conversa'] = historico_conversa
    st.session_state['conversa_atual'] = nome_arquivo


def tab_conversas(tab):
    tab.button('+ Nova Conversa',
            on_click=seleciona_conversa,
            args=('',),
            use_container_width=True)
    col1,col2 = tab.columns(2)
    col1.button('Rename',
                use_container_width=True)
    col2.button('Delete',
                on_click=deleta_historico,
                args=(pasta_historico,st.session_state['conversa_atual']),
                type='primary',
                use_container_width=True)
    tab.markdown('')
    conversas = listar_conversas()
    for conversa in conversas:
        tab.button(conversa,
               on_click=seleciona_conversa,
               args=(conversa,),
               disabled=conversa==st.session_state['conversa_atual'],
               use_container_width=True)
   
def tab_configuracoes(tab):
    modelo_escolhido = tab.selectbox('Selecione o modelo',
                                     ['gpt-3.5-turbo', 'gpt-4'])
    st.session_state['modelo'] = modelo_escolhido



def pagina_principal():
    
    inicializacao()
    
    # define o historico de conversa como o historico do session state
    historico_conversa = st.session_state['historico_conversa']

    # header da página
    st.header('Colina ChatBot', divider=True)
    st.write('Você está usando a versão ' + st.session_state['modelo'])

    # exibe todas as mensagens do histórico_conversa
    for mensagem in historico_conversa:
        chat = st.chat_message(mensagem['role'])
        chat.markdown(mensagem['content'])
        
    # solicita input de mensagem para usuário    
    input = st.chat_input('Digite sua mensagem')

    # se o usuário digita mensagem
    if input:
        
        # usuário ==============================
        
        nova_mensagem_user = {'role':'user','content':input}
        chat = st.chat_message('user') # define a pessoa do chat
        chat.markdown(input) # exibe a mensagem no chat
        historico_conversa.append(nova_mensagem_user)   # append input no historico
        st.session_state['historico_conversa']= historico_conversa  # atualiza o session state com o historico novo  

        # assistant ==============================
        
        chat = st.chat_message('assistant') # define a pessoa do chat
        resposta_json = gera_resposta(historico_conversa,modelo=st.session_state['modelo'])   # puxa a função de resposta
        resposta_texto = resposta_json.choices[0].message.content   # puxa apenas o texto de resposta no return da função
        nova_mensagem_assistant = {'role':'assistant','content':resposta_texto} # cria o novo dict com a mensagem do assistant
        historico_conversa.append(nova_mensagem_assistant)  # append resposta no historico
        chat.markdown(resposta_texto)   # exibe resposta no chat
        st.session_state['historico_conversa']= historico_conversa  # atualiza session state com historico novo
        
        # backend ==============================
        
        st.session_state['historico_conversa'] = historico_conversa
        salva_historico(historico_conversa)



if __name__ == '__main__':
    pagina_principal()
    tab1, tab2 = st.sidebar.tabs(['Conversas','Configurações'])
    tab_conversas(tab1)
    tab_configuracoes(tab2)
    