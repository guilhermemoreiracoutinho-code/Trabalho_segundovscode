from langdetect import detect


def detetar_idioma(texto):
    if not texto or len(texto.split()) < 3:
        return "desconhecido"

    try:
        return detect(texto)
    except Exception:
        return "desconhecido"


def formatar_texto(texto):
    if not texto:
        return ""

    texto = texto.strip()
    texto = texto.replace("\t", " ")

    return texto


def criar_chunks(texto, tamanho=1000):
    if not texto or tamanho <= 0:
        return []

    palavras = texto.split()
    chunks = []
    chunk = ""

    for palavra in palavras:
        if len(palavra) >= tamanho:
            if chunk.strip():
                chunks.append(chunk.strip())
                chunk = ""

            chunks.append(palavra)
            continue

        if len(chunk) + len(palavra) + 1 < tamanho:
            chunk += palavra + " "
        else:
            if chunk.strip():
                chunks.append(chunk.strip())

            chunk = palavra + " "

    if chunk.strip():
        chunks.append(chunk.strip())

    return chunks


def criar_prompt(texto, idioma):
    idioma_prompt = idioma if idioma else "desconhecido"

    return f"""
Normaliza o seguinte texto em {idioma_prompt}.

Objetivos:
- corrigir erros gramaticais
- melhorar pontuação
- remover artefactos textuais
- devolver o texto em plain text
- manter o significado original

Texto:
{texto}
"""

