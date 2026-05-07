import re


def remover_artefactos(texto):
    texto = texto.replace("\ufeff", " ")
    texto = texto.replace("\u00a0", " ")
    texto = texto.replace("\u00ad", "")

    texto = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", texto)

    texto = re.sub(
        r"(?<=[A-Za-zÀ-ÖØ-öø-ÿ])-\s*\n\s*(?=[A-Za-zÀ-ÖØ-öø-ÿ])",
        "",
        texto
    )

    texto = re.sub(
        r"[^\w\s.,;:!?()\[\]{}\"'\u00ab\u00bb\u201c\u201d\u2018\u2019\-"
        r"\u2013\u2014/@%€$+#*=<>\\]",
        " ",
        texto,
        flags=re.UNICODE
    )

    texto = re.sub(
        r"^\s*(p[aá]g(?:ina)?\.?\s*)?\d+\s*(?:/|de)\s*\d+\s*$",
        " ",
        texto,
        flags=re.IGNORECASE | re.MULTILINE
    )
    texto = re.sub(r"^\s*[-_=*#.]{3,}\s*$", " ", texto, flags=re.MULTILINE)
    texto = re.sub(r"([^\w\s])\1{2,}", r"\1", texto)

    return texto


def limpar_texto(
    texto,
    usar_artefactos=True,
    usar_cabecalhos=True,
    usar_paragrafos=True,
    usar_quebras=True,
    usar_espacos=True
):
    if not texto:
        return ""

    if usar_artefactos:
        texto = remover_artefactos(texto)

    if usar_cabecalhos:
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

        texto = "\n".join(resultado)

    if usar_paragrafos:
        texto = re.sub(
            r"(?<=[^\n.!?:;])\n(?=[^\nA-ZÁÀÂÃÉÊÍÓÔÕÚÇ])",
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
            r"[ \t]+",
            " ",
            texto
        )

        texto = re.sub(
            r" *\n *",
            "\n",
            texto
        )

        texto = re.sub(
            r"\n{3,}",
            "\n\n",
            texto
        )

        texto = texto.strip()

    return texto
