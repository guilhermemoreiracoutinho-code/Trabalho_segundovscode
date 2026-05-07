from langdetect import detect


def detetar_idioma(texto):

    try:

        return detect(texto)

    except:

        return "desconhecido"
