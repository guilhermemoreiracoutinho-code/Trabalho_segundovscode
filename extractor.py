import pdfplumber
from docx import Document


def extrair_pdf(ficheiro):

    texto = ""

    with pdfplumber.open(ficheiro) as pdf:

        for pagina in pdf.pages:

            conteudo = pagina.extract_text()

            if conteudo:
                texto += conteudo + "\n"

    return texto


def extrair_docx(ficheiro):

    doc = Document(ficheiro)

    texto = ""

    for paragrafo in doc.paragraphs:
        texto += paragrafo.text + "\n"

    return texto


def extrair_txt(ficheiro):

    return ficheiro.read().decode(
        "utf-8",
        errors="replace"
    )


def extrair_texto(ficheiro):

    nome = ficheiro.name.lower()

    if nome.endswith(".pdf"):
        return extrair_pdf(ficheiro)

    elif nome.endswith(".docx"):
        return extrair_docx(ficheiro)

    elif nome.endswith(".txt"):
        return extrair_txt(ficheiro)

    else:
        return "Formato não suportado."