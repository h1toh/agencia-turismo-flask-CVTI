from app import app
from flask import redirect, request, render_template, flash, session
import json, os

app.secret_key = 'CVTI'

@app.route("/")
def redirectHome():
    return redirect('/home')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/viagens")
def viagens():
    return render_template('viagens.html')

@app.route("/favoritos")
def favoritos():
    return render_template('favoritos.html')

@app.route("/conectar")
def conectar():
    return render_template('conectar.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/auth", methods=['POST'])
def auth():
    email = request.form.get('email')
    senha = request.form.get('senha')

    try:
        if os.path.exists('app/conta.json'):
            with open('app/conta.json') as link:
                conta = json.load(link)
                for c in conta:
                    if c['email'] == email and c['senha'] == senha:
                        session['user'] = c['nome']
                        session['email'] = c['email']
                        session['celular'] = c['celular']
                        return redirect('/home')
                flash('Email ou senha incorretos.', 'error')
                return redirect('/login')
        else:
            flash('Conta inexistente.', 'error')
            return redirect('/signup')
    except:
        return redirect('/login')


@app.route("/creating", methods=['POST'])
def createAcc():
    nomeSignup = request.form.get('nome')
    emailSignup = request.form.get('email')
    celularSignup = request.form.get('celular')
    senhaSignup = request.form.get('senha')

    nova_conta = dict(nome=nomeSignup, email=emailSignup, celular=celularSignup, senha=senhaSignup)

    try:
        if os.path.exists('app/conta.json'):
            with open('app/conta.json','r') as link:
                conta = json.load(link)
                for c in conta:
                    if c['email'] == emailSignup:
                        return "Email já existente."
        else:
            conta = []
        conta.append(nova_conta)

        with open('app/conta.json','w') as link:
            json.dump(conta,link,indent='\t')
            return redirect('/login')
    except:
        return redirect('/signup')
    
@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect('/home')
    return render_template('profile.html', email = session['email'], user = session['user'], cel = session['celular'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('email', None)
    return redirect('/home')