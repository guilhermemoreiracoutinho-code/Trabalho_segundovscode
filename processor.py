# processor.py

from langdetect import detect


def detetar_idioma(texto):

    try:

        return detect(texto)

    except:

        return "desconhecido"


def formatar_texto(texto):

    texto = texto.strip()

    return texto


def criar_chunks(texto, tamanho=500):

    palavras = texto.split()

    chunks = []

    chunk_atual = ""

    for palavra in palavras:

        if len(chunk_atual) + len(palavra) < tamanho:

            chunk_atual += palavra + " "

        else:

            chunks.append(chunk_atual.strip())

            chunk_atual = palavra + " "

    if chunk_atual:

        chunks.append(chunk_atual.strip())

    return chunks


def criar_prompt(texto, idioma):

    prompt = f"""
Normaliza o seguinte texto em {idioma}.

Objetivos:
- corrigir erros gramaticais
- melhorar pontuação
- remover artefactos textuais
- manter significado original

Texto:
{texto}
"""

    return prompt