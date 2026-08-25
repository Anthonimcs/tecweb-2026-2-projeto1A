from utils import load_template, build_response
from urllib.parse import unquote_plus
from database import Database, Note

def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    db = Database("notes")
    
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[unquote_plus(chave)] = unquote_plus(valor)
        note = Note(title=params["titulo"], content=params["detalhes"])
        db.add(note)

    # Busca todas as notas do banco:
    all_notes = db.get_all()

    # Cria o HTML de cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')

    notes_li = [
        note_template.format(title=note.title, details=note.content, id=note.id)
        for note in all_notes
    ]

    notes = '\n'.join(notes_li)
    body = load_template('index.html').format(notes=notes)

    return build_response(body=body)

def delete_note(id):
    db = Database("notes")
    db.delete(id)