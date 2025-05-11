<h1>Análise e tratamento de dados de apps da steam.</h1>

<h3>*EXTRAIR OS DADOS EM ZIP E COLOCAR NA PASTA DataCSV*</h3>

<h4>Dar uma olhada no descriptions.csv e games.csv:</h4>

<p>
-Organizar os dados de descriptions.csv:<br>
ddesc = pd.read_csv('.\\DataCSV\\descriptions.csv', sep=',',on_bad_lines='warn')<br>
desc_filtred=ddesc[ddesc["summary"]!=r"\N"]<br>
desc_filtred

-Organizar os dados e remover "price_overview" e "languages" de games.csv:<br>
dgames = pd.read_csv('.\\DataCSV\\games.csv', sep=',',on_bad_lines='warn')<br>
dgames
</p>
