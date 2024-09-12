from flask import Flask, render_template, redirect, url_for, request
from db import db
from models import Usuario, Tarefa
import datetime

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
        senha2 = request.form['senha2']
        if senha != senha2:
            return render_template('cadastro_page.html', erro="As senhas não coincidem.")

        novo_usuario = Usuario(nome=nome,email=email,telefone=telefone,senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('home'))




@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = db.session.query(Usuario).filter_by(email=email, senha=senha).first()

        if usuario:
            return redirect(url_for('tarefas_page', usuario_id=usuario.id))
        else:
            return redirect(url_for('login'))
        
# por enquanto achei melhor fazer o login com email + senha sem username
    

@app.route('/tarefas/<int:usuario_id>', methods=['GET', 'POST'])
def adicionar_tarefa(usuario_id):
    usuario = db.session.query(Usuario).filter_by(id=usuario_id).first()
    usuarios = db.session.query(Usuario).all()
    
    if request.method == 'GET':
        return render_template('adicionar_tarefa.html', usuario=usuario, usuarios=usuarios)

    elif request.method == 'POST':    
        titulo = request.form['titulo']
        data_inicio_str = request.form['data_inicio']
        data_fim_str = request.form['data_fim']
        descricao = request.form['descricao']
        status = request.form['status']
        userTarefa_id = request.form['userTarefa_id']

        
        data_inicio = datetime.datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
        data_fim = datetime.datetime.strptime(data_fim_str, '%Y-%m-%d').date()

    
        nova_tarefa = Tarefa(titulo=titulo, data_inicio=data_inicio, data_fim=data_fim,descricao=descricao,status=status,        usuario_id=userTarefa_id)
        db.session.add(nova_tarefa)
        db.session.commit()

        
        return redirect(url_for('tarefas_page', usuario_id=usuario_id))
    

@app.route('/editar_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
def editar_tarefa(tarefa_id):
    tarefa = db.session.query(Tarefa).filter_by(id=tarefa_id).first()
    
    if request.method == 'GET':
       return render_template('editar_tarefa.html', tarefa=tarefa)
    
    elif request.method == 'POST':
       
        tarefa.titulo = request.form['titulo']
        tarefa.data_inicio = datetime.datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date()
        tarefa.data_fim = datetime.datetime.strptime(request.form['data_fim'], '%Y-%m-%d').date()
        tarefa.descricao = request.form['descricao']
        tarefa.status = request.form['status']

        
        db.session.commit()

        
        return redirect(url_for('tarefas_page', usuario_id=tarefa.usuario_id))
    

@app.route('/deletar_tarefa/<int:tarefa_id>', methods=['GET'])
def deletar_tarefa(tarefa_id):
    tarefa = db.session.query(Tarefa).filter_by(id=tarefa_id).first()
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
        return redirect(url_for('tarefas_page', usuario_id=tarefa.usuario_id))
    

@app.route('/tarefas_page/<int:usuario_id>', methods=['GET'])
def tarefas_page(usuario_id):
    usuario = db.session.query(Usuario).filter_by(id=usuario_id).first()

   
    status_filtro = request.args.get('status')

    if status_filtro:
       
        tarefas = db.session.query(Tarefa).filter_by(usuario_id=usuario_id, status=status_filtro).all()
    else:
       
        tarefas = db.session.query(Tarefa).filter_by(usuario_id=usuario_id).all()

    return render_template('tarefas_page.html', usuario=usuario, tarefas=tarefas)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)