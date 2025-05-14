'''
import pandas as pd

games = pd.read_csv('DataCSV/games.csv', sep=',')
dg_filter = games[["app_id","name","release_date","is_free","type"]]

dspy = pd.read_csv('DataCSV/steamspy_insights.csv', sep=',')
ds_filter = dspy[["app_id","developer","publisher","languages","genres"]]

reviews = pd.read_csv('DataCSV/review.csv', sep=',')
dr_filter = reviews[["app_id","review_score","review_score_description","positive","negative","total","metacritic_score","recommendations"]]

npromotional = pd.read_csv('DataCSV/promotional.csv', sep=',')
categories = pd.read_csv('DataCSV/categories.csv', sep=',')
tags = pd.read_csv('DataCSV/tags.csv', sep=',')
dt_filter = games[["app_id","tag"]]


df = pd.merge(dg_filter, ds_filter, on='app_id', how='inner')
df = pd.merge(df, dr_filter, on='app_id', how='inner')
df = pd.merge(df, npromotional, on='app_id', how='inner')
df = pd.merge(df, categories, on='app_id', how='inner')
df = pd.merge(df, tags, on='app_id', how='inner')

# Salvar o DataFrame em um novo arquivo CSV
df.to_csv('games_merged.csv', index=False, encoding='utf-8')
print("Arquivo CSV 'games_merged.csv' criado com sucesso!")
'''

'''
import pandas as pd

# Função para realizar o inner join, salvar em CSV e contar removidos
def process_and_save(df1, df2, df1_name, df2_name, on='app_id'):
    """
    Realiza um inner join de dois DataFrames na coluna especificada,
    salva o resultado em um novo arquivo CSV e imprime uma mensagem de sucesso.
    Retorna o número de linhas removidas.

    Args:
        df1 (pd.DataFrame): O primeiro DataFrame.
        df2 (pd.DataFrame): O segundo DataFrame.
        df1_name (str): Nome do primeiro DataFrame para nomear o arquivo de saída.
        df2_name (str): Nome do segundo DataFrame para nomear o arquivo de saída.
        on (str, optional): Coluna para realizar o join. Padrão é 'app_id'.

    Returns:
        int: O número de linhas removidas.
    """
    initial_rows_df1 = len(df1)
    initial_rows_df2 = len(df2)
    merged_df = pd.merge(df1, df2, on=on, how='inner')
    final_rows = len(merged_df)
    rows_removed_df1 = initial_rows_df1 - final_rows
    rows_removed_df2 = initial_rows_df2 - final_rows

    output_filename = f'{df1_name}_inner_{df2_name}.csv'
    merged_df.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"Arquivo CSV '{output_filename}' criado com sucesso!")
    print(f"Removidas {rows_removed_df1} linhas de {df1_name}.")
    print(f"Removidas {rows_removed_df2} linhas de {df2_name}.")
    return rows_removed_df1, rows_removed_df2  # Retorna o número de linhas removidas de ambos os DataFrames


# Carregar os dados dos arquivos CSV
# Usei os nomes dos seus arquivos
categories_df = pd.read_csv('DataCSV/categories.csv', sep=',')
games_limpo_df = pd.read_csv('DataCSV/games_limpo.csv', sep=',')
newpromotional_df = pd.read_csv('DataCSV/newpromotional.csv', sep=',')
review_corrigido_df = pd.read_csv('DataCSV/review_corrigido.csv', sep=',')
steamspy_insights_df = pd.read_csv('DataCSV/steamspy_insights.csv', sep=',')
tags_df = pd.read_csv('DataCSV/tags.csv', sep=',')

# Selecionando colunas
dg_filter = games_limpo_df[["app_id","name","release_date","is_free","type"]]
ds_filter = steamspy_insights_df[["app_id","developer","publisher","languages","genres"]]
dr_filter = review_corrigido_df[["app_id","review_score","review_score_description","positive","negative","total","metacritic_score","recommendations"]]


# Processar e salvar os DataFrames individualmente e combinados.
# Combinar 'games' com todos os outros e salvar os resultados.
total_removidos_games = 0
total_removidos_outros = 0 

removidos_games_steamspy, removidos_steamspy = process_and_save(dg_filter, ds_filter, 'games_limpo', 'steamspy_insights')
total_removidos_games += removidos_games_steamspy
total_removidos_outros += removidos_steamspy

removidos_games_review, removidos_review = process_and_save(dg_filter, dr_filter, 'games_limpo', 'review_corrigido')
total_removidos_games += removidos_games_review
total_removidos_outros += removidos_review

removidos_games_promo, removidos_promo = process_and_save(dg_filter, newpromotional_df, 'games_limpo', 'newpromotional')
total_removidos_games += removidos_games_promo
total_removidos_outros += removidos_promo

removidos_games_categ, removidos_categ = process_and_save(dg_filter, categories_df, 'games_limpo', 'categories')
total_removidos_games += removidos_games_categ
total_removidos_outros += removidos_categ

removidos_games_tags, removidos_tags = process_and_save(dg_filter, tags_df, 'games_limpo', 'tags')
total_removidos_games += removidos_games_tags
total_removidos_outros += removidos_tags
#Combinar 'reviews' com 'promotional' para fins de exemplo
removidos_review_promo, removidos_promo_review = process_and_save(dr_filter, newpromotional_df, 'review_corrigido', 'newpromotional')
total_removidos_outros += removidos_promo_review # Adiciona ao total de outros, já que 'review_corrigido' não está em 'games_limpo'

print(f"Total de linhas removidas de games_limpo: {total_removidos_games}")
print(f"Total de linhas removidas dos outros DataFrames: {total_removidos_outros}")
'''

'''
import pandas as pd

# Função para realizar o inner join, salvar em CSV e contar removidos
def process_and_save(df, df_name, on='app_id'):
    """
    Salva o DataFrame em um novo arquivo CSV e imprime uma mensagem de sucesso.

    Args:
        df (pd.DataFrame): O DataFrame.
        df_name (str): Nome do DataFrame para nomear o arquivo de saída.
        on (str, optional): Coluna para realizar o join. Padrão é 'app_id'.
    """
    output_filename = f'{df_name}.csv'
    df.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"Arquivo CSV '{output_filename}' criado com sucesso!")

# Carregar os dados dos arquivos CSV
# Use os nomes dos seus arquivos
categories_df = pd.read_csv('DataCSV/categories.csv', sep=',')
games_limpo_df = pd.read_csv('DataCSV/games_limpo.csv', sep=',')
newpromotional_df = pd.read_csv('DataCSV/newpromotional.csv', sep=',')
review_corrigido_df = pd.read_csv('DataCSV/review_corrigido.csv', sep=',')
steamspy_insights_df = pd.read_csv('DataCSV/steamspy_insights.csv', sep=',')
tags_df = pd.read_csv('DataCSV/tags.csv', sep=',')

# Selecionando colunas
dg_filter = games_limpo_df[["app_id", "name", "release_date", "is_free", "type"]]
ds_filter = steamspy_insights_df[["app_id", "developer", "publisher", "languages", "genres"]]
dr_filter = review_corrigido_df[["app_id", "review_score", "review_score_description", "positive", "negative", "total", "metacritic_score", "recommendations"]]

# Realizar merges encadeados
df_merged = pd.merge(dg_filter, ds_filter, on='app_id', how='inner')
df_merged = pd.merge(df_merged, dr_filter, on='app_id', how='inner')
df_merged = pd.merge(df_merged, newpromotional_df, on='app_id', how='inner')
df_merged = pd.merge(df_merged, categories_df, on='app_id', how='inner')
df_merged = pd.merge(df_merged, tags_df, on='app_id', how='inner')

# Salvar o resultado final
process_and_save(df_merged, 'games_merged_final')

# Separar o DataFrame mergeado em DataFrames individuais
games_limpo_merged = df_merged[["app_id", "name", "release_date", "is_free", "type"]].drop_duplicates()
steamspy_insights_merged = df_merged[["app_id", "developer", "publisher", "languages", "genres"]].drop_duplicates()
review_corrigido_merged = df_merged[["app_id", "review_score", "review_score_description", "positive", "negative", "total", "metacritic_score", "recommendations"]].drop_duplicates()
newpromotional_merged = df_merged[["app_id"] + [col for col in df_merged.columns if 'promotional' in col]].drop_duplicates()
categories_merged = df_merged[["app_id"] + [col for col in df_merged.columns if 'category' in col]].drop_duplicates()
tags_merged = df_merged[["app_id"] + [col for col in df_merged.columns if 'tag' in col]].drop_duplicates()


# Salvar os DataFrames separados
process_and_save(games_limpo_merged, 'games_limpo_merged')
process_and_save(steamspy_insights_merged, 'steamspy_insights_merged')
process_and_save(review_corrigido_merged, 'review_corrigido_merged')
process_and_save(newpromotional_merged, 'newpromotional_merged')
process_and_save(categories_merged, 'categories_merged')
process_and_save(tags_merged, 'tags_merged')
'''

'''
import pandas as pd

# Carrega o arquivo CSV que contém todos os dados
games_merged_final_df = pd.read_csv('DataCSV/games_merged_final.csv', sep=',')

# Carrega o arquivo CSV promocional, que contém apenas a coluna 'app_id'
promotional_df = pd.read_csv('DataCSV/promotional.csv', sep=',')  # Certifique-se de que o caminho está correto

# Garante que temos apenas um 'header_image' e 'background_image' por 'app_id'
promotional_data_from_merged = games_merged_final_df[['app_id', 'header_image', 'background_image']].drop_duplicates()

# Realiza o merge para adicionar as colunas ao DataFrame promocional.
promotional_df_updated = pd.merge(promotional_df, promotional_data_from_merged, on='app_id', how='left')

# Salva o DataFrame atualizado em um novo arquivo CSV
promotional_df_updated.to_csv('promotional_atualizado.csv', index=False, encoding='utf-8')
print("Arquivo CSV 'promotional_atualizado.csv' criado com sucesso!")
'''