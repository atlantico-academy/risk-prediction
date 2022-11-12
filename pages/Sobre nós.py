import streamlit as st
import random

st.title("Noctua")
sidebar = st.sidebar.image('assets/img/logo.png')  


equipe = [
    "- [Deiferson da Silva Moura](https://github.com/deiferson)",
    "- [Francisco Leocassio da Silva](https://github.com/leocassiosilva)",
    "- [Gabriel Lucas Silva Felix](https://github.com/gabriellfelix)",
    "- [Letícia Dayana de Campos](https://github.com/leticiadcampos92)",
    "- [Luciano Silva de Arruda](https://github.com/lucenfort)",
    "- [Marcello Alexandre Rodrigues Filho](https://github.com/marcelloale)",
    "- [Maria Luísa Leandro de Lima](https://github.com/maluwastaken)",
    "- [Tessele Sampaio Lopes](https://github.com/tesselesampaio)"
]

random.shuffle(equipe)

for member in equipe:
    st.markdown(member)
