import zipfile
import os
from datetime import datetime, timedelta

# Função para copiar arquivos e compactar apenas os que foram criados no mês passado
def copy_and_compress(source_folder, output_zip):
    print(f"Compactando arquivos da pasta: {source_folder}")
    now = datetime.now()
    first_day_current_month = datetime(now.year, now.month, 1)
    last_day_last_month = first_day_current_month - timedelta(days=1)
    first_day_last_month = datetime(last_day_last_month.year, last_day_last_month.month, 1)

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_creation_time = os.path.getctime(file_path)
                creation_date = datetime.fromtimestamp(file_creation_time)

                if first_day_last_month <= creation_date < first_day_current_month:
                    print(f"Adicionando ao ZIP: {file_path}")
                    zipf.write(file_path, os.path.relpath(file_path, source_folder))
    
    print(f"Arquivo ZIP gerado: {output_zip}")

# Função principal de backup
def backup_and_upload():
    try:
        with open("caminho_pasta.txt", "r") as f:
            source_folder = f.read().strip()
    except FileNotFoundError:
        print("Erro: o arquivo com o caminho da pasta não foi encontrado.")
        return

    if not os.path.exists(source_folder):
        print(f"Erro: a pasta {source_folder} não existe.")
        return

    output_zip = f'C:\\Users\\Suporte F5\\Documents\\Fernando\\Salvador de XML\\uploads\\backup_{datetime.now().strftime("%Y%m%d")}.zip'
    
    # Copiar e compactar
    copy_and_compress(source_folder, output_zip)
    
    print(f"Backup feito e enviado: {datetime.now()}")

# Executar o backup
backup_and_upload()
