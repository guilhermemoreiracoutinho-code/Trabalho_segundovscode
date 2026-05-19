from html import escape


def avaliar_normalizacao(texto_original, texto_limpo):
    return {
        "palavras_antes": len(texto_original.split()),
        "palavras_depois": len(texto_limpo.split()),
        "caracteres_antes": len(texto_original),
        "caracteres_depois": len(texto_limpo),
        "diferenca": len(texto_original) - len(texto_limpo),
    }


def gerar_relatorio_html(nome_ficheiro, parametros, texto_original, texto_limpo, idioma, chunks):
    avaliacao = avaliar_normalizacao(texto_original, texto_limpo)
    etapas = [nome for nome, ativo in parametros.items() if ativo]
    etapas_texto = ", ".join(etapas) if etapas else "Nenhuma"

    return f"""<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Relatório da Pipeline</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.5; }}
        pre {{ background: #f4f4f4; padding: 12px; white-space: pre-wrap; }}
        td, th {{ border: 1px solid #ccc; padding: 8px; }}
        table {{ border-collapse: collapse; width: 100%; }}
    </style>
</head>
<body>
    <h1>Relatório da Pipeline de Texto</h1>
    <h2>Parâmetros</h2>
    <p><b>Ficheiro:</b> {escape(nome_ficheiro)}</p>
    <p><b>Idioma:</b> {escape(idioma)}</p>
    <p><b>Etapas aplicadas:</b> {escape(etapas_texto)}</p>
    <p><b>Número de chunks:</b> {len(chunks)}</p>

    <h2>Avaliação da Normalização</h2>
    <table>
        <tr><th>Métrica</th><th>Valor</th></tr>
        <tr><td>Palavras antes</td><td>{avaliacao["palavras_antes"]}</td></tr>
        <tr><td>Palavras depois</td><td>{avaliacao["palavras_depois"]}</td></tr>
        <tr><td>Caracteres antes</td><td>{avaliacao["caracteres_antes"]}</td></tr>
        <tr><td>Caracteres depois</td><td>{avaliacao["caracteres_depois"]}</td></tr>
        <tr><td>Diferença de caracteres</td><td>{avaliacao["diferenca"]}</td></tr>
    </table>

    <h2>Texto Antes</h2>
    <pre>{escape(texto_original)}</pre>

    <h2>Texto Depois</h2>
    <pre>{escape(texto_limpo)}</pre>
</body>
</html>
"""
