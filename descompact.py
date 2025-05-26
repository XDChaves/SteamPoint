# descompactador.py
import zipfile
import os
import glob

# --- Configuração ---
pasta_origem = 'CSVzip'
pasta_destino = 'DataCSV'
# --------------------

def descompactar_todos_zips(origem, destino):
    """
    Descompacta todos os arquivos .zip de uma pasta de origem para uma pasta de destino,
    somente se a pasta de destino estiver vazia ou não existir.
    """

    # 1. Verifica se a pasta de origem existe
    if not os.path.isdir(origem):
        print(f"Erro: A pasta de origem '{origem}' não foi encontrada.")
        print("Por favor, crie a pasta 'CSVzip' e coloque seus arquivos .zip nela.")
        return

    # 2. Verifica a pasta de destino
    if os.path.isdir(destino):
        # Se existe, verifica se está vazia
        # os.listdir() retorna uma lista com os nomes dos arquivos/pastas
        if os.listdir(destino): # Se a lista NÃO for vazia...
            print(f"Aviso: A pasta de destino '{destino}' já existe e NÃO está vazia.")
            print("Nenhum arquivo será descompactado.")
            return # <<<--- Sai da função se a pasta não estiver vazia
        else:
            print(f"Pasta de destino '{destino}' existe e está vazia. Prosseguindo...")
    else:
        # Se não existe, cria
        os.makedirs(destino, exist_ok=True)
        print(f"Pasta de destino '{destino}' criada.")

    # 3. Encontra todos os arquivos .zip na pasta de origem
    caminho_pesquisa = os.path.join(origem, '*.zip')
    arquivos_zip = glob.glob(caminho_pesquisa)

    # 4. Verifica se encontrou algum arquivo .zip
    if not arquivos_zip:
        print(f"Nenhum arquivo .zip encontrado na pasta '{origem}'.")
        return

    print(f"\nIniciando a descompactação de {len(arquivos_zip)} arquivo(s):")

    # 5. Itera sobre cada arquivo .zip encontrado
    for caminho_zip in arquivos_zip:
        nome_arquivo = os.path.basename(caminho_zip)
        print(f"  -> Descompactando '{nome_arquivo}'...")

        try:
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                zip_ref.extractall(destino)
            print(f"     '{nome_arquivo}' descompactado com sucesso para '{destino}'.")

        except zipfile.BadZipFile:
            print(f"     Erro: O arquivo '{nome_arquivo}' não é um zip válido ou está corrompido.")
        except Exception as e:
            print(f"     Erro inesperado ao descompactar '{nome_arquivo}': {e}")

    print("\nProcesso de descompactação concluído!")

# Esta parte só executa se você rodar 'python descompactador.py' diretamente
if __name__ == "__main__":
    descompactar_todos_zips(pasta_origem, pasta_destino)