# conding: utf-8

from flask import Flask, flash, render_template, redirect, request, send_from_directory, url_for
import requests
from flask_recaptcha import ReCaptcha 
from control.email_function import send_email, Contato
import os
from dotenv import load_dotenv
from control.contador import inicializar_contador, obter_contadores, atualizar_contadores


# inicia o dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


# Configura as chaves do ReCaptcha no app.config
app.config['RECAPTCHA_SITE_KEY'] = os.getenv('RECAPTCHA_SITE_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = os.getenv('RECAPTCHA_SECRET_KEY')


# Inicializa o ReCaptcha
recaptcha = ReCaptcha(app=app)


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
    recaptcha_site_key = app.config['RECAPTCHA_SITE_KEY'] 
    recaptcha_secret_key = app.config['RECAPTCHA_SECRET_KEY'] 
    print(recaptcha_site_key, recaptcha_secret_key)  
    return render_template('mapa.html', recaptcha_site_key=recaptcha_site_key)


@app.route('/termosuso')
def termosuso():
	return render_template('useterms.html')

@app.route('/politica')
def politica():
	return render_template('p_privacy.html')



@app.route('/send', methods=['POST'])
def send():    
    if request.method == 'POST': 

        # Recebe o token do Turnstile
        turnstile_token = request.form['cf-turnstile-response'] 
            
        # Pegue o token reCAPTCHA enviado pelo formulário
        turnstile_token = request.form['cf-turnstile-response']  
        recaptcha_secret_key = app.config['RECAPTCHA_SECRET_KEY'] 

        

        # Validação da resposta no Cloudflare
        verification_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
        response = requests.post(verification_url, data={
            'secret': recaptcha_secret_key,
            'response': turnstile_token
        })

        result = response.json()     


        nome = request.form.get('name', '')   # Garantimos que sempre terá um valor, 
        email = request.form.get('email', '') # mesmo que seja uma string vazia
        mensagem = request.form.get('message', '')

            

        # Se o hCaptcha for validado, continua o processamento do formulário
        if result.get('success'):
            nome = request.form['name']
            email = request.form['email']
            mensagem = request.form['message']
            contato = Contato(nome, email, mensagem)

            try:
                send_email(contato)  # Envia o e-mail com os dados do contato
                flash('Mensagem enviada! Obrigado!', 'success')  # Flash de sucesso
            except Exception as e:
                flash(f'Erro de envio: {str(e)}', 'danger') 
                return redirect(url_for('mapa')) # Flash de erro em caso de falha no envio
        else:
            # Se o reCAPTCHA falhar, exiba uma mensagem de erro
            flash('Falha na verificação do reCAPTCHA. Tente novamente.', 'danger')
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

