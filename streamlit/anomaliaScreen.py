import pandas as pd
import streamlit as st
import plotly.express as px
import json
import requests
from urllib.request import urlopen
import numpy as np

@st.cache_data
def carregar_anomalias():
    return pd.read_csv(
        "../data/df_anomaly_cliente.csv", 
        usecols=['clientCode', 'clientIndex', 'media_gasto', 'desvio_padrao', 'max_gasto', 'min_gasto', 'anomaly']
    )

@st.cache_data
def carregar_consumo():
    return pd.read_csv(
        "../data/novoDataframe.csv", 
        usecols=['clientCode', 'clientIndex', 'gasto', 'datetime']
    )

@st.cache_data
def carregar_cadastro():
    return pd.read_csv(
        "../data/informacao_cadastral.csv", 
        usecols=['clientCode', 'bairro']
    )

@st.cache_data
def carregar_geojson():
    with urlopen('https://raw.githubusercontent.com/fea-dev-usp/IBGE/master/geojson_2022.json') as response:
        return json.load(response)

def grafico_consumo(dados):
    fig = px.line(
        dados, 
        x='datetime', 
        y='gasto', 
        title='Consumo do Cliente ao Longo do Tempo',
        labels={'datetime': 'Tempo', 'gasto': 'Consumo (Gasto)'},
        markers=True
    )
    fig.update_xaxes(title_text='Tempo', tickformat='%d-%m-%Y %H:%M:%S')
    fig.update_yaxes(title_text='Consumo (m³/h)')	
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def randomizar_coordenadas(latitudes, longitudes):
    """Adiciona uma pequena variação aleatória às coordenadas"""
    var_lat = np.random.uniform(-0.001, 0.001, size=latitudes.shape)
    var_lon = np.random.uniform(-0.001, 0.001, size=longitudes.shape)
    return latitudes + var_lat, longitudes + var_lon

def simplificar_geojson(geo_json, tolerancia=0.1):
    from shapely.geometry import shape, mapping
    simplificados = []
    for feature in geo_json['features']:
        geom = shape(feature['geometry'])
        geom_simplificado = geom.simplify(tolerancia, preserve_topology=True)
        simplificados.append({
            'type': 'Feature',
            'geometry': mapping(geom_simplificado),
            'properties': {
                'nome': feature['properties'].get('nome')
            }
        })
    return {'type': 'FeatureCollection', 'features': simplificados}

@st.cache_data
def carregar_simplificado_geojson(tolerancia=0.1):
    geo_json = carregar_geojson()
    if not geo_json:
        st.error("GeoJSON não foi carregado corretamente.")
        return None
    simplificado = simplificar_geojson(geo_json, tolerancia)
    return simplificado

@st.cache_data
def coordenadas_bairros(bairros):
    coords = {}
    for bairro in bairros:
        if not isinstance(bairro, str) or bairro.strip().lower() == 'nan' or bairro.strip() == '':
            st.warning(f"Ignorando bairro inválido ou vazio: '{bairro}'")
            continue
        query = f"{bairro}"
        url = "https://photon.komoot.io/api/"
        params = {
            'q': 'Porto Alegre, ' + query,
            'limit': 1,
        }
        try:
            resposta = requests.get(url, params=params, timeout=10)
            resposta.raise_for_status()
            dados = resposta.json()
            if dados['features']:
                lon, lat = dados['features'][0]['geometry']['coordinates']
                coords[bairro] = (lat, lon)
            else:
                st.warning(f"Nenhuma coordenada encontrada para o bairro: {bairro}")
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao geocodificar o bairro '{bairro}': {e}")
        except (KeyError, IndexError) as e:
            st.error(f"Erro ao processar a resposta da API para o bairro '{bairro}': {e}")
    return coords

def display():
    dados_anomalias = carregar_anomalias()
    dados_consumo = carregar_consumo()
    cadastro = carregar_cadastro()

    try:
        dados_consumo['datetime'] = pd.to_datetime(dados_consumo['datetime'], errors='coerce', unit='s')
        cadastro['clientCode'] = pd.factorize(cadastro['clientCode'])[0]
    except Exception as e:
        st.error(f"Erro ao converter a coluna 'datetime': {e}")
        return

    dados_consumo = dados_consumo.dropna(subset=['datetime'])
    dados_consumo = dados_consumo.sort_values(by='datetime')

    clientes_anomalias = dados_anomalias[dados_anomalias['anomaly'] == 1][['clientCode', 'clientIndex']].drop_duplicates()

    st.title("DashBoard e Insights de anomalias")

    st.header("Seleção de Cliente Anômalo")
    codigo_cliente = st.selectbox(
        "Selecione o ClientCode",
        options=sorted(clientes_anomalias['clientCode'].unique())
    )

    selected = False
    if codigo_cliente:
        indices_cliente = clientes_anomalias[clientes_anomalias['clientCode'] == codigo_cliente]['clientIndex'].unique()
        if len(indices_cliente) == 1:
            st.sidebar.warning("O clientCode atual só possui um medidor")
            indice_cliente = indices_cliente[0]
        else:
            indice_cliente = st.sidebar.selectbox(
                "Selecione o clientIndex",
                options=sorted(indices_cliente)
            )
        selected = True

    if selected:
        dados_cliente = dados_consumo[
            (dados_consumo["clientCode"] == codigo_cliente) & 
            (dados_consumo["clientIndex"] == indice_cliente)
        ]

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"#### Gráfico de Consumo - Cliente {codigo_cliente} (Index: {indice_cliente})")
            if st.button("Gerar Gráfico de Consumo"):
                if not dados_cliente.empty:
                    fig_consumo = grafico_consumo(dados_cliente)
                    st.plotly_chart(fig_consumo, use_container_width=True)
                else:
                    st.warning("Nenhum dado encontrado para o clientIndex selecionado.")

        with col2:
            st.markdown("#### Informações do Cliente")
            try:
                dados_anomalia_cliente = dados_anomalias[
                    (dados_anomalias["clientCode"] == codigo_cliente) & 
                    (dados_anomalias["clientIndex"] == indice_cliente)
                ].iloc[0]
                
                col_a, col_b = st.columns(2)
                col_c, col_d = st.columns(2)

                col_a.metric(label="Máximo de Consumo", value=f"{round(dados_anomalia_cliente['max_gasto'], 2)} m³/h")
                col_b.metric(label="Mínimo de Consumo", value=f"{round(dados_anomalia_cliente['min_gasto'], 2)} m³/h")
                col_c.metric(label="Média de Consumo", value=f"{round(dados_anomalia_cliente['media_gasto'], 2)} m³/h")
                col_d.metric(label="Desvio Padrão", value=f"{round(dados_anomalia_cliente['desvio_padrao'], 2)} m³/h")
            except IndexError:
                st.error("Dados de anomalia do cliente não encontrados.")

    cadastro['clientCode'] = cadastro['clientCode'].astype(str)
    dados_anomalias['clientCode'] = dados_anomalias['clientCode'].astype(str)
    dados_anomalias = dados_anomalias.merge(cadastro, on='clientCode', how='left')

    bairros = dados_anomalias['bairro'].dropna().astype(str).unique()
    coords_bairro = coordenadas_bairros(bairros)

    simplificado_geojson = carregar_simplificado_geojson(tolerancia=0.1)
    if not simplificado_geojson:
        st.error("GeoJSON simplificado não foi carregado corretamente.")
        return

    tamanho_geojson = len(json.dumps(simplificado_geojson)) / (1024 * 1024)
    if tamanho_geojson > 200:
        st.error(f"GeoJSON simplificado é muito grande: {tamanho_geojson:.2f} MB. Tente aumentar a tolerância.")
        return

    dados_anomalias['lat'] = dados_anomalias['bairro'].map(lambda bairro: coords_bairro.get(bairro, (None, None))[0])
    dados_anomalias['lon'] = dados_anomalias['bairro'].map(lambda bairro: coords_bairro.get(bairro, (None, None))[1])

    dados_anomalias = dados_anomalias.dropna(subset=['lat', 'lon'])

    # Para os pontos não ficarem exatamente em cima uns dos outros
    dados_anomalias['lat'], dados_anomalias['lon'] = randomizar_coordenadas(
        dados_anomalias['lat'].values, 
        dados_anomalias['lon'].values
    )

    with st.spinner("Carregando mapa..."):
        @st.cache_data
        def gerar_mapa(dados_anomalias, simplificado_geojson):
            fig = px.choropleth_mapbox(
                data_frame=dados_anomalias,
                geojson=simplificado_geojson,
                locations='bairro',
                featureidkey='properties.nome',
                mapbox_style='carto-positron',
                zoom=10,
                center={"lat": dados_anomalias['lat'].mean(), "lon": dados_anomalias['lon'].mean()},
                opacity=0.5,
                labels={'bairro': 'Bairro'},
                width=1300,
                height=700,
                title='Anomalias por Localidade'
            )

            fig.add_scattermapbox(
                lat=dados_anomalias['lat'],
                lon=dados_anomalias['lon'],
                mode='markers',
                marker=dict(
                    size=dados_anomalias['media_gasto'] / dados_anomalias['media_gasto'].max() * 15 + 5,
                    color=dados_anomalias['media_gasto'],
                    colorscale='YlOrRd',
                    cmin=dados_anomalias['media_gasto'].min(),
                    cmax=dados_anomalias['media_gasto'].max(),
                    showscale=True,
                    colorbar=dict(
                        title="Consumo Médio (m³/h)",
                        titleside="top",
                        tickmode="array",
                        ticks="outside",
                        x=-0.25,
                        y=0.5,
                        len=1,
                        thickness=15
                    ),
                    opacity=0.8
                ),
                
                text=dados_anomalias.apply(lambda row: f"Cliente: {row['clientCode']}<br>Média de Gasto: {row['media_gasto']}<br>Desvio Padrão: {row['desvio_padrao']}", axis=1),
                hoverinfo='text',
                name="Anomalias"
            )

            return fig
        
    mapa_anomalias = gerar_mapa(dados_anomalias, simplificado_geojson)

    st.markdown("---")
    st.title("Mapa de Anomalias")
    st.plotly_chart(mapa_anomalias, use_container_width=True)

    # adiciona métricas gerais de anomalias
    st.markdown("---")
    st.header("Métricas Gerais de Anomalias")

    col1, col2 = st.columns(2)

    with col1:
        col1.metric(label="Total de Clientes", value=f"{dados_consumo['clientCode'].nunique()}")
        col1.metric(label="Quantidade de clientes Anômalos", value=f"{dados_anomalias[dados_anomalias['anomaly'] == 1]['clientCode'].count()}")

    with col2:
        total_clientes = dados_consumo['clientCode'].nunique()
        total_clientes_anomalicos = dados_anomalias[dados_anomalias['anomaly'] == 1]['clientCode'].nunique()
        porcentagem_anomalicos = (total_clientes_anomalicos / total_clientes) * 100

        col2.metric(label="Porcentagem de Clientes Anômalos", value=f"{porcentagem_anomalicos:.2f}%")
        
        col2.metric(label="Bairro com mais anomalias", value=dados_anomalias['bairro'].value_counts().idxmax())