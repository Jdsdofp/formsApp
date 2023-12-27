import streamlit as st
import pandas as pd
from st_aggrid import *
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_local_storage import LocalStorage
from models import *
import datetime
import time
from config import *


st.set_page_config(initial_sidebar_state="collapsed",page_icon="Logo_CoraçãoDrogaria_Globo.ico",layout="wide")


scs_db=[documento for documento in col_solicitacao.find({'status': {'$in': ['aberto', 'fechado']}})]


st.subheader("📝 Atendimentos")

def LocalStorageManager():
    return LocalStorage()

localS = LocalStorageManager()


if scs_db:
    df = pd.DataFrame(scs_db).sort_values(by='status')
    # Adicione uma coluna com ícones condicionais
    def row_icons(row):
        if row["status"] == "aberto":
            return pd.Series("🔴", index=["#"])
        else:
            return pd.Series("", index=["#"])

    df["#"] = df.apply(row_icons, axis=1)



    df = df.rename(columns={
        'solicitante': 'Solicitante',
        'cod_loja': 'Código da Loja',
        'loja': 'Loja',
        'desc_servico': 'Descrição Serviço',
        'data_abertura': 'Data de Abertura',
        'data_solicitacao': 'Data de Solicitação',
        'tp_urg': 'Tipo de Urgência',
        'nr_chamado': 'Número do Chamado',
        'oc': 'OC',
        'status': 'Status',
        'nr_solicitacao': 'Nº Solicitação',
    })

    # Remover colunas indesejadas
    colunas_para_remover = ['_id', 'gr_complexidade', 'forncedor','Solicitante', 'NF']
    #df['class_servico'] = df['class_servico'].apply(lambda x: str(x).strip("[]"))
    df = df.drop(colunas_para_remover, axis=1)
    cols = list(df.columns)
    cols.insert(0, cols.pop(cols.index('cod_registro')))
    df = df[cols]

    ordem_colunas = [
        "Código da Loja",
        "Loja",
        "arquivo_1",
        "arquivo_2",
        "class_servico",
        "Data de Abertura",
        "Data de Solicitação",
        "Descrição Serviço",
        "Tipo de Urgência",
        "Número do Chamado",
        "Nº Solicitação",
        "OC",
        "vlr_oc",
        "Status",
        "atendente",
        "data_atendimento",
        "imagem_1",
        "imagem_2",
        "imagem_3",
        "imagem_4"
        # Adicione outras colunas conforme necessário
    ]

    df = df[["#"] + ordem_colunas + ["cod_registro"]]
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column("#", pinned="left")
    gb.configure_column("cod_registro", pinned="left")
    gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="single", use_checkbox=False)
    gb.configure_side_bar()
    gb.configure_pagination("pagination")
    gridoptions = gb.build()

    
    custom_css = {
        "#gridToolBar": {
        "padding-bottom": "0px !important",
        },
        ".ag-root.ag-unselectable.ag-layout-normal": {"font-size": "13px !important",
        "font-family": "Roboto, sans-serif !important;"},
        ".ag-header-cell-text": {"color": "#495057 !important;"},
        ".ag-theme-alpine .ag-ltr .ag-cell": {"color": "#444 !important;"},
        ".ag-theme-alpine .ag-row-odd": {"background": "rgba(243, 247, 249, 0.3) !important;",
        "border": "1px solid #eee !important;"},
        ".ag-theme-alpine .ag-row-even": {"border-bottom": "1px solid #eee !important;"},
        ".ag-theme-light button": {"font-size": "0 !important;", "width": "auto !important;", "height": "24px !important;",
        "border": "1px solid #eee !important;", "margin": "4px 2px !important;",
        "background": "#3162bd !important;", "color": "#fff !important;",
        "border-radius": "3px !important;"},
        ".ag-theme-light button:before": {"content": "'Confirm' !important","position": "relative !important",
        "z-index": "1000 !important", "top": "0 !important",
        "font-size": "12px !important", "left": "0 !important",
        "padding": "4px !important"
        },
    }

  


    response = AgGrid(
        df,
        reload_data=True,
        height=500,
        gridOptions=gridoptions,
        custom_css=custom_css,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
        header_checkbox_selection_filtered_only=True,
        use_checkbox=True)


    data_dict=response["selected_rows"]  
         # Imprimindo os resultados


    
    
else:
    df = pd.DataFrame(columns=[
        'Solicitante',
        'Código da Loja',
        'Loja',
        'Data de Abertura',
        'Data de Solicitação',
        'Fornecedor',
        'Tipo de Urgência',
        'Grau de Complexidade',
        'Número do Chamado',
        'OC',
        'Status',
        'Descrição Serviço'
    ])

lS = localS.getItem("atend", key="get_item")
urs = lS.get("storage", {}) if lS is not None else {}

usr = urs.get("value") if isinstance(urs, dict) else ""
data_atual = datetime.datetime.now(fuso_horario)
data_formatada = data_atual.strftime("%d/%m/%Y %H:%M:%S")



if 'data_dict' in locals():
    if usr:
        atnd = st.text_input("Atendente: ", key="atendente_key", value=str(usr).upper(), disabled=True)
        salvar_checkbox = st.checkbox(" ", disabled=True)
    else:
        atnd = st.text_input("Atendente: ", key="atendente_key", placeholder="Atendente")
        salvar_checkbox = st.checkbox("Salvar nome atendente")

            
    if salvar_checkbox:
                # Adiciona o valor ao local storage quando o checkbox é marcado
        localS.setItem("atend", atnd)
    if len(data_dict) > 0:
            with st.form(key="submitted"):
                col1, col2 = st.columns(2)
                with col1:
                    
                    


                    cd_rgs=col1.text_input(label="Cod. Registro", disabled=True,value=data_dict[0]['cod_registro'])
                    stts_txt=col1.text_input(label="Status: ", disabled=True,value=data_dict[0]['Status'])
                    
                    if data_dict[0]['Status'] == 'fechado':
                        stts=col1.selectbox(label="Fechamento: ", options=["finalizada"])
                    elif data_dict[0]['Status'] == 'finalizada':
                         stts=col1.selectbox(label="Fechamento: ", disabled=True,options=["-"])
                    else:
                         stts=col1.selectbox(label="Fechamento: ", options=["fechado"])
                    
                    if len(data_dict[0]['arquivo_1']) and len(data_dict[0]['arquivo_2']):
                        col1.markdown(f"<a href='{data_dict[0]['arquivo_1']}' style='border: 1px #777 solid; background: #F36B6B; color: white; padding: 6px; font-size: 13px; border-radius: 20px'>Arquivo📥 1</a>", unsafe_allow_html=True)
                        col1.markdown(f"<a href='{data_dict[0]['arquivo_2']}' style='border: 1px #777 solid; background: #F36B6B; color: white; padding: 6px; font-size: 13px; border-radius: 20px'>Arquivo📥 2</a>", unsafe_allow_html=True)
                    elif len(data_dict[0]['arquivo_1']):
                         col1.markdown(f"<a href='{data_dict[0]['arquivo_1']}' style='outline: none; border: 1px #777 solid; background: #F36B6B; color: white; padding: 6px; font-size: 13px; border-radius: 20px'>Arquivo📥 1</a>", unsafe_allow_html=True)
                    else:
                         pass
                    
                    if len(data_dict[0]['imagem_1']):
                        col1.markdown(f"<a href='{data_dict[0]['imagem_1']}' style='border: 1px #777 solid; background: #F36B6B; color: white; padding: 6px; font-size: 13px; border-radius: 20px'>Imagem 📥 1</a>", unsafe_allow_html=True)  
                    if len(data_dict[0]['imagem_2']):
                        col1.markdown(f"<a href='{data_dict[0]['imagem_2']}' style='border: 1px #777 solid; background: #F36B6B; color: white; padding: 6px; font-size: 13px; border-radius: 20px'>Imagem 📥 2</a>", unsafe_allow_html=True)
                    if len(data_dict[0]['imagem_3']):
                        col1.markdown(f"<a href='{data_dict[0]['imagem_3']}' style='border: 1px #777 solid; background: #F36B6B; color: white; padding: 6px; font-size: 13px; border-radius: 20px'>Imagem 📥 3</a>", unsafe_allow_html=True)
                    if len(data_dict[0]['imagem_4']):
                        col1.markdown(f"<a href='{data_dict[0]['imagem_3']}' style='border: 1px #777 solid; background: #F36B6B; color: white; padding: 6px; font-size: 13px; border-radius: 20px'>Imagem 📥 4</a>", unsafe_allow_html=True)
                    else:
                         pass



                with col2:
                    nr_cmd=col2.text_input("Nº Chamado: ", disabled=True,value=data_dict[0]['Número do Chamado'])
                    

                    if data_dict[0]['Nº Solicitação']:
                        nr_solic=col2.text_input("Nº Solicitação: ", disabled=True, value=data_dict[0]['Nº Solicitação'])
                    else:
                        nr_solic=col2.text_input("Nº Solicitação: ")
                    


                    if data_dict[0]['Status'] == 'aberto':
                         nr_oc=col2.number_input("Nº OC: ", disabled=True)
                    elif data_dict[0]['Status'] == 'finalizada':
                         nr_oc=col2.number_input("Nº OC: ", data_dict[0]['OC'],  disabled=True)
                    else:
                         nr_oc=col2.number_input("Nº OC: ",step=0)

                    

                submitted = st.form_submit_button(label="Lançar :heavy_check_mark:", type="primary", use_container_width=True)

            if submitted:
                filterID = int(cd_rgs)

            
            
                filter_criteria={'cod_registro': filterID}
                
                new_oc=int(nr_oc)
                nr_slc=int(nr_solic)
                new_atnd=str(atnd)
                new_stts=str(stts)
                new_data_atendimento=data_formatada

                oc=col_solicitacao.find_one({"cod_registro": filterID})
                if oc["nr_solicitacao"] == 0:
                    new_values={'$set':{'nr_solicitacao': nr_slc,'status': new_stts, 'oc': new_oc, 'atendente': new_atnd, 'data_atendimento': new_data_atendimento}}
                    resultUpdate=col_solicitacao.update_one(filter_criteria, new_values)
                else:
                    new_values={'$set':{'nr_solicitacao': nr_slc,'status': new_stts, 'oc': new_oc}}
                    resultUpdate=col_solicitacao.update_one(filter_criteria, new_values)

                if resultUpdate:
                    st.info(f"Status de registro fechado com sucesso")
                    

    else:
            
        with st.form(key="submitted",clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    cd_rgs=col1.text_input(label="Cod. Registro", disabled=True, value="")
                    stts_txt=col1.text_input(label="Status: ", disabled=True, value="")
                    stts=col1.selectbox(label="Fechamento: ", disabled=True, options=[""])
                
                with col2:
                    nr_cmd=col2.text_input("Nº Chamado: ", disabled=True, value="")
                    nr_solic=col2.text_input("Nº Solicitação:", disabled=True)

                submitted = st.form_submit_button(label="Lançar :heavy_check_mark:", type="primary", use_container_width=True, disabled=True)

else:
    pass