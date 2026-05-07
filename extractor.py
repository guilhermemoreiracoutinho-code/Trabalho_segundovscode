# extractor.py

import pdfplumber
from docx import Document


def extrair_pdf(caminho):

    texto = ""

    with pdfplumber.open(caminho) as pdf:

        for pagina in pdf.pages:

            conteudo = pagina.extract_text()

            if conteudo:

                texto += conteudo + "\n"

    return texto


def extrair_docx(caminho):

    doc = Document(caminho)

    texto = ""

    for paragrafo in doc.paragraphs:

        texto += paragrafo.text + "\n"

    return texto


def extrair_txt(caminho):

    with open(
        caminho,
        "r",
        encoding="utf-8",
        errors="replace"
    ) as ficheiro:

        return ficheiro.read()


def extrair_texto(caminho):

    if caminho.endswith(".pdf"):

        return extrair_pdf(caminho)

    elif caminho.endswith(".docx"):

        return extrair_docx(caminho)

    elif caminho.endswith(".txt"):

        return extrair_txt(caminho)

    else:

        return "Formato não suportado."