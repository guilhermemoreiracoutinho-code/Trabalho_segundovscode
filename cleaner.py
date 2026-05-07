import re


def limpar_texto(
    texto,
    usar_artefactos=True,
    usar_cabecalhos=True,
    usar_paragrafos=True,
    usar_quebras=True,
    usar_espacos=True
):

    if usar_artefactos:

        texto = re.sub(
            r"[^\x00-\x7FÀ-ÿ\n]",
            " ",
            texto
        )

    if usar_cabecalhos:

        linhas = texto.splitlines()

        frequencia = {}

        for linha in linhas:

            linha_limpa = linha.strip()

            if linha_limpa:
                frequencia[linha_limpa] = frequencia.get(
                    linha_limpa,
                    0
                ) + 1

        resultado = []

        for linha in linhas:

            if frequencia.get(linha.strip(), 0) < 3:
                resultado.append(linha)

        texto = "\n".join(resultado)

    if usar_paragrafos:

        texto = re.sub(
            r"\n(?=[a-zà-ÿ])",
            " ",
            texto
        )

    if usar_quebras:

        texto = re.sub(
            r"(?<!\n)\n(?!\n)",
            " ",
            texto
        )

    if usar_espacos:

        texto = re.sub(
            r"\s+",
            " ",
            texto
        )

        texto = texto.strip()

    return texto