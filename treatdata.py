'''
# Tratar o arquivo promotional.csv / Remover as colunas de video e screenshots

import csv

input_file = 'DataCSV/promotional.csv'
output_file = 'newpromotional.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = ['app_id', 'header_image', 'background_image']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

    writer.writeheader()
    for row in reader:
        new_row = {key: row.get(key, "") for key in fieldnames}
        writer.writerow(new_row)

print("Arquivo salvo como", output_file)
'''

'''
#Tratar o arquivo games.csv / Remover as colunas de preço

import re

# Caminhos dos arquivos
entrada_csv = 'DataCSV/games.csv'
saida_csv = 'DataCSV/games_limpo.csv'

# Expressão regular para remover conteúdo dentro de chaves, mantendo as chaves
regex_chaves = re.compile(r'\{.*?\}')

with open(entrada_csv, 'r', encoding='utf-8') as entrada, \
     open(saida_csv, 'w', encoding='utf-8') as saida:

    for linha in entrada:
        linha_limpa = regex_chaves.sub('{}', linha)  # Substitui conteúdo das chaves por {}
        saida.write(linha_limpa)

print("CSV criado com conteúdo das chaves limpo.")
'''

'''
#Tratar o arquivo reviews.csv / Organizar a coluna de reviews

import csv

def corrigir_csv_v2(input_file, output_file):
    """
    Corrige as linhas quebradas em um arquivo CSV e adiciona aspas aos campos.

    Args:
        input_file (str): O caminho para o arquivo CSV de entrada.
        output_file (str): O caminho para o arquivo CSV de saída corrigido.
    """
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL) # Adiciona aspas a todos os campos
        header = next(reader)  # Lê o cabeçalho
        writer.writerow(header)

        linha_acumulada = []
        num_colunas_esperado = len(header)

        for row in reader:
            linha_acumulada.extend(row)
            if len(linha_acumulada) == num_colunas_esperado:
                writer.writerow(linha_acumulada)
                linha_acumulada = []
            elif len(linha_acumulada) > num_colunas_esperado:
                print(f"Aviso: Linha com mais colunas que o esperado. Ignorando o excesso: {linha_acumulada}")
                writer.writerow(linha_acumulada[:num_colunas_esperado])
                linha_acumulada = []

        # Se sobrar algo na linha_acumulada no final do arquivo
        if linha_acumulada:
            print(f"Aviso: Fim do arquivo com linha incompleta: {linha_acumulada}")
            writer.writerow(linha_acumulada)

if __name__ == "__main__":
    arquivo_entrada = 'DataCSV/reviews.csv'
    arquivo_saida = 'review_corrigido.csv'
    corrigir_csv_v2(arquivo_entrada, arquivo_saida)
    print(f"Arquivo corrigido '{arquivo_saida}' gerado com sucesso.")
'''