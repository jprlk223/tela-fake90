from flask import Flask, render_template_string, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///compras.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto = db.Column(db.String(100))
    cep = db.Column(db.String(15))
    forma_pagamento = db.Column(db.String(30))
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    cpf = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    cartao = db.Column(db.String(25))
    validade = db.Column(db.String(10))
    cvv = db.Column(db.String(5))
    chave_pix = db.Column(db.String(100))
    data = db.Column(db.DateTime, server_default=db.func.now())

@app.route('/')
def index():
    with open('index.html', encoding='utf-8') as f:
        return render_template_string(f.read())

@app.route('/checkout', methods=['POST'])
def checkout():
    dados = request.form
    nova = Compra(
        produto=dados['produto'],
        cep=dados['cep'],
        forma_pagamento=dados['forma_pagamento'],
        nome=dados['nome'],
        email=dados['email'],
        cpf=dados['cpf'],
        endereco=dados['endereco'],
        cartao=dados.get('cartao'),
        validade=dados.get('validade'),
        cvv=dados.get('cvv'),
        chave_pix=dados.get('chave_pix')
    )
    db.session.add(nova)
    db.session.commit()
    return "<h2>✅ Pedido realizado com sucesso!</h2><p><a href='/'>Voltar</a></p>"

@app.route('/admin')
def admin():
    registros = Compra.query.order_by(Compra.data.desc()).all()
    html = "<h1>🗂️ Compras Recebidas</h1><ul>"
    for r in registros:
        html += f"<li><b>{r.produto}</b> | {r.nome} | CPF: {r.cpf} | {r.email} | Pagamento: {r.forma_pagamento}"
        if r.cartao:
            html += f" | 💳 Cartão: {r.cartao} | Validade: {r.validade} | CVV: {r.cvv}"
        if r.chave_pix:
            html += f" | PIX: {r.chave_pix}"
        html += "</li>"
    html += "</ul>"
    return html

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
