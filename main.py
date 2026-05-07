from hashlib import sha1

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


def criar_key(prefixo, texto):
    resumo = sha1(texto.encode("utf-8")).hexdigest()[:12]
    return f"{prefixo}_{resumo}"


uploaded_file = st.file_uploader(
    "Carrega um ficheiro",
    type=["pdf", "docx", "txt"]
)


if uploaded_file:
    try:
        texto_bruto = extrair_texto(uploaded_file)

        if not texto_bruto.strip():
            st.warning("Não foi encontrado texto no ficheiro carregado.")
            st.stop()

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
                height=500,
                key=criar_key("texto_original", texto_bruto)
            )

        with aba2:
            st.subheader("Configuração da Pipeline")

            col1, col2 = st.columns(2)

            with col1:
                usar_artefactos = st.checkbox(
                    "Remover artefactos",
                    value=True
                )

                usar_cabecalhos = st.checkbox(
                    "Remover cabeçalhos",
                    value=True
                )

                usar_paragrafos = st.checkbox(
                    "Reconstruir parágrafos",
                    value=True
                )

            with col2:
                usar_quebras = st.checkbox(
                    "Corrigir quebras de linha",
                    value=True
                )

                usar_espacos = st.checkbox(
                    "Normalizar espaços",
                    value=True
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

            if not texto_final:
                st.warning("O texto ficou vazio após a limpeza.")

            st.text_area(
                "",
                texto_final,
                height=500,
                key=criar_key("texto_limpo", texto_final)
            )

        idioma = detetar_idioma(texto_final)
        chunks = criar_chunks(texto_final)

        with aba3:
            st.subheader("Idioma Detetado")
            st.success(idioma)

        with aba4:
            st.subheader("Chunks Gerados")

            if not chunks:
                st.warning("Não foram gerados chunks porque o texto limpo está vazio.")

            for i, chunk in enumerate(chunks):
                st.text_area(
                    f"Chunk {i + 1}",
                    chunk,
                    height=150,
                    key=criar_key(f"chunk_{i}", chunk)
                )

        with aba5:
            st.subheader("Prompts Gerados")

            if not chunks:
                st.warning("Não há prompts para gerar porque não existem chunks.")

            for i, chunk in enumerate(chunks):
                prompt = criar_prompt(chunk, idioma)

                st.text_area(
                    f"Prompt {i + 1}",
                    prompt,
                    height=200,
                    key=criar_key(f"prompt_{i}", prompt)
                )

    except Exception as erro:
        st.error(f"Erro: {erro}")
