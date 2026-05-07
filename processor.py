from langdetect import detect


def detetar_idioma(texto):

    try:

        return detect(texto)

    except:

        return "desconhecido"


def formatar_texto(texto):

    texto = texto.strip()

    texto = texto.replace("\t", " ")

    return texto


def criar_chunks(texto, tamanho=1000):

    palavras = texto.split()

    chunks = []

    chunk = ""

    for palavra in palavras:

        if len(chunk) + len(palavra) + 1 < tamanho:

            chunk += palavra + " "

        else:

            chunks.append(chunk.strip())

            chunk = palavra + " "

    if chunk:
        chunks.append(chunk.strip())

    return chunks


def criar_prompt(texto, idioma):

    return f"""
Normaliza o seguinte texto em {idioma}.

Objetivos:
- corrigir erros gramaticais
- melhorar pontuação
- remover artefactos textuais
- devolver o texto em plain text
- manter o significado original

Texto:
{texto}
"""
