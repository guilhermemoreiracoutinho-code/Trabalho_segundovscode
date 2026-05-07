import re


# remover caracteres estranhos
def remover_artefactos(texto):

    texto = re.sub(r'[^\x00-\x7FÀ-ÿ]', ' ', texto)

    return texto


# reconstruir parágrafos
def reconstruir_paragrafos(texto):

    texto = re.sub(r'\n(?=[a-zà-ÿ])', ' ', texto)

    return texto


# remover quebras de linha incorretas
def remover_quebras_linha(texto):

    texto = re.sub(r'(?<!\n)\n(?!\n)', ' ', texto)

    return texto


# normalizar espaços
def normalizar_espacos(texto):

    texto = re.sub(r'\s+', ' ', texto)

    return texto.strip()


# remover cabeçalhos repetidos
def remover_cabecalhos(texto):

    linhas = texto.splitlines()

    frequencia = {}

    for linha in linhas:

        linha_limpa = linha.strip()

        if linha_limpa:
            frequencia[linha_limpa] = frequencia.get(linha_limpa, 0) + 1

    resultado = []

    for linha in linhas:

        if frequencia.get(linha.strip(), 0) < 3:
            resultado.append(linha)

    return "\n".join(resultado)


# pipeline principal
def limpar_texto(texto):

    texto = remover_artefactos(texto)

    texto = remover_cabecalhos(texto)

    texto = reconstruir_paragrafos(texto)

    texto = remover_quebras_linha(texto)

    texto = normalizar_espacos(texto)

    return texto