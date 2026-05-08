from langdetect import detect


def detetar_idioma(texto):
    if not texto or len(texto.split()) < 3:
        return "desconhecido"

    try:
        return detect(texto)
    except Exception:
        return "desconhecido"


def criar_chunks(texto, tamanho=1000):
    chunks = []
    chunk = ""

    for palavra in texto.split():
        if len(chunk) + len(palavra) + 1 <= tamanho:
            chunk += palavra + " "
        else:
            if chunk.strip():
                chunks.append(chunk.strip())
            chunk = palavra + " "

    if chunk.strip():
        chunks.append(chunk.strip())

    return chunks
