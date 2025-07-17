# conding: utf-8

from flask import Flask, flash, render_template, redirect, request, send_from_directory, url_for
import requests
import os
from dotenv import load_dotenv
from control.contador import inicializar_contador, obter_contadores, atualizar_contadores, iniciar_pingador
from control.email_function import Contato, send_email






# inicia o dotenv
load_dotenv()


# Inicia o pingador em background
iniciar_pingador()


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
    return render_template('mapa.html', recaptcha_site_key=os.getenv('RECAPTCHA_SITE_KEY'))

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
        secret_key = os.getenv('RECAPTCHA_SECRET_KEY')

        # Verifica se o token reCAPTCHA foi enviado
        if not recaptcha_response:
            flash('Por favor, complete a verificação reCAPTCHA.', 'danger')
            return redirect(url_for('mapa'))

        # Verifica se a chave secreta está configurada
        if not secret_key:
            flash('Erro de configuração do servidor. Tente novamente mais tarde.', 'danger')
            return redirect(url_for('mapa'))

        # 3. Verifica com o Google se o token é válido
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': secret_key,
            'response': recaptcha_response,
            'remoteip': request.remote_addr
        }

        try:
            r = requests.post(verify_url, data=payload, timeout=10)
            result = r.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar com reCAPTCHA: {str(e)}")
            flash('Erro de conexão com o serviço de verificação. Tente novamente.', 'danger')
            return redirect(url_for('mapa'))

        # 4. Verifica resposta
        if not result.get('success'):
            error_codes = result.get('error-codes', [])
            print(f"reCAPTCHA falhou com códigos de erro: {error_codes}")
            
            # Mensagens específicas para cada tipo de erro
            if 'invalid-input-secret' in error_codes:
                flash('Erro de configuração do reCAPTCHA. Contate o administrador.', 'danger')
            elif 'invalid-input-response' in error_codes:
                flash('Token reCAPTCHA inválido. Tente novamente.', 'danger')
            elif 'timeout-or-duplicate' in error_codes:
                flash('reCAPTCHA expirado. Recarregue a página e tente novamente.', 'danger')
            else:
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
    # Em produção, use: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
    app.run(debug=True)

