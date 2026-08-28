import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name + '.db')
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT NOT NULL
            );      
        """)
    def add(self, note):
        self.conn.execute(
            "INSERT INTO note (title,content) VALUES (?, ?)", 
            (note.title, note.content)      
        )
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT id, title, content FROM note")
        notes = []
        for linha in cursor:
            id = linha[0]
            title = linha[1]
            content = linha[2]
            note = Note(id, title, content)
            notes.append(note)
        return notes

    def update(self, entry):
        self.conn.execute("UPDATE note SET title = ?, content = ? WHERE id = ?", 
        (entry.title, entry.content, entry.id))
        self.conn.commit()

    def delete(self, note_id):
        self.conn.execute("DELETE from note WHERE id = ?", 
        (note_id,))
        self.conn.commit()

    def get_note(self, id_note):
            cursor = self.conn.execute("SELECT id, title, content FROM note")
            for linha in cursor:
                id = linha[0]
                title = linha[1]
                content = linha[2]
                if id == id_note:
                    note = Note(id, title, content)
            return note

class Note:
    def __init__(self, id=None, title=None, content=''):
        self.id = id
        self.title = title
        self.content = content
    
