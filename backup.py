import zipfile
import os
import requests
from datetime import datetime, timedelta
import schedule
import time

# Função para copiar arquivos e compactar apenas os que foram criados no mês passado
def copy_and_compress(source_folder, output_zip):
    print(f"Compactando arquivos da pasta: {source_folder}")

    # Calcula o mês e ano do mês passado
    now = datetime.now()
    first_day_current_month = datetime(now.year, now.month, 1)
    last_day_last_month = first_day_current_month - timedelta(days=1)
    first_day_last_month = datetime(last_day_last_month.year, last_day_last_month.month, 1)

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                # Verifica a data de criação do arquivo
                file_creation_time = os.path.getctime(file_path)
                creation_date = datetime.fromtimestamp(file_creation_time)
                
                # Verifica se o arquivo foi criado no mês passado
                if first_day_last_month <= creation_date < first_day_current_month:
                    print(f"Adicionando ao ZIP: {file_path}")  # Log de depuração
                    zipf.write(file_path, os.path.relpath(file_path, source_folder))
    
    print(f"Arquivo ZIP gerado: {output_zip}")

# Função para fazer upload do arquivo compactado
def upload_file(url, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            try:
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    print("Upload feito com sucesso!")
                else:
                    print(f"Erro no upload: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão: {e}")
    else:
        print(f"Arquivo {file_path} não encontrado para upload.")

# Função principal de backup
def backup_and_upload():
    source_folder = r'C:\Users\Suporte F5\Desktop'  # Corrija o caminho aqui
    output_zip = f'C:\\Users\\Suporte F5\\Documents\\backup_{datetime.now().strftime("%Y%m%d")}.zip'
    
    # Copiar e compactar
    copy_and_compress(source_folder, output_zip)
    
    # Fazer upload
    upload_url = 'http://127.0.0.1:5000/upload'  # URL do site Flask
    upload_file(upload_url, output_zip)
    print(f"Backup feito e enviado: {datetime.now()}")

# Agendar a execução a cada 30 dias
def schedule_backup():
    print("Agendando backup para rodar a cada 30 dias...")
    schedule.every(30).days.do(backup_and_upload)

    while True:
        schedule.run_pending()
        time.sleep(1)  # Esperar até a próxima verificação de agendamentos

if __name__ == "__main__":
    backup_and_upload()  # Testar o upload diretamente
