'''import csv

# Arquivo de entrada e saída
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
import csv

input_file = 'DataCSV/games.csv'
output_file = 'newgames.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

    header = next(reader)
    writer.writerow(["app_id", "name", "release_date", "is_free", "type"])

    for row in reader:
        try:
            # Garante que a linha tem pelo menos 5 colunas
            if len(row) < 5:
                continue
            # Pega os 4 primeiros campos + o último (type)
            new_row = [row[0], row[1], row[2], row[3], row[-1]]
            writer.writerow(new_row)
        except Exception as e:
            print(f"Erro ao processar linha: {row}\n{e}")
            continue

print(f"Arquivo salvo como {output_file}")