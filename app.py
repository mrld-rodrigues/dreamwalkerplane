# conding: utf-8

from flask import Flask, flash, render_template, redirect, request, send_from_directory, url_for
from control.email_function import send_email, Contato
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/contos')
def contos():
	return render_template('contos.html')


@app.route('/sonhar')
def sonhar():
	return render_template('sonhar.html')


@app.route('/mapa')
def mapa():
	return render_template('mapa.html')

@app.route('/termosuso')
def termosuso():
	return render_template('useterms.html')

@app.route('/politica')
def politica():
	return render_template('p_privacy.html')


@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        nome = request.form['name']
        email = request.form['email']
        mensagem = request.form['message']        
        contato = Contato(nome, email, mensagem)        
        try:
            send_email(contato)
            flash('Mensagem enviada! Obrigado!', 'success')
        except Exception as e:
            flash(f'Erro de envio: {str(e)}', 'danger')
    return redirect(url_for('index'))


"""
 Rota para o download do arquivo CV.pdf
"""

@app.route('/download/conto_000.pdf')
def download_000(filename):
    return send_from_directory('static/download', filename)

@app.route('/download/conto_001.pdf')
def download_001(filename):
    return send_from_directory('static/download', filename)

@app.route('/download/conto_002.pdf')
def download_002(filename):
    return send_from_directory('static/download', filename)


if __name__ == '__main__':
	app.run(debug=True)

