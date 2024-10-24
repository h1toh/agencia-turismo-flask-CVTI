from app import app
from flask import redirect, request, render_template, flash, session, jsonify
import json, os, app.ofer as of, requests, math, uuid
import datetime

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

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


    public_ip_link = 'https://api.ipify.org/'
    public_ip = requests.get(public_ip_link).text
    # IP Público do usuário 

    geolocation_link = f'http://ip-api.com/json/{public_ip}'
    geolocation_api = requests.get(geolocation_link).json()
    # Geolocalização do usuário

    user_lat = geolocation_api['lat'] 
    user_lon = geolocation_api['lon']
    user_city = geolocation_api['city']
    # Latitude e longitude do usuário

    copacabana_lat = -22.970722
    copacabana_lon = -43.182365

    paraty_lat = -23.2167
    paraty_lon = -44.7179

    petropolis_lat = -22.5046
    petropolis_lon = -43.1823

    def haversine(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        # Graus para radianos

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        #Diferença entre lat. e lon.

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
        # Fórmula de haversine

        R = 6371.0
        # Raio de Terra em km

        distancia = R*c
        return distancia

    copacabana_distance = math.floor(haversine(copacabana_lat,copacabana_lon,user_lat,user_lon))
    paraty_distance = math.floor(haversine(paraty_lat,paraty_lon,user_lat,user_lon))
    petropolis_distance = math.floor(haversine(petropolis_lat,petropolis_lon,user_lat,user_lon))

    return render_template('home.html', locais=locais, hoteis=hoteis, precos=precos, estados=estados, tempos=tempos, moedas=moedas, petropolis_distance=petropolis_distance, copacabana_distance=copacabana_distance, paraty_distance=paraty_distance)

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

@app.route('/explore/rj/copacabana/hilton')
def hilton():
    cep = 22011010
    link = f'https://brasilapi.com.br/api/cep/v1/{cep}'
    info = requests.get(link).json()
    return render_template('hilton.html', info=info)

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
    nova_avaliacao = dict(hospedagem = hospedagem,nome=session['nome'],sobrenome=session['sobrenome'],comentario=user_comentario, data_envio=data_agora)

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

@app.route('/reservas')
def reserva():
    return 'wip'






