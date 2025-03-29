import pandas as pd
import os

# Função para ler as colunas
def read_columns(file_path):
    # Pega a extensão
    file_extension = os.path.splitext(file_path)[1].lower()  # Obter a extensão do arquivo

    # Se for .xlsx ou .xls
    if file_extension in ['.xlsx', '.xls']:
        return pd.read_excel(file_path, nrows=0).columns  # Só lê o cabeçalho

    # Se for CSV
    elif file_extension == '.csv':
        return pd.read_csv(file_path, nrows=0).columns  # Só lê o cabeçalho
    
    # Se não for nenhuma das duas lenvanta uma exceção
    else:
        raise ValueError("Informe arquivos em Excel (.xlsx, .xls) ou CSV (.csv).") # interrompe caso uma exceção/erro aconteça

# Função para comparar as colunas de dois arquivos
def compare_files(model_file, new_file):
    model_columns = read_columns(model_file)
    new_columns = read_columns(new_file)

    if set(new_columns) == set(model_columns):
        print("As colunas são as mesmas.")

        if list(model_columns) == list(new_columns):
            print("A ordem é a mesma!")
        else: 
            print("Não está na mesma ordem!")
    else:
        removed_columns = set(model_columns) - set(new_columns)
        added_columns = set(new_columns) - set(model_columns)

        if removed_columns:
            print(f"Colunas que não tem na nova fonte: {removed_columns}")

        if added_columns:
            print(f"Colunas adicionadas na nova fonte: {added_columns}")


def valid_file(prompt):
    while True:
        file_path = input(prompt).strip()  # Remove espaços em branco e aspas
        # Remove as aspas duplas
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]  # Remove as aspas do começo e do final

        if os.path.exists(file_path):
            return file_path
        else:
            print("Caminho inválido! Por favor, insira o caminho correto do arquivo.")
            print("Exemplo de caminho correto: C:\\Users\\seu_usuario\\Desktop\\seuarquivo.xlsx")


# Primeiro, pede os caminhos dos arquivos
model_file = valid_file("Informe o caminho da base antiga: ")
new_file = valid_file("Informe o caminho da base nova: ")

# Depois chama a função para comparar as colunas
compare_files(model_file, new_file)
