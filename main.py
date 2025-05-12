import pandas as pd

games = pd.read_csv('DataCSV/games_limpo.csv', sep=',')
dg_filter = games[["app_id","name","release_date","is_free","type"]]

dspy = pd.read_csv('.\\DataCSV\\steamspy_insights.csv', sep=',')
ds_filter = dspy[["app_id","developer","publisher","languages","genres"]]

reviews = pd.read_csv('DataCSV/review_corrigido.csv', sep=',')
dr_filter = reviews[["app_id","review_score","review_score_description","positive","negative","total","metacritic_score","recommendations"]]

npromotional = pd.read_csv('DataCSV/newpromotional.csv', sep=',')
categories = pd.read_csv('DataCSV/categories.csv', sep=',')
tags = pd.read_csv('.\\DataCSV\\tags.csv', sep=',')

df = pd.merge(dg_filter, ds_filter, on='app_id', how='inner')
df = pd.merge(df, dr_filter, on='app_id', how='inner')
df = pd.merge(df, npromotional, on='app_id', how='inner')
df = pd.merge(df, categories, on='app_id', how='inner')
df = pd.merge(df, tags, on='app_id', how='inner')

df