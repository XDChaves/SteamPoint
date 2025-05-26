# start.py
import subprocess
import sys
from descompact import descompactar_todos_zips, pasta_origem, pasta_destino

print("="*30)
print(" Executando script de descompactação...")
print("="*30)

# 1. Executa a função de descompactação
descompactar_todos_zips(pasta_origem, pasta_destino)

print("\n" + "="*30)
print(" Iniciando o servidor Flask...")
print("="*30)

# 2. Executa o comando 'flask run'
#    Usamos 'sys.executable' para garantir que está usando o python do poetry
#    '-m flask' é mais robusto que apenas 'flask' em alguns ambientes
subprocess.run([sys.executable, '-m', 'flask', 'run'])