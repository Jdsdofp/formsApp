import streamlit as st
import pandas as pd
from models import *
import folium
import geopandas as gpd
from folium import Marker, Icon
from folium.plugins import MarkerCluster

# Configuração inicial do Streamlit
st.set_page_config(initial_sidebar_state="collapsed", page_icon="Logo_CoraçãoDrogaria_Globo.ico", layout="wide")
st.subheader("Dashboard")


col1, col2 = st.columns(2)

with col1:
    st.markdown("<h5 style='color: #fa4848'>Dados Gerais</h5>", unsafe_allow_html=True)
    st.write("Contagem de chamados por UF e status:")
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


with col2:
    st.markdown("<h5 style='color: #fa4848'>Mapeamento Filiais  </h5>", unsafe_allow_html=True)
    # Função para obter as filiais
    def filial_get():
        # Substitua esta lógica pela obtenção real dos dados do banco de dados
        filiais = [filial for filial in col_filiais.find({})]
        return filiais

    # Função para criar o mapa
    def create_map(filiais, estados):
        map = folium.Map(location=[-6.6121,-39.2396], zoom_start=4.5)

        # Adicione informações sobre os marcadores
        marker_cluster = MarkerCluster().add_to(map)

        # Determine os estados com filiais dinamicamente
        estados_com_filiais = set(filial['uf'] for filial in filiais)

        for filial in filiais:
            nome_loja = filial.get('nome_loja', '')
            lat = float(filial.get('lat', ''))
            lon = float(filial.get('lon', ''))

            folium.Marker([lat, lon], tiles='Stamen Terrain', popup=nome_loja,
                        icon=Icon(color="red", icon='heart')).add_to(marker_cluster)

        # Adicione limites dos estados ao mapa
        folium.GeoJson(estados, style_function=lambda feature: {
            'fillColor': 'red' if feature['properties']['UF'] in estados_com_filiais else 'lightgray',
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5',
            'fillOpacity': 0.5
        }).add_to(map)

        # Exibe o mapa no Streamlit
        folium_static = folium.Figure().add_child(map)
        st.components.v1.html(folium_static._repr_html_(), width=800, height=800)

    # Obtém as coordenadas da cidade desejada
    filiais = filial_get()

    # Carrega os dados geográficos dos estados
    geojson_path = 'Brasil.json'  # Substitua pelo caminho real do seu arquivo GeoJSON
    estados = gpd.read_file(geojson_path)

    # Adiciona um spinner com uma imagem personalizada como ícone
    with st.spinner("Carregando mapa..."):
        # Cria o mapa
        create_map(filiais, estados)
