import pandas as pd

imdb_movies = pd.read_csv('./Data/IMDb movies.csv')
imdb_movies.drop(['title','reviews_from_users','reviews_from_critics','writer','production_company','description','usa_gross_income','metascore'],axis=1,inplace=True)
imdb_movies.rename({'worlwide_gross_income':'worldwide_gross_income','avg_vote':'imdb_score'},axis=1,inplace=True)

imdb_movies_cleaned = imdb_movies.loc[imdb_movies['worldwide_gross_income'].notnull()].copy()
imdb_movies_cleaned['year'] = imdb_movies_cleaned['year'].astype(int)

imdb_movies_cleaned_income =  imdb_movies_cleaned.loc[\
                                imdb_movies_cleaned['worldwide_gross_income'].str.startswith('$')].copy()
def remove_dollar_sign(gross_income):
    return gross_income.replace('$','')
imdb_movies_cleaned_income['worldwide_gross_income_numbered'] = imdb_movies_cleaned_income.apply(lambda \
                                                    row: remove_dollar_sign(row['worldwide_gross_income']),axis=1)
imdb_movies_cleaned_income['worldwide_gross_income_numbered'] = imdb_movies_cleaned_income[\
                                                              'worldwide_gross_income_numbered'].astype(float)
imdb_movies_cleaned_income.drop(['worldwide_gross_income'],axis=1,inplace=True)
imdb_movies_cleaned_income.rename({'worldwide_gross_income_numbered':'worldwide_gross_income'},axis=1,inplace=True)
imdb_movies_cleaned_income['worldwide_gross_income'] = imdb_movies_cleaned_income['worldwide_gross_income']/1000000

imdb_movies_cleaned_income['director'] = imdb_movies_cleaned_income['director'].fillna('No Director')
imdb_movies_cleaned_income['actors'] = imdb_movies_cleaned_income['actors'].fillna('No Actor')

def convert_col_list(col):
  split_col = col.split(',')
  remove_spaces_col_list = [x.strip() for x in split_col]
  return remove_spaces_col_list

imdb_movies_cleaned_income['director_list'] = imdb_movies_cleaned_income.apply(lambda row:convert_col_list(row['director']),axis=1)
imdb_movies_cleaned_income_explode_director = imdb_movies_cleaned_income.explode('director_list')

movies_director = imdb_movies_cleaned_income_explode_director.groupby('director_list')['imdb_title_id'].agg('count').rename('no_of_movies').reset_index()
movies_director.sort_values(by='no_of_movies',ascending=False,inplace=True)

directors = list(movies_director[:10]['director_list'])+ ['All Top 10 Directors']
