import datetime
from time import time
import requests
import streamlit as st
import pandas as pd
import streamlit_option_menu
from streamlit_option_menu import option_menu
import streamlit_nested_layout
from streamlit_extras.card import card
from streamlit_extras.metric_cards import style_metric_cards
import holidays

from xgboost import XGBRegressor

import joblib

# Função para carregar os dados com cache
@st.cache_data
def load_data():
    try:
        df_cluster = pd.read_csv("../data/df_cluster.csv")
        return df_cluster
    except FileNotFoundError:
        st.error("Arquivo não encontrado. Verifique se o caminho está correto.")
        return pd.DataFrame()  # Retorna um dataframe vazio para evitar falhas.

def display():
    # Carregar os dados
    df_cluster = load_data()

    # Verificar se o DataFrame está vazio
    if df_cluster.empty:
        st.stop()

    # Título
    st.title("Dashboard previsão de consumo")

    # Subtítulo
    st.subheader("Cliente:")

    # Selecione o código do cliente
    clientcode = st.selectbox("Selecione o Codigo do Cliente:", df_cluster["clientCode"].unique())

    # Seleciona o clientIndex com base no clientcode
    clientIndex_options = df_cluster[df_cluster["clientCode"] == clientcode]["clientIndex"].unique()
    if len(clientIndex_options) == 1:
        st.write(f"Index único encontrado: {clientIndex_options[0]}")
        clientIndex = clientIndex_options[0]
    else:
        clientIndex = st.selectbox("Selecione o Index do Cliente:", clientIndex_options)

    # Filtrar dados do cliente
    df_client = df_cluster[(df_cluster["clientCode"] == clientcode) & (df_cluster["clientIndex"] == clientIndex)]

    st.write("---")

    # Subtítulo
    st.subheader("Resumo do consumo")

    labelCluster = ["Alto Consumo", "Consumo Baixíssimo", "Baixo Consumo", "Consumo Volátil", "Consumo Médio"]

    # Coluns
    col1, col2, col3 = st.columns(3)
    col1.metric("Consumo Medio diario", str(round(df_client['gasto'].mean(), 3)) + ' m³')
    col2.metric("Consumo Total", str(round(df_client['gasto'].sum(), 3)) + ' m³')
    col3.metric("Cluster", labelCluster[df_client['cluster'].values[0]])

    # Subtítulo
    st.subheader("Previsão de consumo")
    
    # loading
    with st.spinner("Prevendo consumo dos proximos 7 dias..."):
        df = data_to_predict(df_client)

        if df_client['cluster'].values[0] == 0:
            model = joblib.load("../notebooks/xgb_regressor_model0.pkl")
        elif df_client['cluster'].values[0] == 1:
            model = joblib.load("../notebooks/xgb_regressor_model1.pkl")
        elif df_client['cluster'].values[0] == 2:
            model = joblib.load("../notebooks/xgb_regressor_model2.pkl")
        elif df_client['cluster'].values[0] == 3:
            model = joblib.load("../notebooks/xgb_regressor_model3.pkl")
        elif df_client['cluster'].values[0] == 4:
            model = joblib.load("../notebooks/xgb_regressor_model4.pkl")


        # Prever o consumo
        consumo_previsto = model.predict(df.drop(columns=["data", "date"]))

        # Combine a previsao com as datas
        df["consumo_previsto"] = consumo_previsto

        st.write("Consumo previsto para os próximos 7 dias:")

        # Grafico de consumo previsto
        st.line_chart(df.set_index("data")["consumo_previsto"], x_label="Data", y_label="Consumo Previsto (m³)")

        st.write("Dados previstos para os próximos 7 dias, em m3:")
        # Mostrar a tabela gasto e consumo previsto
        st.table(df[["data", "consumo_previsto"]])

        with st.expander("Dados Usados para a Previsão"):
            st.write("Dados usados para a previsão:")
            st.dataframe(df.drop(columns=["date"]))


    # Subtítulo
    st.subheader("Dados do cliente")

    # Cluster do cliente
    cluster = df_cluster[df_cluster["clientCode"] == clientcode]["cluster"].values[0]

    # Mostrar dados do cliente
    if not df_client.empty:
        with st.expander("Historico de consumo"): 
            tab1, tab2 = st.tabs(["Graficos", "Tabela"])
            with tab1:
                st.write("Gráfico de consumo:")
                st.line_chart(df_client.set_index("date")["gasto"], x_label="Data", y_label="Gasto", )
            with tab2:
                st.write("Tabela do cliente:")
                st.dataframe(df_client)
    else:
        st.warning("Nenhum dado encontrado para este cliente.")

def get_temp_data():
    # request data from API https://my.meteoblue.com/packages/trend-day?apikey=swAlCvekzJX9SByD&lat=-29.9422&lon=-50.9928&asl=41&format=json&windspeed=ms-1&forecast_days=7
    data = {
        "apikey": "swAlCvekzJX9SByD",
        "lat": -29.9422,
        "lon": -50.9928,
        "asl": 41,
        "format": "json",
        "windspeed": "ms-1",
        "forecast_days": 7
    }

    # get
    response = requests.get("https://my.meteoblue.com/packages/trend-day", params=data, )
    #response.raise_for_status()
    if response.status_code != 200:
        st.error(f"Erro ao acessar a API: {response.status_code}")
        return None
    return transformar_json(response.json())
    
def transformar_json(json_original):
    resultado = []
       
     
    for i in range(len(json_original['trend_day']['time'])):
        dia = {
            "data": json_original['trend_day']['time'][i][:10],  # Pega apenas a data no formato YYYY-MM-DD
            "Temp. Ins. (C)": json_original['trend_day']['temperature_mean'][i],
            "Temp. Max. (C)": json_original['trend_day']['temperature_max'][i],
            "Temp. Min. (C)": json_original['trend_day']['temperature_min'][i],
            "Umi. Ins. (%)": json_original['trend_day']['relativehumidity_max'][i] + json_original['trend_day']['relativehumidity_min'][i] / 2,
            "Umi. Max. (%)": json_original['trend_day']['relativehumidity_max'][i],
            "Umi. Min. (%)": json_original['trend_day']['relativehumidity_min'][i],
            "Pto Orvalho Ins. (C)": json_original['trend_day']['temperature_mean'][i],
            "Pto Orvalho Max. (C)": json_original['trend_day']['temperature_max'][i],
            "Pto Orvalho Min. (C)": json_original['trend_day']['temperature_min'][i],
            "Pressao Ins. (hPa)": json_original['trend_day']['sealevelpressure_mean'][i],
            "Pressao Max. (hPa)": json_original['trend_day']['sealevelpressure_max'][i],
            "Pressao Min. (hPa)": json_original['trend_day']['sealevelpressure_min'][i],
            "Vel. Vento (m/s)": json_original['trend_day']['windspeed_mean'][i],
            "Dir. Vento (°)": json_original['trend_day']['winddirection'][i],
            "Raj. Vento (m/s)": json_original['trend_day']['windspeed_mean'][i],
            "Chuva (mm)": json_original['trend_day']['precipitation'][i],
        }
        resultado.append(dia)

    # Ordenar a lista de dicionários por data
    resultado = sorted(resultado, key=lambda x: x["data"])
    
    return resultado

def get_ipca_data():
    url = "https://apisidra.ibge.gov.br/values/t/7060/n1/1/v/63,69,2265,66/c315/7169,7170,7445,7486,7558,7625,7660,7712,7766,7786/p/last"
    response = requests.get(url)
    return extrair_variacao_mensal(response.json())

def data_to_predict(df_client):
    temp = get_temp_data()
    ipca = get_ipca_data()
    
    df_temp = pd.DataFrame(temp)
    df_temp['mes'] = pd.to_datetime(df_temp['data']).dt.month
    print(df_temp)

    df_ipca = pd.DataFrame(ipca, index=[0])
    df_ipca['mes'] = pd.to_datetime(df_ipca['date']).dt.month
    print(df_ipca)

    df = pd.merge(df_temp, df_ipca, on='mes', how='left')

    df['bairro'] = df_client['bairro'].values[0]
    df['categoria'] = df_client['categoria'].values[0]
    df['IG1K-L-v2'] = df_client['IG1K-L-v2'].values[0]
    df['Infinity V2'] = df_client['Infinity V2'].values[0]
    df['inputType'] = df_client['inputType'].values[0]
    df['cluster'] = df_client['cluster'].values[0]
    
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    df['feriado'] = df['date'].dt.date.apply(lambda x: 1 if x in holidays.Brazil() else 0)
    df['dia_da_semana'] = df['date'].dt.weekday
    df['mes'] = df['date'].dt.month
    df['clientCode'] = df_client['clientCode'].values[0]
    df['clientIndex'] = df_client['clientIndex'].values[0]

    # Ordenar as colunas, nessa ordem ['clientCode', 'clientIndex', 'date', 'gasto', 'hora', 'dia_da_semana', 'mes', 'bairro', 'categoria', 'IG1K-L-v2', 'Infinity V2', 'inputType','medidor', 'gasto_por_hora', 'feriado', 'Temp. Ins. (C)','Temp. Max. (C)', 'Temp. Min. (C)', 'Umi. Ins. (%)', 'Umi. Max. (%)','Umi. Min. (%)', 'Pto Orvalho Ins. (C)', 'Pto Orvalho Max. (C)','Pto Orvalho Min. (C)', 'Pressao Ins. (hPa)', 'Pressao Max. (hPa)','Pressao Min. (hPa)', 'Vel. Vento (m/s)', 'Dir. Vento (°)','Raj. Vento (m/s)', 'Chuva (mm)', 'alimentacao/bebidas', '2.Habitação','artigo-de-residencia', '4.Vestuário', 'transportes', 'saude/cuidados','despesas-pessoais', 'educacao', 'comunicacao', 'indice-geral','cluster']
    df = df[['clientCode', 'clientIndex', 'date', 'data', 'dia_da_semana', 'mes', 'bairro', 'categoria', 'IG1K-L-v2', 'Infinity V2', 'inputType', 'feriado', 'Temp. Ins. (C)','Temp. Max. (C)', 'Temp. Min. (C)', 'Umi. Ins. (%)', 'Umi. Max. (%)','Umi. Min. (%)', 'Pto Orvalho Ins. (C)', 'Pto Orvalho Max. (C)','Pto Orvalho Min. (C)', 'Pressao Ins. (hPa)', 'Pressao Max. (hPa)','Pressao Min. (hPa)', 'Vel. Vento (m/s)', 'Dir. Vento (°)','Raj. Vento (m/s)', 'Chuva (mm)', 'alimentacao/bebidas', '2.Habitação','artigo-de-residencia', '4.Vestuário', 'transportes', 'saude/cuidados','despesas-pessoais', 'educacao', 'comunicacao', 'indice-geral','cluster']]

    print(df)
    return df

def extrair_variacao_mensal(dados):
    # Dicionário para armazenar os resultados com o mês incluído
    variacao_mensal = {"date": datetime.datetime.now().strftime("%Y-%m-%d")}

    # Iterando sobre os dados
    for item in dados:
        if item['D2C'] == "63":  # Código para variação mensal
            variacao_mensal[item['D3N']] = float(item['V'])

    # '1.Alimentação e bebidas', '2.Habitação', '3.Artigos de residência', '4.Vestuário', '5.Transportes', '6.Saúde e cuidados pessoais', '7.Despesas pessoais', '8.Educação', '9.Comunicação', 'Índice geral'
    variacao_mensal = {k: variacao_mensal[k] for k in ['date','1.Alimentação e bebidas', '2.Habitação', '3.Artigos de residência', '4.Vestuário', '5.Transportes', '6.Saúde e cuidados pessoais', '7.Despesas pessoais', '8.Educação', '9.Comunicação', 'Índice geral']}

    # Renoemar as chaves
    variacao_mensal = {
        "date": variacao_mensal["date"],
        "alimentacao/bebidas": variacao_mensal["1.Alimentação e bebidas"],
        "2.Habitação": variacao_mensal["2.Habitação"],
        "artigo-de-residencia": variacao_mensal["3.Artigos de residência"],
        "4.Vestuário": variacao_mensal["4.Vestuário"],
        "transportes": variacao_mensal["5.Transportes"],
        "saude/cuidados": variacao_mensal["6.Saúde e cuidados pessoais"],
        "despesas-pessoais": variacao_mensal["7.Despesas pessoais"],
        "educacao": variacao_mensal["8.Educação"],
        "comunicacao": variacao_mensal["9.Comunicação"],
        "indice-geral": variacao_mensal["Índice geral"]
    }

    print(variacao_mensal)
    return variacao_mensal