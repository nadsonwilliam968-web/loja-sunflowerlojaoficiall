from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = '123456'

def conectar():
    return sqlite3.connect('banco.db')

def criar():
    con = conectar()
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY, nome TEXT, preco REAL)')
    con.commit()
    con.close()

criar()

@app.route('/')
def loja():
    con = conectar()
    produtos = con.execute('SELECT * FROM produtos').fetchall()
    con.close()
    return render_template('loja.html', produtos=produtos)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['senha'] == '1234':
            session['logado'] = True
            return redirect('/admin')
    return render_template('login.html')

@app.route('/admin', methods=['GET','POST'])
def admin():
    if not session.get('logado'):
        return redirect('/login')

    con = conectar()
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        con.execute('INSERT INTO produtos (nome, preco) VALUES (?,?)', (nome, preco))
        con.commit()

    produtos = con.execute('SELECT * FROM produtos').fetchall()
    con.close()
    return render_template('admin.html', produtos=produtos)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
