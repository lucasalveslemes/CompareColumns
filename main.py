import pandas as pd  # Importa a biblioteca pandas para manipulação de dados, principalmente DataFrames.
import os          # Importa a biblioteca os para realizar operações com o sistema de arquivos (como verificar existência de arquivos).

def read_columns(file_path, delimiter=None):
    """
    Lê as colunas (cabeçalho) do arquivo.
    Para arquivos CSV, se o cabeçalho não for separado corretamente (ou seja, for lido como uma única coluna contendo o delimitador),
    a função realiza a separação manual utilizando o delimitador informado.
    
    Parâmetros:
      file_path: Caminho do arquivo.
      delimiter: Caractere separador (padrão é vírgula).
    
    Retorna:
      As colunas (cabeçalho) do arquivo.
    """
    # Obtém a extensão do arquivo em letras minúsculas (e.g., .csv, .xlsx)
    file_extension = os.path.splitext(file_path)[1].lower()
    
    # Se o arquivo for um Excel (extensão .xlsx ou .xls)
    if file_extension in ['.xlsx', '.xls']:
        # Lê apenas o cabeçalho do arquivo Excel e retorna suas colunas
        return pd.read_excel(file_path, nrows=0).columns

    # Se o arquivo for CSV
    elif file_extension == '.csv':
        # Lê o cabeçalho do CSV usando o delimitador informado; nrows=0 indica que só queremos a primeira linha (cabeçalho)
        df = pd.read_csv(file_path, delimiter=delimiter, nrows=0)
        # Armazena as colunas lidas do DataFrame
        cols = df.columns
        
        # Caso o cabeçalho não tenha sido separado corretamente:
        # Se houver apenas uma coluna e o delimitador estiver presente na string, significa que o cabeçalho está junto
        if len(cols) == 1 and delimiter is not None and delimiter in cols[0]:
            # Divide a string usando o delimitador e remove espaços em branco extras de cada coluna
            cols = [c.strip() for c in cols[0].split(delimiter)]
        # Retorna as colunas obtidas
        return cols

    # Se o arquivo não for Excel nem CSV, gera um erro com mensagem informativa
    else:
        raise ValueError("Informe arquivos em Excel (.xlsx, .xls) ou CSV (.csv).")

def compare_files(model_file, new_file, delimiter_model=None, delimiter_new=None):
    """
    Compara as colunas de dois arquivos (modelo e novo), verificando se possuem as mesmas colunas e se estão na mesma ordem.
    
    Parâmetros:
      model_file: Caminho do arquivo base (modelo).
      new_file: Caminho do novo arquivo a ser comparado.
      delimiter_model: Delimitador para o arquivo modelo (se for CSV).
      delimiter_new: Delimitador para o novo arquivo (se for CSV).
      
    Exibe:
      Mensagens informando se as colunas são iguais, se a ordem está correta ou quais colunas foram adicionadas/removidas.
    """
    # Chama a função read_columns para ler as colunas do arquivo modelo, utilizando o delimitador específico se informado
    model_columns = read_columns(model_file, delimiter_model)
    # Chama a função read_columns para ler as colunas do novo arquivo, utilizando o delimitador específico se informado
    new_columns = read_columns(new_file, delimiter_new)

    # Compara os conjuntos de colunas (desconsiderando a ordem) para verificar se são iguais
    if set(new_columns) == set(model_columns):
        print("✅ As colunas são as mesmas.")
        # Se a ordem das colunas também for a mesma, informa que a ordem está correta
        if list(model_columns) == list(new_columns):
            print("✅ A ordem é a mesma!")
        else:
            # Caso contrário, alerta que a ordem está diferente
            print("⚠️ As colunas não estão na mesma ordem!")
    else:
        # Se os conjuntos de colunas forem diferentes, identifica as colunas removidas e adicionadas
        removed_columns = set(model_columns) - set(new_columns)
        added_columns = set(new_columns) - set(model_columns)
        if removed_columns:
            print(f"Colunas que não estão na nova fonte: {removed_columns}")
        if added_columns:
            print(f"Colunas adicionadas na nova fonte: {added_columns}")

def valid_file(prompt):
    """
    Solicita que o usuário informe o caminho de um arquivo e verifica se ele existe.
    
    Parâmetros:
      prompt: Mensagem exibida ao usuário solicitando o caminho do arquivo.
      
    Retorna:
      O caminho do arquivo informado, caso ele exista.
    """
    while True:
        # Solicita o caminho do arquivo e remove espaços em branco adicionais no início/fim
        file_path = input(prompt).strip()
        # Se o caminho estiver entre aspas, remove as aspas do início e do fim
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]
        # Verifica se o arquivo existe na localização informada
        if os.path.exists(file_path):
            return file_path
        else:
            # Caso o caminho não seja válido, informa o usuário e pede para inserir novamente
            print("Caminho inválido! Por favor, insira o caminho correto do arquivo.")
            print("Exemplo: C:\\Users\\seu_usuario\\Desktop\\seuarquivo.xlsx")

# Solicita ao usuário o caminho da base antiga (modelo)
model_file = valid_file("Informe o caminho da base antiga: ")
# Solicita ao usuário o caminho da base nova
new_file = valid_file("Informe o caminho da base nova: ")

# Exemplo de chamada:
# Informar os delimitadores caso sejam csv. Exemplo se for vírgula: delimiter_model=',', delimiter_new=','
compare_files(model_file, new_file, delimiter_model=None, delimiter_new=None)
