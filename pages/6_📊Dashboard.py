import streamlit as st
import pandas as pd
from models import *
import plotly.express as px
import folium
import geopandas as gpd
from folium import Marker, Icon
from folium.plugins import MarkerCluster
import locale

# Configurar a formatação para o padrão brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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


  
    dados = col_solicitacao.find()

    somatoria_por_categoria = {}

    for documento in dados:
        categoria = documento.get('gr_complexidade', 'Outros')
        if not categoria:
            categoria = 'Outros'
        valor_oc_raw = documento.get('vlr_oc', 0)
        valor_oc_str_clean = ''.join(char for char in str(valor_oc_raw) if char.isdigit() or char in {',', '.'})
        valor_oc = float(valor_oc_str_clean.replace(',', '.')) if valor_oc_str_clean else 0

        if categoria not in somatoria_por_categoria:
            somatoria_por_categoria[categoria] = {'total': 0}
        somatoria_por_categoria[categoria]['total'] += valor_oc

    # Ordenar o dicionário por valores de forma crescente
    somatoria_por_categoria_ordenado = dict(sorted(somatoria_por_categoria.items(), key=lambda item: item[1]['total']))

    # Criar DataFrame
    df = pd.DataFrame(list(somatoria_por_categoria_ordenado.items()), columns=['Categoria', 'Valor Total'])

    # Formatar a coluna "Valor Total" como somas numéricas
    df['Valor Total'] = df['Valor Total'].apply(lambda x: x['total'])

    # Criar gráfico de barras com Plotly Express, incluindo rótulos de dados
    fig = px.bar(df, x='Categoria', y='Valor Total', text='Valor Total', title='Custo por Categoria')

    # Formatar o eixo y em formato de moeda brasileira (R$)
    fig.update_layout(
        yaxis_tickprefix='R$', 
        yaxis_tickformat=',.2f', 
        yaxis_title='Valor Total (R$)'
    )

    # Exibir gráfico no Streamlit
    col1.plotly_chart(fig)


    dds = col_solicitacao.find()
    somatoria_por_servico = {}
    for documento in dds:
        
        for servico in documento.get('class_servico', []):
            valor_oc_raw = documento.get('vlr_oc', 0)
            valor_oc_str_clean = ''.join(char for char in str(valor_oc_raw) if char.isdigit() or char in {',', '.'})
            valor_oc = float(valor_oc_str_clean.replace(',', '.')) if valor_oc_str_clean else 0

            if servico not in somatoria_por_servico:
                somatoria_por_servico[servico] = {'total': 0}
            somatoria_por_servico[servico]['total'] += valor_oc

    # Criar DataFrame
    df_servico = pd.DataFrame(list(somatoria_por_servico.items()), columns=['Classe de Serviço', 'Valor Total'])
    df_servico['Valor Total'] = df_servico['Valor Total'].apply(lambda x: x['total'])
    # Antes de criar o gráfico

    # Criar gráfico de pizza com Plotly Express
    fig = px.pie(df_servico, values='Valor Total', names='Classe de Serviço', title='Percentual por Classe de Serviço')

    # Exibir gráfico de pizza no Streamlit
    st.plotly_chart(fig)

    

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

    dds1 = col_solicitacao.find()
    valor_por_servico = {}

    for documento in dds1:
        for servico in documento.get('class_servico', []):
            valor_oc_raw = documento.get('vlr_oc', 0)
            valor_oc_str_clean = ''.join(char for char in str(valor_oc_raw) if char.isdigit() or char in {',', '.'})
            valor_oc = float(valor_oc_str_clean.replace(',', '.')) if valor_oc_str_clean else 0

            if servico not in valor_por_servico:
                valor_por_servico[servico] = {'total': 0}
            valor_por_servico[servico]['total'] += valor_oc

    # Criar DataFrame
    df_servico = pd.DataFrame(list(valor_por_servico.items()), columns=['Classe de Serviço', 'Valor Total'])
    df_servico['Valor Total'] = df_servico['Valor Total'].apply(lambda x: x['total'])

    # Ordenar o DataFrame por Valor Total
    df_servico = df_servico.sort_values(by='Valor Total', ascending=True)

    # Criar gráfico de barras com Plotly Express
    fig = px.bar(df_servico, x='Classe de Serviço', y='Valor Total', title='Somatória por Classe de Serviço')

    # Adicionar rótulos de dados aos valores nas barras
    fig.update_traces(texttemplate='%{y:,.2f}', textposition='outside')  # Adiciona a formatação de moeda BR

    # Exibir gráfico de barras no Streamlit
    col2.plotly_chart(fig)


    # Recuperar os dados do MongoDB
    data = list(col_solicitacao.find())

    # Criar DataFrame com os dados
    df = pd.DataFrame(data)

    # Converter a coluna 'data_abertura' para o formato datetime
    df['data_abertura'] = pd.to_datetime(df['data_abertura'], format='%d/%m/%Y %H:%M:%S')

    # Criar colunas 'dia_do_mes' e 'mes'
    df['dia_do_mes'] = df['data_abertura'].dt.day
    df['mes'] = df['data_abertura'].dt.month

    # Filtro por mês e dia do mês
    selected_month = col2.selectbox("Selecione o mês", range(1, 13))
    selected_days = col2.slider("Selecione o intervalo de dias do mês", 1, 31, (1, 31))

    # Filtrar os dados com base no mês e no intervalo de dias selecionados
    filtered_df = df[(df['mes'] == selected_month) & 
                    (df['dia_do_mes'] >= selected_days[0]) & 
                    (df['dia_do_mes'] <= selected_days[1])]

    # Agrupar por dia e contar o número de registros
    counts_per_day = filtered_df.groupby('dia_do_mes').size().reset_index(name='counts')

    # Encontrar o ponto mais alto
    max_point = counts_per_day.loc[counts_per_day['counts'].idxmax()]

    # Criar o gráfico Plotly Express
    fig = px.line(counts_per_day, x='dia_do_mes', y='counts', markers=True, line_shape='linear', title='Registros por Dia',
                labels={'dia_do_mes': 'Dia do Mês', 'counts': 'Número de Registros'})

    # Adicionar rótulo de dados no ponto mais alto
    fig.add_annotation(x=max_point['dia_do_mes'], y=max_point['counts'], text=f'Máximo: {max_point["counts"]}', showarrow=True,
                    arrowhead=1, ax=0, ay=-40)

    # Exibir gráfico no Streamlit
    col2.plotly_chart(fig)
