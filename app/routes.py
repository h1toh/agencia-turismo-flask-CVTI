from app import app
from flask import redirect, request, render_template, flash, session
import json, os, app.ofer as of, requests

app.secret_key = 'CVTI'

@app.route("/")
def loading():
    return render_template('loading.html')

@app.route("/home")
def home():
    hoteis = []
    precos = []
    locais = []
    estados = []
    tempos = []
    moedas = []

    for i in range(3):
        local = of.ofertas[i]['local']
        estado = of.ofertas[i]['estado']
        tempo = of.ofertas[i]['tempo']
        moeda = of.ofertas[i]['moeda']
        for k in range(3):
            hotel = of.ofertas[i]['hoteis'][k]['nome']
            preco = of.ofertas[i]['hoteis'][k]['preco']
            locais.append(local)
            hoteis.append(hotel)
            precos.append(preco)
            estados.append(estado)
            tempos.append(tempo)
            moedas.append(moeda)

    return render_template('home.html', locais=locais, hoteis=hoteis, precos=precos, estados=estados, tempos=tempos, moedas=moedas)

@app.route("/viagens")
def viagens():
    if 'email' not in session:
        return redirect('/login')
    return render_template('viagens.html')

@app.route("/favoritos")
def favoritos():
    if 'email' not in session:
        return redirect('/login')
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
                        return redirect('/')
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
        return redirect('/login')
    return render_template('profile.html', email = session['email'], user = session['user'], cel = session['celular'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('email', None)
    return redirect('/')

@app.route('/pesquisar', methods=['GET'])
def pesquisar():
    return """<head><title>Aterrissar.com</title></head>oi"""

@app.route('/explore/rj/copacabana/hilton')
def hilton():
    cep = 22011010
    link = f'https://brasilapi.com.br/api/cep/v1/{cep}'
    info = requests.get(link).json()
    return render_template('hilton.html', info=info)