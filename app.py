import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'zip'}

# Garantir que a pasta de uploads existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função para checar se a extensão é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota para listar os arquivos ZIP
@app.route('/')
def index():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    return render_template('index.html', files=files)

# Rota para baixar o arquivo
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Rota para fazer upload do arquivo
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado.", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "Nenhum arquivo selecionado.", 400

    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return f"Arquivo {filename} enviado com sucesso!", 200
    else:
        return "Formato de arquivo não permitido.", 400

# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
