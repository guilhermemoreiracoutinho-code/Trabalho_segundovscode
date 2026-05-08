from langdetect import detect


def detetar_idioma(texto):
    if not texto or len(texto.split()) < 3:
        return "desconhecido"

    try:
        return detect(texto)
    except Exception:
        return "desconhecido"


def criar_chunks(texto, tamanho=1000):
    palavras = texto.split()
    chunks = []
    chunk = ""

    for palavra in palavras:
        if len(chunk) + len(palavra) + 1 <= tamanho:
            chunk += palavra + " "
        else:
            if chunk.strip():
                chunks.append(chunk.strip())
            chunk = palavra + " "

    if chunk.strip():
        chunks.append(chunk.strip())

    return chunks


def criar_prompt(texto, idioma):
    return (
        f"Normaliza o texto seguinte em {idioma}. "
        "Corrige gramática, pontuação e artefactos, mantendo o significado. "
        "Devolve apenas plain text.\n\n"
        f"{texto}"
    )
