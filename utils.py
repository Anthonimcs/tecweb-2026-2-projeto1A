from pathlib import Path
import json

def extract_route(request):
    posicao_barra = request.find("/")
    rota1 = request[posicao_barra+1:]
    pausa = rota1.find(' ')
    rota = rota1[:pausa]
    return rota

def read_file(Path):
    with open(Path, 'rb') as arquivo:
        conteudo_binario = arquivo.read()
        return conteudo_binario

def load_data(arquivo_JSON):
    caminho = Path("data") / arquivo_JSON

    with open(caminho, 'r') as arquivo:
        texto = json.load(arquivo)
        return texto

def load_template(nome_template):
    caminho = Path("templates") / nome_template

    with open(caminho, 'r') as arquivo:
        texto = arquivo.read()
        return texto

def add_notes(anotacao):

    lista = load_data("notes.json")
    lista.append(anotacao)

    caminho = Path("data") / "notes.json"

    with open(caminho, 'w') as arquivo:
    # O json.dump pega o dicionário, transforma em JSON e joga dentro do arquivo
        json.dump(lista, arquivo)
    return

def build_response(body='', code=200, reason='OK', headers=''):
    if headers:
        response = f'HTTP/1.1 {code} {reason}\n{headers}\n\n{body}'
    else:
        response = f'HTTP/1.1 {code} {reason}\n\n{body}'
    return response.encode()