# conding: utf-8

from flask import Flask, flash, render_template, redirect, request, send_from_directory, url_for
import requests
import os
from dotenv import load_dotenv
from control.contador import inicializar_contador, obter_contadores, atualizar_contadores
from control.email_function import Contato, send_email





# inicia o dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')



# Inicializa o contador ao iniciar o app
inicializar_contador()


@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)  # Obtém o IP "REAL" do visitante
    # Atualiza o contador de visitantes
    atualizar_contadores(visitas=1, ip=ip)
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
        # 1. Pega os dados do formulário
        nome = request.form.get('name', '')
        email = request.form.get('email', '')
        mensagem = request.form.get('message', '')

        # 2. Pega o token do reCAPTCHA
        recaptcha_response = request.form.get('g-recaptcha-response')
        secret_key = os.getenv('RECAPTCHA_SECRET_KEY')  # coloque sua chave no .env!

        # 3. Verifica com o Google se o token é válido
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': secret_key,
            'response': recaptcha_response
        }

        r = requests.post(verify_url, data=payload)
        result = r.json()

        # 4. Verifica resposta
        if not result.get('success'):
            flash('Verificação reCAPTCHA falhou. Tente novamente.', 'danger')
            return redirect(url_for('mapa'))

        # 5. Se passou, envia o e-mail
        contato = Contato(nome, email, mensagem)
        try:
            send_email(contato)
            flash('Mensagem enviada! Obrigado!', 'success')
        except Exception as e:
            print(f"Erro ao enviar e-mail: {str(e)}")   
            flash(f'Erro de envio: {str(e)}', 'danger')
            return redirect(url_for('mapa'))

    return redirect(url_for('index'))

     

    
"""
 Rota para o download dos contos
"""

@app.route('/download/<filename>')
def download_file(filename):
    ip = request.remote_addr  # Obtém o IP do visitante
    # Atualiza o contador de visitantes
    atualizar_contadores(downloads=1, ip=ip)
    return send_from_directory('static/download', filename)


@app.route('/status')
def status():
    visitantes, downloads, visitas = obter_contadores()
    return render_template('status.html', visitantes=visitantes, downloads=downloads, visitas=visitas)

if __name__ == '__main__':
	app.run(debug=True)

