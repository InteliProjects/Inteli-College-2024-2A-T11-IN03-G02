from time import time
import streamlit as st
import pandas as pd
import streamlit_option_menu
from streamlit_option_menu import option_menu
import streamlit_nested_layout
from streamlit_extras.card import card
from streamlit_extras.metric_cards import style_metric_cards

def display_doc_page():
    st.markdown("# Inteli - Instituto de Tecnologia e Liderança", unsafe_allow_html=True)
    
    st.image("../assets/inteli.png")
    st.markdown("""
    <p align="center">
    <a href= "https://www.inteli.edu.br/">
    </a>
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    # Modelo Preditivo de Gás - COMPASS 

    ## GasBusters
    """, unsafe_allow_html=True)
    st.image("../streamlit/assets/logoGas-removebg-preview.png", caption="Logo da Equipe")


    st.markdown("""
    ## Integrantes: 
    - <a href="https://www.linkedin.com/in/giacomo-zema-matizonkas-7ab9072b2/">Giacomo Zema </a>
    - <a href="https://www.linkedin.com/in/heitorfariacandido/">Heitor Cândido </a>
    - <a href="https://www.linkedin.com/in/ian-pereira-simao/">Ian Simão </a> 
    - <a href="https://www.linkedin.com/in/iisabelledantas/">Isabelle Dantas</a> 
    - <a href="https://www.linkedin.com/in/marianadepaulabarbosa/">Mariana de Paula </a>
    - <a href="https://www.linkedin.com/in/matheusfgs/">Matheus Fernandes </a> 
    - <a href="https://www.linkedin.com/in/rafaela-s-o-lima/">Rafaela Silva</a> """, unsafe_allow_html=True)

    st.markdown("""
    ## Professores:
    ### Orientador(a) 
    - <a href="https://www.linkedin.com/in/claudio-andr%C3%A9-64911a1b5/">Claudio André</a>
    ### Instrutores
    - <a href="https://www.linkedin.com/in/rafael-will-m-de-araujo-20809b18b/">Rafael Will</a>
    - <a href="https://www.linkedin.com/in/henrique-mohallem-paiva-6854b460/">Henrique Mohallem</a> 
    - <a href="https://www.linkedin.com/in/francisco-escobar/">Francisco Escobar</a> 
    - <a href="https://www.linkedin.com/in/michele-bazana-de-souza-69b77763/">Michele Bazana</a>
    - <a href="https://www.linkedin.com/in/diogo-martins-gon%C3%A7alves-de-morais-96404732/">Diogo Martins</a> 
    """, unsafe_allow_html=True)

    st.markdown("""
    ## 📝 Descrição
    O projeto da equipe Gasbusters do INTELI, além de detectar fraudes no consumo de gás natural, também tem como objetivo identificar padrões de consumo e prever gastos. A criação de um modelo preditivo, com o uso de técnicas de inteligência artificial, é uma resposta à demanda da Compass Gás e Energia SA, que busca otimizar suas operações.
    
    Um dos principais desafios enfrentados no desenvolvimento do modelo é o baixo nível de detalhamento dos dados disponíveis. Isso significa que o modelo precisa trabalhar com informações limitadas, o que torna ainda mais relevante a capacidade de análise avançada e preditiva do sistema. Mesmo com essas limitações, o modelo deve ser capaz de reconhecer tendências de consumo ao longo do tempo e fornecer previsões sobre os gastos futuros dos clientes, oferecendo insights valiosos tanto para otimização de recursos quanto para planejamento estratégico.
    """)

    st.markdown("""
    ## 📁 Estrutura de pastas
    Dentre os arquivos presentes na raiz do projeto, definem-se:

    - <b>readme.md</b>: Arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

    - <b>assets</b>: Todas as imagens e mídias utilizadas nos notebooks e documentação são posicionadas aqui.

    - <b>documents</b>: Aqui estarão todos os documentos do projeto. Há também uma pasta denominada <b>extras</b> onde estão presentes documentos complementares.

    - <b>notebooks</b>: Todos os Jupyter Notebooks criados para desenvolvimento do projeto.

    - <b>.gitattributes</b>: Esse arquivo serve para detectar automaticamente arquivos de texto e normalizá-los.

    - <b>.gitignore</b>: Arquivo destinado para que certos tipos de arquivo <b>(.csv, .xls, .xlsx
        .tsv, .db, .sql)</b> não sejam transportados para nuvem e outros meios on-line, a fim de assegurar itegridade dos dados obtidos e tratados.
    """, unsafe_allow_html=True)

    # Restante do texto
    st.markdown("""
    ## 💻 Execução dos projetos
    ### Sistema Operacional
    O modelo foi testado e pode ser executado em:

    >Windows 10 ou superior macOS 10.15+
    >Distribuições Linux como Ubuntu ou CentOS

    ### Linguagem de Programação
    Este projeto foi desenvolvido em **Python 3.8 ou superior**. Certifique-se de ter uma versão compatível instalada.

    ### Bibliotecas e Pacotes
    ```bash
    pip install -r requirements.txt
    ```
    _Os pacotes essenciais incluem:_

    * _numpy:_ Para manipulação numérica;
    * _pandas:_ Para análise e manipulação de dados;
    * _scikit-learn:_ Para implementação dos algoritmos variados de machine learning;
    * _matplotlib e seaborn:_ Para visualizações e gráficos;
    * _category encoders:_ Para categorização e normalização dos dados.
                
    ### Leitura dos Dados 
    No caso do projeto, o _dataframe_ está sendo importado e utilizado como arquivo **.cvs** e esse mesmo formato está inserido no arquivo **.gitignore**. Por esse fator, a base de dados não estará disponível no _github_ e deverá ser importada em sua máquina local.
                
    ### Ambiente Virtual (Recomendado)
    Recomendamos a utilização de um ambiente virtual para isolar as dependências do projeto. Para criar e ativar um ambiente virtual, utilize os comandos abaixo:
    ```bash
        python -m venv venv
        source venv/bin/activate  #Linux/macOS
        ./venv/Scripts/activate   #Windows
    ```

    ### IDE
    Recomendamos a utilização do _vscode_ para visualização do código e a instalação das seguintes extensões:

    * Jupyter: É um ambiente de desenvolvimento Python  Se um desenvolvedor quer visualizar um gráfico ou fórmula, ele digita o comando desejado na célula correspondente. Essa ação economiza tempo e ajuda a evitar erros.
    * Python: Necessário para compreender a linguagem do código referido.          
    """)

    # Licença
    st.markdown("""
    ## 📋 Licença/License
    <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1">
    <p>
    <a property="dct:title" rel="cc:attributionURL" href="https://github.dev/Intelihub/Template_M3">MODELO GIT INTELI</a> by Inteli is licensed under <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.
    </p>
    """, unsafe_allow_html=True)

