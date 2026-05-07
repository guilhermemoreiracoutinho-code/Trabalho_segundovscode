# main.py

import os
import streamlit as st

from extractor import extrair_texto
from cleaner import limpar_texto

from processor import (
    detetar_idioma,
    criar_chunks,
    criar_prompt,
    formatar_texto
)


st.set_page_config(page_title="TP2 - Pipeline de Texto")

st.title("Normalização de Texto com Pipeline de Pré-Processamento e SLMs")


uploaded_file = st.file_uploader(
    "Carrega um ficheiro",
    type=["pdf", "docx", "txt"]
)


if uploaded_file:

    caminho = uploaded_file.name

    with open(caminho, "wb") as f:

        f.write(uploaded_file.getbuffer())

    try:

        # TEXTO ORIGINAL

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

        # FORMATAÇÃO

        texto_formatado = formatar_texto(texto_limpo)

        st.subheader("Texto Formatado")

        st.text_area(
            "Texto pronto para SLM",
            texto_formatado,
            height=300
        )

        # IDIOMA

        idioma = detetar_idioma(texto_formatado)

        st.subheader("Idioma Detetado")

        st.write(idioma)

        # CHUNKS

        chunks = criar_chunks(texto_formatado)

        st.subheader("Chunks Gerados")

        for i, chunk in enumerate(chunks):

            st.text_area(
                f"Chunk {i+1}",
                chunk,
                height=150
            )

        # PROMPTS

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

    finally:

        os.remove(caminho)