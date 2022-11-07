import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import locale
from joblib import load

import streamlit as st
import pandas as pd


locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')
hoje = datetime.datetime.now()
model = load('models/model.joblib')

columns = [
    'AGE', 'SEX', 'MARRIAGE', 'EDUCATION', 'LIMIT_BAL', 'PAY_0', 'PAY_2',
    'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3',
    'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3',
    'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6'
]

def main():
    inputs = {}


    st.title("Noctua score")

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

    saida = model.predict_proba(X)
    st.write(saida)
    

if __name__ == '__main__':
    main()