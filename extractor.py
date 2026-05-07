import pdfplumber
from docx import Document


def extrair_pdf(ficheiro):
    texto = ""

    with pdfplumber.open(ficheiro) as pdf:
        for pagina in pdf.pages:
            conteudo = pagina.extract_text()

            if conteudo:
                texto += conteudo + "\n"

    texto = texto.strip()

    if not texto:
        raise ValueError("Não foi possível extrair texto do PDF.")

    return texto


def extrair_docx(ficheiro):
    doc = Document(ficheiro)
    texto = ""

    for paragrafo in doc.paragraphs:
        texto += paragrafo.text + "\n"

    texto = texto.strip()

    if not texto:
        raise ValueError("Não foi possível extrair texto do ficheiro DOCX.")

    return texto


def extrair_txt(ficheiro):
    conteudo = ficheiro.read()

    if not conteudo:
        raise ValueError("O ficheiro TXT está vazio.")

    for codificacao in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            texto = conteudo.decode(codificacao)
            break
        except UnicodeDecodeError:
            continue
    else:
        texto = conteudo.decode("utf-8", errors="replace")

    texto = texto.strip()

    if not texto:
        raise ValueError("O ficheiro TXT não contém texto legível.")

    return texto


def extrair_texto(ficheiro):
    nome = ficheiro.name.lower()

    if nome.endswith(".pdf"):
        return extrair_pdf(ficheiro)

    if nome.endswith(".docx"):
        return extrair_docx(ficheiro)

    if nome.endswith(".txt"):
        return extrair_txt(ficheiro)

    raise ValueError("Formato não suportado. Usa um ficheiro PDF, DOCX ou TXT.")
