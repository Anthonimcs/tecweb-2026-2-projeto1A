from utils import load_template, build_response
from urllib.parse import unquote_plus
from database import Database, Note

def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    db = Database("notes")
    error = ""
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}

        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[unquote_plus(chave)] = unquote_plus(valor)
        title = params["titulo"].strip()
        content = params["detalhes"].strip()
        if not title or not content:
            error = "Preencha o título e o conteúdo da anotação."
        else:
            note = Note(title=params["titulo"], content=params["detalhes"])
            db.add(note)

    # Busca todas as notas do banco:
    all_notes = db.get_all()

    # Cria o HTML de cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')

    notes_li = []
    for note in all_notes:
        if note.favorite == 1:
            favorite_icon = '⭐'
        else:
            favorite_icon ='☆'
        notes_li.append(note_template.format(title=note.title, details=note.content, id=note.id, favorite = favorite_icon))

    notes = '\n'.join(notes_li)
    body = load_template('index.html').format(notes=notes, error = error)

    return build_response(body=body)

def update_note(request, route):
    note_id = int(route.split("/")[1])
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
        title = params["titulo"].strip()
        content = params["detalhes"].strip()
        if not title or not content:
            body = load_template('update.html').format(
                title=title,
                details=content,
                error="Preencha o título e o conteúdo da anotação."
            )
            return build_response(body=body)
        else:
            note = Note(title=params["titulo"], content=params["detalhes"], id=note_id)
            db.update(note)
            return build_response(
                                    code=303,
                                    reason='See Other',
                                    headers='Location: /'
                                )
    else: 
        note = db.get_note(note_id)
        body = load_template('update.html').format(title=note.title, details=note.content, error = '') 
        return build_response(body=body)

def not_found():
    body = load_template('404.html')
    return build_response(
                            body=body,
                            code=404,
                            reason='Not Found'
                        )

def delete_note(request, route):
    note_id = int(route.split("/")[1])
    db = Database("notes")
    if request.startswith('POST'):
        db.delete(note_id)
        return build_response(
                                code=303,
                                reason='See Other',
                                headers='Location: /'
                            )
    else: 
        note = db.get_note(note_id)
        body = load_template('delete.html').format(title=note.title,details=note.content, id=note.id) 
        return build_response(body=body)

def favorite_note(request, route):
    note_id = int(route.split("/")[1])
    db = Database("notes")
    note = db.get_note(note_id)
    if note.favorite == 1:
        db.favorite(note_id=note_id,favorite=0)
    else: 
        db.favorite(note_id=note_id,favorite=1)
    return build_response(
                            code=303,
                            reason='See Other',
                            headers='Location: /'
                            )