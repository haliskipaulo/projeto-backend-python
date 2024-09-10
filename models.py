from db import db
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nome = db.Column(db.String(150), unique = True, nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    telefone = db.Column(db.String(150), unique = True, nullable = False)
    senha = db.Column(db.String(20), unique = False, nullable = False)

    def _repr__(self):
        return f"<{self.nome}>"
    

class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(150), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) 