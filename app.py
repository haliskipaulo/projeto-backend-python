from flask import Flask, render_template, redirect, url_for, request
from db import db
from models import Usuario

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
db.init_app(app)

@app.route('/')
def home():
    usuarios = db.session.query(Usuario).all()
    return render_template('home.html', usuarios = usuarios)


@app.route('/cadastro_page', methods = ['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('cadastro_page.html')
    elif request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        novo_usuario = Usuario(nome=nome,email=email,telefone=telefone,senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':


    



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)