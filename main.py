import streamlit as st

from extractor import extrair_texto
from cleaner import limpar_texto

from processor import (
    detetar_idioma,
    criar_chunks,
    criar_prompt,
    formatar_texto
)


st.set_page_config(
    page_title="TP2 - Pipeline de Texto",
    layout="wide"
)

st.title("Normalização de Texto com Pipeline de Pré-Processamento e SLMs")

st.write(
    "Aplicação para extração, limpeza e preparação de texto para SLMs."
)


uploaded_file = st.file_uploader(
    "Carrega um ficheiro",
    type=["pdf", "docx", "txt"]
)


if uploaded_file:

    try:

        texto_bruto = extrair_texto(uploaded_file)

        aba1, aba2, aba3, aba4, aba5 = st.tabs([
            "Texto Original",
            "Texto Limpo",
            "Idioma",
            "Chunks",
            "Prompts"
        ])

        with aba1:

            st.subheader("Texto Original")

            st.text_area(
                "",
                texto_bruto,
                height=500
            )

        with aba2:

            st.sidebar.header("Configuração da Pipeline")

            usar_artefactos = st.sidebar.checkbox(
                "Remover artefactos",
                True
            )

            usar_cabecalhos = st.sidebar.checkbox(
                "Remover cabeçalhos",
                True
            )

            usar_paragrafos = st.sidebar.checkbox(
                "Reconstruir parágrafos",
                True
            )

            usar_quebras = st.sidebar.checkbox(
                "Corrigir quebras de linha",
                True
            )

            usar_espacos = st.sidebar.checkbox(
                "Normalizar espaços",
                True
            )

            texto_limpo = limpar_texto(
                texto_bruto,
                usar_artefactos,
                usar_cabecalhos,
                usar_paragrafos,
                usar_quebras,
                usar_espacos
            )

            texto_final = formatar_texto(texto_limpo)

            melhorias = []

            if usar_artefactos:
                melhorias.append("Artefactos")

            if usar_cabecalhos:
                melhorias.append("Cabeçalhos")

            if usar_paragrafos:
                melhorias.append("Parágrafos")

            if usar_quebras:
                melhorias.append("Quebras")

            if usar_espacos:
                melhorias.append("Espaços")

            titulo = "Texto Após Limpeza"

            if melhorias:
                titulo += ": " + ", ".join(melhorias)

            st.subheader(titulo)

            st.text_area(
                "",
                texto_final,
                height=500
            )

        idioma = detetar_idioma(texto_final)

        chunks = criar_chunks(texto_final)

        with aba3:

            st.subheader("Idioma Detetado")

            st.success(idioma)

        with aba4:

            st.subheader("Chunks Gerados")

            for i, chunk in enumerate(chunks):

                st.text_area(
                    f"Chunk {i+1}",
                    chunk,
                    height=150
                )

        with aba5:

            st.subheader("Prompts Gerados")

            for i, chunk in enumerate(chunks):

                prompt = criar_prompt(chunk, idioma)

                st.text_area(
                    f"Prompt {i+1}",
                    prompt,
                    height=200
                )

    except Exception as erro:

        st.error(f"Erro: {erro}")