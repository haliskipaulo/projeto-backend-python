from db import db
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nome = db.Column(db.String(150), unique = True, nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    telefone = db.Column(db.String(150), unique = True, nullable = False)
    senha = db.Column(db.String(20), unique = True, nullable = False)

    def _repr__(self):
        return f"<{self.nome}>"