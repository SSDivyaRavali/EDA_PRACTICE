# import the libraries
import pandas as pd
import dash 
import dash_html_components as html
#from dash import html
import dash_core_components as dcc
#from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

from prep_data import imdb_movies_cleaned_income_explode_director,directors

# Create the Dash app
app = dash.Dash(__name__)
server = app.server

# Layout section of dashboard basically how the app would look like
app.layout = html.Div(children=[
    html.H1(children='Imdb score and Gross Income  Dashboard'),
    html.H2(children='Director'),
    dcc.Dropdown(
        id = 'Director-dropdown',
        options=[{'label':i,'value':i} for i in directors],
        value='All Top 10 Directors'
    ),dcc.Graph(id='income-imbdscore-graph')
]
)
# add interactivity to the code - basically create a scatter plot
# we will filter out movies based on their director 
# then for those movies we will make scatter plot of imdb_score and worldwide gross income
# Set up the callback function
@app.callback(
    Output(component_id='income-imbdscore-graph', component_property='figure'),
    [
     Input(component_id='Director-dropdown',component_property='value')
    ]
)
def update_graph(directors):    
    if directors == 'All Top 10 Directors':
      director_select = ''
    else:
      director_select = directors
    
    filtered_final = imdb_movies_cleaned_income_explode_director.loc[imdb_movies_cleaned_income_explode_director['director_list'].str.contains(director_select,na=False)]
    
    
    scatter_fig = px.scatter(filtered_final,
                       x='worldwide_gross_income', y='imdb_score',hover_name='original_title',
                       hover_data=['director_list'],
                       title='Ratings and worldwide_gross_income for movies for director {}'.format(directors))
    return scatter_fig

if __name__ == '__main__':
    app.run_server()