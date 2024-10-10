from app import app
from flask import flash, redirect, request, render_template

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/viagens")
def viagens():
    return render_template('viagens.html')

@app.route("/favoritos")
def favoritos():
    return render_template('favoritos.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/auth", methods=['POST'])
def auth():
    email = request.form.get('email')
    senha = request.form.get('senha')

    if email == 'admin@admin.com' and senha == 'admin':
        return f"email {email} e senha {senha}"
    else:
        flash("Email ou senha inválido.")
        return redirect('/login')

