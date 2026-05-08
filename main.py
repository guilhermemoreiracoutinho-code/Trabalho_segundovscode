import streamlit as st

from cleaner import limpar_texto
from extractor import extrair_texto
from processor import criar_chunks, criar_prompt, detetar_idioma


st.set_page_config(
    page_title="TP2 - Pipeline de Texto",
    layout="wide"
)

st.title("Normalização de Texto com Pipeline de Pré-Processamento")
st.write("Aplicação para extração, limpeza, segmentação e preparação de texto para SLMs.")

ficheiro = st.file_uploader(
    "Carrega um ficheiro",
    type=["pdf", "docx", "txt"]
)

if ficheiro:
    try:
        texto_bruto = extrair_texto(ficheiro)

        if not texto_bruto.strip():
            st.warning("Não foi encontrado texto no ficheiro carregado.")
            st.stop()

        aba_original, aba_limpo, aba_idioma, aba_chunks, aba_prompts = st.tabs([
            "Texto Original",
            "Texto Limpo",
            "Idioma",
            "Chunks",
            "Prompts"
        ])

        with aba_original:
            st.text_area("Texto original", texto_bruto, height=500)

        with aba_limpo:
            with st.expander("Configuração da Pipeline", expanded=True):
                col1, col2 = st.columns(2)

                with col1:
                    usar_artefactos = st.toggle("Remover artefactos")
                    usar_cabecalhos = st.toggle("Remover cabeçalhos e rodapés")
                    usar_paragrafos = st.toggle("Reconstruir parágrafos")

                with col2:
                    usar_quebras = st.toggle("Corrigir quebras de linha")
                    usar_espacos = st.toggle("Normalizar espaços")

            texto_limpo = limpar_texto(
                texto_bruto,
                usar_artefactos,
                usar_cabecalhos,
                usar_paragrafos,
                usar_quebras,
                usar_espacos
            ).strip()

            st.text_area("Texto limpo", texto_limpo, height=500)

        idioma = detetar_idioma(texto_limpo)
        chunks = criar_chunks(texto_limpo)

        with aba_idioma:
            st.subheader("Idioma Detetado")
            st.success(idioma)

        with aba_chunks:
            st.subheader("Chunks Gerados")

            if not chunks:
                st.warning("Não foram gerados chunks porque o texto limpo está vazio.")

            for i, chunk in enumerate(chunks, start=1):
                st.text_area(f"Chunk {i}", chunk, height=150)

        with aba_prompts:
            st.subheader("Prompts Gerados")

            if not chunks:
                st.warning("Não há prompts para gerar porque não existem chunks.")

            for i, chunk in enumerate(chunks, start=1):
                st.text_area(
                    f"Prompt {i}",
                    criar_prompt(chunk, idioma),
                    height=200
                )

    except Exception as erro:
        st.error(f"Erro: {erro}")
