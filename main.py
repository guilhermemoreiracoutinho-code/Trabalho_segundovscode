import streamlit as st

from cleaner import limpar_texto
from extractor import extrair_texto
from processor import criar_chunks, detetar_idioma
from report import avaliar_normalizacao, gerar_relatorio_html
from slm import criar_prompt, enviar_para_slm


def mostrar_blocos(titulo, blocos, altura=150):
    st.subheader(titulo)

    if not blocos:
        st.warning("Não há conteúdo para mostrar.")

    for i, bloco in enumerate(blocos, start=1):
        st.text_area(f"{titulo[:-1]} {i}", bloco, height=altura)


st.set_page_config(page_title="TP2 - Pipeline de Texto", layout="wide")

st.title("Normalização de Texto com Pipeline de Pré-Processamento")
st.write("Aplicação para extrair, limpar, segmentar e preparar texto para SLMs.")

ficheiro = st.file_uploader(
    "Carrega um ficheiro ou arrasta-o para a caixa abaixo",
    type=["pdf", "docx", "txt"]
)

if ficheiro:
    try:
        texto_bruto = extrair_texto(ficheiro)

        abas = st.tabs([
            "Texto Original",
            "Texto Limpo",
            "Idioma",
            "Chunks",
            "Prompts",
            "SLM",
            "Relatório"
        ])

        aba_original, aba_limpo, aba_idioma, aba_chunks, aba_prompts, aba_slm, aba_relatorio = abas

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

            parametros = {
                "Remoção de artefactos": usar_artefactos,
                "Remoção de cabeçalhos e rodapés": usar_cabecalhos,
                "Reconstrução de parágrafos": usar_paragrafos,
                "Correção de quebras de linha": usar_quebras,
                "Normalização de espaços": usar_espacos,
            }

            texto_limpo = limpar_texto(
                texto_bruto,
                usar_artefactos,
                usar_cabecalhos,
                usar_paragrafos,
                usar_quebras,
                usar_espacos
            )

            if not texto_limpo:
                st.warning("O texto ficou vazio após a limpeza.")

            st.text_area("Texto limpo", texto_limpo, height=500)

        idioma = detetar_idioma(texto_limpo)
        chunks = criar_chunks(texto_limpo)
        prompts = [criar_prompt(chunk) for chunk in chunks]
        etapas_ativas = [nome for nome, ativo in parametros.items() if ativo]
        etapas_texto = ", ".join(etapas_ativas) if etapas_ativas else "nenhuma"

        with aba_idioma:
            st.subheader("Idioma Detetado")
            st.success(idioma)

        with aba_chunks:
            mostrar_blocos("Chunks", chunks)

        with aba_prompts:
            st.caption(f"Os prompts usam o texto limpo com estas etapas: {etapas_texto}.")
            mostrar_blocos("Prompts", prompts, altura=200)

        with aba_slm:
            st.subheader("Enviar para o SLM")

            if not chunks:
                st.warning("Não há texto limpo para enviar ao SLM.")
            else:
                numero_chunk = st.selectbox("Escolhe o chunk para enviar", range(1, len(chunks) + 1))
                chunk_escolhido = chunks[numero_chunk - 1]
                prompt = criar_prompt(chunk_escolhido)

                st.text_area("Prompt enviado à API", prompt, height=200)

                if st.button("Enviar pedido ao SLM"):
                    try:
                        with st.spinner("A aguardar resposta do SLM..."):
                            resposta = enviar_para_slm(chunk_escolhido)

                        st.success("Resposta recebida.")
                        st.text_area("Resposta do SLM", resposta, height=300)
                    except Exception as erro_slm:
                        st.error(f"Erro ao contactar o SLM: {erro_slm}")

        with aba_relatorio:
            st.subheader("Relatório Automático")
            avaliacao = avaliar_normalizacao(texto_bruto, texto_limpo)

            st.write(f"Etapas aplicadas: {etapas_texto}")
            st.write(f"Palavras antes/depois: {avaliacao['palavras_antes']} / {avaliacao['palavras_depois']}")
            st.write(f"Caracteres antes/depois: {avaliacao['caracteres_antes']} / {avaliacao['caracteres_depois']}")
            st.write(f"Diferença de caracteres: {avaliacao['diferenca']}")

            relatorio_html = gerar_relatorio_html(
                ficheiro.name,
                parametros,
                texto_bruto,
                texto_limpo,
                idioma,
                chunks
            )

            st.download_button(
                "Exportar relatório HTML",
                data=relatorio_html,
                file_name="relatorio_pipeline.html",
                mime="text/html"
            )

    except Exception as erro:
        st.error(f"Erro: {erro}")
