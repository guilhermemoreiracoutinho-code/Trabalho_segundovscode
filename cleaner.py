import re
from collections import Counter


LETRAS = r"A-Za-z\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u00ff"


def corrigir_encoding(texto):
    try:
        corrigido = texto.encode("latin-1").decode("utf-8")
    except UnicodeError:
        return texto

    erros_antes = texto.count("Ã") + texto.count("Â") + texto.count("â")
    erros_depois = corrigido.count("Ã") + corrigido.count("Â") + corrigido.count("â")

    return corrigido if erros_depois < erros_antes else texto


def remover_artefactos(texto):
    texto = corrigir_encoding(texto)
    texto = texto.replace("\ufeff", " ").replace("\u00a0", " ")
    texto = texto.replace("\u200b", "").replace("\u00ad", "")
    texto = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", texto)
    texto = re.sub(rf"(?<=[{LETRAS}])-\s*\n\s*(?=[{LETRAS}])", "", texto)
    texto = re.sub(r"^\s*(p[aá]g(?:ina)?\.?\s*)?\d+\s*(/|de)\s*\d+\s*$", " ", texto, flags=re.I | re.M)
    texto = re.sub(r"^\s*[-_=*#.]{3,}\s*$", " ", texto, flags=re.M)
    texto = re.sub(r"[•●▪◦■□◆◇►→←↑↓]+", " ", texto)
    texto = re.sub(r"[^\w\s.,;:!?()\[\]{}\"'«»“”‘’\-–—/%€$@+=<>\\|]", " ", texto)
    texto = re.sub(r"([!?.,;:])\1{1,}", r"\1", texto)
    return texto


def remover_cabecalhos_rodapes(texto):
    linhas = texto.splitlines()
    normalizadas = [re.sub(r"\s+", " ", linha.strip()) for linha in linhas]
    repetidas = Counter(linha for linha in normalizadas if linha)

    resultado = []
    for linha, limpa in zip(linhas, normalizadas):
        if repetidas[limpa] >= 3:
            continue
        if re.match(r"^(p[aá]g(?:ina)?\.?\s*)?\d+(\s*/\s*\d+)?$", limpa, re.I):
            continue
        resultado.append(linha)

    return "\n".join(resultado)


def reconstruir_paragrafos(texto):
    linhas = texto.splitlines()
    resultado = []

    for linha in linhas:
        linha = linha.strip()

        if not linha:
            if resultado and resultado[-1]:
                resultado.append("")
            continue

        anterior_abrupta = resultado and resultado[-1] and not re.search(r"[.!?:;»”)\]]$", resultado[-1])
        comeca_minuscula = re.match(rf"^[a-z\u00e0-\u00f6\u00f8-\u00ff]", linha)

        if anterior_abrupta and comeca_minuscula:
            resultado[-1] += " " + linha
        else:
            resultado.append(linha)

    return "\n".join(resultado)


def corrigir_quebras_linha(texto):
    texto = re.sub(r"\r\n?", "\n", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = re.sub(r"(?<!\n)\n(?!\n)", " ", texto)
    return texto


def normalizar_texto(texto):
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r" *\n *", "\n", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = re.sub(r"\s+([.,;:!?])", r"\1", texto)
    texto = re.sub(r"([({\[])\s+", r"\1", texto)
    texto = re.sub(r"\s+([)}\]])", r"\1", texto)
    texto = re.sub(rf"([.,;:!?])([{LETRAS}])", r"\1 \2", texto)
    return texto.strip()


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
        texto = remover_cabecalhos_rodapes(texto)
    if usar_paragrafos:
        texto = reconstruir_paragrafos(texto)
    if usar_quebras:
        texto = corrigir_quebras_linha(texto)
    if usar_espacos:
        texto = normalizar_texto(texto)

    return texto
