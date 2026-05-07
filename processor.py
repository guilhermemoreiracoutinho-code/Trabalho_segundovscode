from langdetect import detect


# dividir texto em blocos
def dividir_chunks(texto, tamanho=500):

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


# detetar idioma
def detetar_idioma(texto):

    try:
        return detect(texto)

    except:
        return "desconhecido"


# gerar prompt automaticamente
def gerar_prompt(texto):

    prompt = f"""
Normaliza o seguinte texto.

Corrige:
- erros gramaticais
- problemas de pontuação
- inconsistências estruturais

Texto:
{texto}
"""

    return prompt