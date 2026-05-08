import streamlit as st

from cleaner import limpar_texto
from extractor import extrair_texto
from processor import criar_chunks, detetar_idioma


st.set_page_config(
    page_title="TP2 - Pipeline de Texto",
    layout="wide"
)

st.title("Normalização de Texto com Pipeline de Pré-Processamento")
st.write("Aplicação para extrair, limpar, segmentar e preparar texto para SLMs.")

ficheiro = st.file_uploader(
    "Carrega um ficheiro",
    type=["pdf", "docx", "txt"]
)

if ficheiro:
    try:
        texto_bruto = extrair_texto(ficheiro)

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
                    usar_artefactos = st.toggle("Remover artefactos", value=False)
                    usar_cabecalhos = st.toggle("Remover cabeçalhos e rodapés", value=False)
                    usar_paragrafos = st.toggle("Reconstruir parágrafos", value=False)

                with col2:
                    usar_quebras = st.toggle("Corrigir quebras de linha", value=False)
                    usar_espacos = st.toggle("Normalizar espaços", value=False)

            texto_limpo = limpar_texto(
                texto_bruto,
                usar_artefactos,
                usar_cabecalhos,
                usar_paragrafos,
                usar_quebras,
                usar_espacos
            )

            etapas_ativas = []

            if usar_artefactos:
                etapas_ativas.append("artefactos")
            if usar_cabecalhos:
                etapas_ativas.append("cabeçalhos/rodapés")
            if usar_paragrafos:
                etapas_ativas.append("parágrafos")
            if usar_quebras:
                etapas_ativas.append("quebras de linha")
            if usar_espacos:
                etapas_ativas.append("espaços")

            if not texto_limpo:
                st.warning("O texto ficou vazio após a limpeza.")

            st.text_area("Texto limpo", texto_limpo, height=500)

        idioma = detetar_idioma(texto_limpo)
        chunks = criar_chunks(texto_limpo)
        etapas_texto = ", ".join(etapas_ativas) if etapas_ativas else "nenhuma"

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
            st.caption(f"Os prompts usam o texto limpo com estas etapas: {etapas_texto}.")

            if not chunks:
                st.warning("Não há prompts para gerar porque não existem chunks.")

            for i, chunk in enumerate(chunks, start=1):
                st.text_area(f"Prompt {i}", chunk, height=200)

    except Exception as erro:
        st.error(f"Erro: {erro}")
