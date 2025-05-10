#Análise e tratamento de dados de apps da steam.

###EXTRAIR OS DADOS EM ZIP E COLOCAR NA PASTA DataCSV

*Dar uma olhada no descriptions.csv e games.csv:

-Organizar os dados de descriptions.csv:
ddesc = pd.read_csv('.\\DataCSV\\descriptions.csv', sep=',',on_bad_lines='warn')
desc_filtred=ddesc[ddesc["summary"]!=r"\N"]
desc_filtred

-Organizar os dados e remover "price_overview" e "languages" de games.csv:
dgames = pd.read_csv('.\\DataCSV\\games.csv', sep=',',on_bad_lines='warn')
dgames

