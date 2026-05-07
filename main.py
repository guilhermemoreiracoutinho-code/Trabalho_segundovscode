import streamlit as st
import os

from extractor import extrair_texto
from cleaner import limpar_texto
from processor import detetar_idioma


st.set_page_config(page_title="TP2 - Pipeline de Texto")

st.title("Normalização de Texto com Pipeline de Pré‑Processamento e SLMs")


uploaded_file = st.file_uploader(
    "Carrega um ficheiro",
    type=["pdf", "docx", "txt"]
)


if uploaded_file:

    caminho = uploaded_file.name

    with open(caminho, "wb") as f:
        f.write(uploaded_file.getbuffer())



    texto_bruto = extrair_texto(caminho)

    st.subheader("Texto Original")

    st.text_area(
        "Texto extraído sem transformações",
        texto_bruto,
        height=300
    )



    # LIMPEZA
    texto_limpo = limpar_texto(texto_bruto)

    st.subheader("Texto Após Limpeza")

    st.text_area(
        "Texto processado",
        texto_limpo,
        height=300
    )

    # IDIOMA
    idioma = detetar_idioma(texto_limpo)

    st.subheader("Idioma Detetado")

    st.write(idioma)

    # apagar ficheiro temporário
    os.remove(caminho)