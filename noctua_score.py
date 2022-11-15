import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
#import locale
from joblib import load
import pandas as pd
import streamlit as st

import numpy as np
import plotly.graph_objects as go



st.set_page_config(layout="wide")
# st.sidebar.image('assets/img/logo.png', width=100)

#locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
hoje = datetime.datetime.now()

model = load('models/model.joblib')
    
st.title("Noctua score")
sidebar = st.sidebar.image('assets/img/logo.png')   


columns = [
    'AGE', 'SEX', 'MARRIAGE', 'EDUCATION', 'LIMIT_BAL', 'PAY_0', 'PAY_2',
    'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3',
    'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3',
    'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6'
]



def main():
    inputs = {}

    saidade_anterior = {}
    
    col1, col2, col3, col4 = st.columns(4)

    marriage_dict = {
        1: "Casado",
        2: "Solteiro",
        3: "Outros",
    }
    education_dict = {
        1: 'Pós-graduação', 
        2: 'Universidade', 
        3: 'Ensino médio',
        0: 'Outros',
    }
    sex_dict = {
        1: 'Masculino',
        2: 'Feminino',
        3: 'Outros'
    }

    inputs['AGE'] = col1.number_input("Idade", min_value=18, max_value=100, value=18)
    inputs['SEX'] = col2.selectbox("Sexo", sex_dict.keys(), format_func=lambda x: sex_dict[x])
    inputs['MARRIAGE'] = col3.selectbox("Estado civil", marriage_dict.keys(), format_func=lambda x: marriage_dict[x])
    inputs['EDUCATION'] = col4.selectbox("Educação", education_dict.keys(), format_func=lambda x: education_dict[x])

    with st.expander('Informações adicionais'):
        col1, col2 = st.columns([.8, .2])
        inputs['LIMIT_BAL'] = col1.number_input("Limite do cartão de crédito", min_value=0, max_value=1000000, value=0, step=50)
        if inputs['LIMIT_BAL'] == 0:
            inputs.pop('LIMIT_BAL')
        N = col2.number_input("Número de faturas", min_value=0, max_value=6, value=0)
        col1, col2 = st.columns(2)
        for i in range(N):
            mes_anterior = (hoje + relativedelta(months=-(i+1))).strftime("%B")
            inputs[f'BILL_AMT{i+1}'] = col1.number_input(f"Fatura de {mes_anterior}", min_value=0, max_value=1000000, value=0, step=50)
            inputs[f'PAY_AMT{i+1}'] = col2.number_input(f"Valor pago na fatura {mes_anterior}", min_value=0, max_value=1000000, value=0, step=50)

    

    X = pd.DataFrame({key: [inputs.get(key, None)] for key in columns})

    if st.button("Calcular Score"):
        
        #if saida:
        #    saidade_anterior = saida[0][1]*1000
        #    st.write(saidade_anterior)
        
        
        saida = model.predict_proba(X)        
        go_chart = saida[0][0]*1000 
        
        fig = go.Figure(go.Indicator(
                domain = {'x': [0,1], 'y': [0, 1]},
                value = go_chart,
                mode = "gauge+number",
                title = {'text': "Score"},
                gauge = {'axis': {'range': [None, 1000]},
                         'bar': {'color': "#505050"},
                         'steps' : [
                             {'range': [0, 300], 'color': '#f54d41'},
                             {'range': [301, 500], 'color': '#ccde3e'},
                             {'range': [501, 700], 'color': '#b4c9a8'},
                             {'range': [701, 1000], 'color': '#20b253'}]
                        }
                )                
            )
        
        col1, col2 = st.columns([.6, .4])
        
        
        if go_chart <= 300:
            col2.error("Seu score está ruim!")            
        elif go_chart <= 500:
            col2.warning("Seu score está regular!")   
        elif go_chart <= 700:
            col2.info("Seu score está bom!")
        else:
            col2.success("Seu score está muito bom!")
        
        
        col1.plotly_chart(fig)
        col2.markdown("""
                O Serasa Score, que segue utiliza as seguintes faixas de classificação:
                
                <center>
                
                | **Quantidade** | **Nível** |
                |:--------------:|:---------:|
                | 0 - 300        | Ruim      |
                | 301 - 500      | Regular   |
                | 501 - 700      | Bom       |
                | 701 - 1000     | Muito Bom |
                
                </center>
                """, unsafe_allow_html=True)

      

            
if __name__ == '__main__':
    main()
