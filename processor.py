from langdetect import detect


def detetar_idioma(texto):

    try:

        return detect(texto)

    except:

        return "desconhecido"


def formatar_texto(texto):

    return texto.strip()


def criar_chunks(texto, tamanho=500):

    palavras = texto.split()

    chunks = []

    chunk = ""

    for palavra in palavras:

        if len(chunk) + len(palavra) < tamanho:

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
