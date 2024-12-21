# conding: utf-8

from flask import Flask, flash, render_template, redirect, request, send_from_directory, url_for
import requests
from control.email_function import send_email, Contato
import os
from dotenv import load_dotenv
from control.contador import inicializar_contador, obter_contadores, atualizar_contadores


# inicia o dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


# Garantir que as variáveis de ambiente estejam no app.config
app.config['HCAPTCHA_SITE_KEY'] = os.getenv('HCAPTCHA_SITE_KEY')
app.config['HCAPTCHA_SECRET_KEY'] = os.getenv('HCAPTCHA_SECRET_KEY')


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
    ip = request.remote_addr  # Obtém o IP do visitante
    # Atualiza o contador de visitantes
    atualizar_contadores(visitas=1, ip=ip)
    return render_template('contos.html')


@app.route('/sonhar')
def sonhar():
    ip = request.remote_addr  # Obtém o IP do visitante
    # Atualiza o contador de visitantes
    atualizar_contadores(visitas=1, ip=ip)
    return render_template('sonhar.html')


@app.route('/mapa')
def mapa():
    ip = request.remote_addr  # Obtém o IP do visitante
    # Atualiza o contador de visitantes
    atualizar_contadores(visitas=1, ip=ip)
    hcaptcha_site_key = app.config['HCAPTCHA_SITE_KEY']
    return render_template('mapa.html', hcaptcha_site_key=hcaptcha_site_key)


@app.route('/termosuso')
def termosuso():
	return render_template('useterms.html')

@app.route('/politica')
def politica():
	return render_template('p_privacy.html')



@app.route('/send', methods=['POST'])
def send():    
    if request.method == 'POST':

        # Captura os dados do formulário antes da verificação do hCaptcha
        nome = request.form.get('name', '')   # Garantimos que sempre terá um valor, 
        email = request.form.get('email', '') # mesmo que seja uma string vazia
        mensagem = request.form.get('message', '')

        
        # Verifica a resposta do hCaptcha
        captcha_response = request.form.get('h-captcha-response')  # Note que o campo do hCaptcha tem um nome diferente

        # Se o hCaptcha não for preenchido, renderiza com um alerta
        if not captcha_response:
            flash('Por favor, complete o captcha!', 'danger')  # Flash de erro
            # Renderiza novamente a página do formulário com os valores preenchidos
            return render_template('mapa.html', hcaptcha_site_key=app.config['HCAPTCHA_SITE_KEY'], nome=nome, email=email, mensagem=mensagem)

        # Verifica a resposta do hCaptcha com a API do hCaptcha
        payload = {
            'secret': app.config['HCAPTCHA_SECRET_KEY'],  # Usa a chave secreta do hCaptcha
            'response': captcha_response
        }

        

        # Envia a requisição para verificar o hCaptcha
        response = requests.post('https://hcaptcha.com/siteverify', data=payload)
        result = response.json()

        # Se o hCaptcha não for validado, mostra erro
        if not result.get('success'):
            flash('Falha na verificação do captcha. Tente novamente.', 'danger')
            # Renderiza novamente a página do formulário com os valores preenchidos
            return render_template('mapa.html', hcaptcha_site_key=app.config['HCAPTCHA_SITE_KEY'], nome=nome, email=email, mensagem=mensagem)

        # Se o hCaptcha for validado, continua o processamento do formulário
        nome = request.form['name']
        email = request.form['email']
        mensagem = request.form['message']
        contato = Contato(nome, email, mensagem)

        try:
            send_email(contato)  # Envia o e-mail com os dados do contato
            flash('Mensagem enviada! Obrigado!', 'success')  # Flash de sucesso
        except Exception as e:
            flash(f'Erro de envio: {str(e)}', 'danger')  # Flash de erro em caso de falha no envio

    return redirect(url_for('index'))  # Redireciona para a página inicial após o envio


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

