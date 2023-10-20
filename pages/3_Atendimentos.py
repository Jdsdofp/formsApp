import streamlit as st
import pandas as pd
from st_aggrid import *
from st_aggrid.grid_options_builder import GridOptionsBuilder
from models import *

st.set_page_config(initial_sidebar_state="collapsed",page_icon="Logo_CoraçãoDrogaria_Globo.ico",layout="wide")

def find_open_sc():
    return [documento for documento in col_solicitacao.find({"status": "aberto"})]

scs_db=find_open_sc()
st.subheader("📝 Atendimentos")

if scs_db:
    df = pd.DataFrame(scs_db)


    df = df.rename(columns={
        'solicitante': 'Solicitante',
        'cod_loja': 'Código da Loja',
        'loja': 'Loja',
        'data_abertura': 'Data de Abertura',
        'data_solicitacao': 'Data de Solicitação',
        'tp_urg': 'Tipo de Urgência',
        'nr_chamado': 'Número do Chamado',
        'status': 'Status',
        'nr_solicitacao': 'Nº Solicitação'
    })

    # Remover colunas indesejadas
    colunas_para_remover = ['_id', 'arquivo_1', 'arquivo_2', 'gr_complexidade', 'forncedor','desc_servico','Solicitante']
    #df['class_servico'] = df['class_servico'].apply(lambda x: str(x).strip("[]"))
    df = df.drop(colunas_para_remover, axis=1)
    cols = list(df.columns)
    cols.insert(0, cols.pop(cols.index('cod_registro')))
    df = df[cols]

 
    gb = GridOptionsBuilder.from_dataframe(df)
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
        'Status','Descrição Serviço'
    ])

if 'data_dict' in locals():
    if len(data_dict) > 0:
            with st.form(key="submitted"):
                col1, col2 = st.columns(2)
                with col1:
                    cd_rgs=col1.text_input(label="Cod. Registro", disabled=True,value=data_dict[0]['cod_registro'])
                    stts_txt=col1.text_input(label="Status: ", disabled=True,value=data_dict[0]['Status'])
                    stts=col1.selectbox(label="Fechamento: ", options=["fechado"])
                
                with col2:
                    nr_cmd=col2.text_input("Nº Chamado: ", disabled=True,value=data_dict[0]['Número do Chamado'])
                    nr_solic=col2.text_input("Nº Solicitação: ")

                submitted = st.form_submit_button(label="Lançar :heavy_check_mark:", type="primary", use_container_width=True)

            if submitted:
                find_open_sc()
                filterID = int(cd_rgs)
                filter_criteria={'cod_registro': filterID}
                
                nr_slc=int(nr_solic)
                new_stts=str(stts)

                new_values={'$set':{'nr_solicitacao': nr_slc,'status': new_stts}}

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
    print("A variável 'data_dict' não está definida.")