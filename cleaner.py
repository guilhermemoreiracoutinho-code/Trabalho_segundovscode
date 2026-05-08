import re
from collections import Counter


LETRAS = r"A-Za-zÀ-ÖØ-öø-ÿ"


def corrigir_encoding(texto):
    """Corrige casos comuns de acentuação estragada"""
    if "Ã" not in texto and "Â" not in texto:
        return texto

    try:
        corrigido = texto.encode("latin-1", errors="ignore").decode("utf-8", errors="ignore")
    except UnicodeError:
        return texto

    erros_antes = texto.count("Ã") + texto.count("Â")
    erros_depois = corrigido.count("Ã") + corrigido.count("Â")

    if erros_depois < erros_antes and len(corrigido) > len(texto) * 0.6:
        return corrigido

    return texto


def remover_artefactos(texto):
    texto = corrigir_encoding(texto)

    for antigo, novo in {"\ufeff": " ", "\u00a0": " ", "\u200b": "", "\u00ad": ""}.items():
        texto = texto.replace(antigo, novo)

    texto = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", texto)
    texto = re.sub(r"([A-Za-zÀ-ÿ])-\s*\n\s*([A-Za-zÀ-ÿ])", r"\1\2", texto)
    texto = re.sub(r"^\s*(p[aá]gina\s*)?\d+\s*(/|de)\s*\d+\s*$", "", texto, flags=re.I | re.M)
    texto = re.sub(r"[^\w\s.,;:!?()\"'\-/%€]", " ", texto)
    texto = re.sub(r"([!?.,;:])\1+", r"\1", texto)

    return texto


def remover_cabecalhos_rodapes(texto):
    linhas = texto.splitlines()
    linhas_normalizadas = [re.sub(r"\s+", " ", linha.strip()) for linha in linhas]
    frequencia = Counter(linha for linha in linhas_normalizadas if linha)

    resultado = []

    for linha, linha_limpa in zip(linhas, linhas_normalizadas):
        if frequencia[linha_limpa] >= 3:
            continue

        if re.match(r"^(p[aá]g(?:ina)?\.?\s*)?\d+(\s*/\s*\d+)?$", linha_limpa, re.I):
            continue

        resultado.append(linha)

    return "\n".join(resultado)


def reconstruir_paragrafos(texto):
    resultado = []

    for linha in texto.splitlines():
        linha = linha.strip()

        if not linha:
            if resultado and resultado[-1]:
                resultado.append("")
            continue

        if resultado and resultado[-1]:
            fim_abrupto = not re.search(r"[.!?:;»”)\]]$", resultado[-1])
            inicio_minusculo = bool(re.match(r"^[a-zà-öø-ÿ]", linha))

            if fim_abrupto and inicio_minusculo:
                resultado[-1] += " " + linha
                continue

        resultado.append(linha)

    return "\n".join(resultado)


def corrigir_quebras_linha(texto):
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = re.sub(r"(?<!\n)\n(?!\n)", " ", texto)
    return texto


def normalizar_texto(texto):
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r" *\n *", "\n", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = re.sub(r"\s+([.,;:!?])", r"\1", texto)
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
