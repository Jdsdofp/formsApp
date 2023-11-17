import streamlit as st
import pandas as pd
from models import *


def obter_contagem_por_uf():
    chamados = [chamado for chamado in col_solicitacao.find()]
    lojas = [loja for loja in col_filiais.find()]
    nomes_lojas_uf_dict = {loja['nome_loja']: loja['uf'] for loja in lojas}

    contagem_por_uf = {uf: {'aberto': 0, 'fechado': 0, 'finalizada': 0} for uf in nomes_lojas_uf_dict.values()}

    for chamado in chamados:
        nome_loja_chamado = chamado.get('loja', '')
        uf_loja = nomes_lojas_uf_dict.get(nome_loja_chamado, 'UF não encontrada')
        status_chamado = chamado.get('status', '').lower()

        if status_chamado in contagem_por_uf[uf_loja]:
            contagem_por_uf[uf_loja][status_chamado] += 1

    df_contagem = pd.DataFrame.from_dict(contagem_por_uf, orient='index')
    df_contagem.loc['Total'] = df_contagem.sum()

    return df_contagem

df_contagem = obter_contagem_por_uf()

# Adiciona cor ao cabeçalho usando o estilo do Streamlit
st.dataframe(df_contagem.style.apply(lambda x: ['background: #f2f2f2' for i in x], axis=1, subset=pd.IndexSlice[:, :]))
