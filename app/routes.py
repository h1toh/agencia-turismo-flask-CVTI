from app import app
from flask import redirect, request, render_template, flash, session, jsonify
import json, os, uuid
import datetime

app.secret_key = 'CVTI'

@app.route("/")
def loading():
    return render_template('loading.html')


@app.route("/home")
def home():
    with open('app/info.json','r',encoding='utf-8') as of:
        ofertas = json.load(of)

    hoteis = []
    precos = []
    locais = []
    estados = []
    tempos = []
    moedas = []

    for i in range(5):
        local = ofertas[i]['local']
        estado = ofertas[i]['estado']
        tempo = ofertas[i]['tempo']
        moeda = ofertas[i]['moeda']
        for k in range(3):
            hotel = ofertas[i]['hoteis'][k]['nome']
            preco = ofertas[i]['hoteis'][k]['preco']
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
                        session['nome'] = c['nome']
                        session['sobrenome'] = c['sobrenome']
                        session['email'] = c['email']
                        session['celular'] = c['celular']
                        session['user_uuid'] = c['user_uuid']
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
    sobrenomeSignup = request.form.get('sobrenome')
    emailSignup = request.form.get('email')
    celularSignup = request.form.get('celular')
    senhaSignup = request.form.get('senha')
    user_uuid = str(uuid.uuid4())
    nova_conta = dict(nome=nomeSignup, sobrenome=sobrenomeSignup, email=emailSignup, celular=celularSignup, senha=senhaSignup, user_uuid=user_uuid)

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
    return render_template('profile.html', email = session['email'], nome = session['nome'], sobrenome = session['sobrenome'], cel = session['celular'], user_uuid = session['user_uuid'])

@app.route('/logout')
def logout():
    session.pop('nome', None)
    session.pop('sobrenome', None)
    session.pop('email', None)
    session.pop('celular', None)
    session.pop('user_uuid', None)
    return redirect('/')

@app.route('/pesquisar', methods=['GET'])
def pesquisar():
    return """<head><title>Aterrissar.com</title></head>oi"""

with open('app/data.json', 'r', encoding='utf-8') as f:
    hotels_data = json.load(f)


@app.route('/viagens/<hot>')
def explore(hot):
    if hot in hotels_data:
        hotel_info = hotels_data[hot]
        lat = hotel_info['lat']
        lon = hotel_info['lon']
        rua = hotel_info['rua']
        preco = hotel_info['preco']
        des = hotel_info['info']
        nome_hosp = hotel_info['nome']
    return render_template('explore.html', lon=lon, lat=lat, hot=hot, nome_hosp=nome_hosp, rua=rua, preco=preco, des=des)

def carregar_avaliacoes():
    with open('app/avaliacao.json', 'r', encoding='utf-8') as file:
        avaliacoes = json.load(file)
    return avaliacoes

@app.route('/avaliacao/<hospedagem>')
def notas(hospedagem):
    avaliacoes = carregar_avaliacoes()

    avaliacoes_filtradas = [
        avaliacao for avaliacao in avaliacoes if avaliacao['hospedagem'].lower() == hospedagem.lower()
    ]

    nome = session.get('nome', 'Usuário')  # 'Usuário' é o valor padrão caso 'nome' não esteja presente
    sobrenome = session.get('sobrenome', '')
    
    return render_template('notas.html', nome = nome, sobrenome = sobrenome,avaliacoes=avaliacoes_filtradas, hospedagem = hospedagem)

@app.route('/enviarnota', methods=['POST'])
def enviarnota():
    data_agora = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    user_comentario = request.form.get('comentario')
    hospedagem = request.form.get('hospedagem')
    if not user_comentario:
        return redirect(f'/avaliacao/{hospedagem}')
    rating = request.form.get('rating')
    nova_avaliacao = dict(hospedagem = hospedagem,nome=session['nome'],sobrenome=session['sobrenome'],comentario=user_comentario, data_envio=data_agora, rating=rating)

    try:
        if os.path.exists('app/avaliacao.json'):
            with open('app/avaliacao.json','r') as aval:
                avaliacao = json.load(aval)
        else:
            avaliacao = []
        avaliacao.append(nova_avaliacao)

        with open('app/avaliacao.json','w') as aval:
            json.dump(avaliacao, aval, indent=4, ensure_ascii=False)
        return redirect(f'/avaliacao/{hospedagem}')
    except:
        return redirect(f'/avaliacao/{hospedagem}')


paises = [
            "Afeganistão", "África do Sul", "Alemanha", "Arábia Saudita", "Argentina", 
            "Austrália", "Bélgica", "Bolívia", "Brasil", "Canadá", "Chile", "China", 
            "Colômbia", "Coreia do Norte", "Coreia do Sul", "Cuba", "Dinamarca", "Egito", 
            "Emirados Árabes Unidos", "Espanha", "Estados Unidos", "Filipinas", "Finlândia", 
            "França", "Grécia", "Holanda", "Índia", "Indonésia", "Irlanda", "Israel", 
            "Itália", "Japão", "México", "Noruega", "Nova Zelândia", "Panamá", "Paraguai", 
            "Peru", "Polônia", "Portugal", "Reino Unido", "Rússia", "Suécia", "Suíça", 
            "Tailândia", "Turquia", "Ucrânia", "Uruguai", "Venezuela", "Vietnã"
        ]

@app.route('/reserva', methods = ['POST'])
def reserva():
    if 'email' not in session:
        return redirect('/login')
    
    hospedagem = request.form.get('hospedagem')
    preco = request.form.get('preco')
    endereco = request.form.get('endereco')

    if hospedagem == None:
        return redirect('home.html')
    
    pais_selecionado = "Brasil"

    return render_template('reserva.html', hospedagem=hospedagem, preco=preco, endereco=endereco, paises = paises, pais_selecionado = pais_selecionado)

@app.route('/concluido', methods = ['POST'])
def concluir():
    if 'email' not in session:
        return redirect('/login')
    
    hospedagem = request.form.get('hospedagem')
    preco = request.form.get('preco')
    endereco = request.form.get('endereco')

    return render_template('concluido.html')
    
