import requests


URL_API = "https://reality.utad.net/slm"
MODELO = "llama-3.2-1b-instruct"


def criar_prompt(texto_limpo):
    return (
        "Normaliza o texto seguinte, corrigindo pequenos erros e mantendo "
        "o significado original. Devolve apenas o texto final.\n\n"
        f"{texto_limpo}"
    )


def processar_resposta(dados):
    if "choices" in dados:
        return dados["choices"][0]["message"]["content"]

    if "response" in dados:
        return dados["response"]

    if "content" in dados:
        return dados["content"]

    return str(dados)


def enviar_para_slm(texto_limpo):
    prompt = criar_prompt(texto_limpo)

    body = {
        "model": MODELO,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    resposta = requests.post(URL_API, json=body, timeout=60)
    resposta.raise_for_status()

    return processar_resposta(resposta.json())
