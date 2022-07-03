# import libraries
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

# import dataset using pandas
data = pd.read_csv("jewellery.csv")

"""
Data Cleansing
"""

# Remove unnecessary columns
data = data.drop(columns=['Order ID', 'Purchased product ID', 'Quantity', 
                          'Category ID', 'Brand ID', 'User ID', 'Product gender'])
# Cleanse Category column
data['Category alias'] = data['Category alias'].str.replace("jewelry.", "")
# Change data type of date columns
data['Order datetime'] = data['Order datetime'].astype(np.datetime64)
# Create year and month columns
data['Order year'] = data['Order datetime'].dt.year
data['Order month'] = data['Order datetime'].dt.month_name()
# rename columns
data = data.rename(columns={'Category alias': 'Category', 'Price in USD': 'Price', 'main gem': 'Main gem'})

# Create month orders list
# new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Create year list to display unique years in dataset
year_list = list([i for i in data['Order year'].unique()])

"""
Create app
"""
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.config.suppress_callback_exceptions = True

"""
App layout
"""

app.layout = html.Div(children=[html.H1("Jewellery Sales Report",
                                        style={'font-size': 38, 'textAlign': 'center',
                                               'margin-bottom': '1em'}),
                                # Outer division starts
                                html.Div([
                                    # helper text + dropdown division
                                    html.Div([
                                        html.Div(["Select a year: "],
                                                 style={'font-size': 28, 'margin-left': '1em',
                                                        'margin-right': '1em'}),
                                        dcc.Dropdown(id='year-type',
                                                     options=[{'label': i, 'value': i} for i in year_list[1:]],
                                                     value=2019,
                                                     style={'textAlign': 'center',
                                                            'width':'50%'}),
                                        ], style={'display': 'flex'}),
                                    # charts division
                                    html.Div([
                                        html.Div([ ], id='plot1'),
                                        html.Div([ ], id='plot2')
                                        ], style={'display': 'flex'})
                                    # Outer division ends
                                    ])               
                                # layout ends
                                ])
"""
Create callback
"""
@app.callback(
    Output('plot1', 'children'),
    Output('plot2', 'children'),
    Input('year-type', 'value')
    )
# Create function that returns charts
def create_charts(year):
    # create df for pie chart
    df = pd.DataFrame(data[data['Order year'] == year].groupby('Category')['Price'].sum())
    # create df for line chart
    df2 = pd.DataFrame(data[data['Order year'] == year].groupby('Order month')['Price'].sum())
    new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df2 = df2.reindex(new_order, axis = 0)
    # create pie chart
    pie_fig = px.pie(df, names=df.index, values=df['Price'], title='Proportion of Sales by Category')
    # create line chart
    line_fig = px.line(df2, x=df2.index, y=df2['Price'], title='Sales by Month', markers=True)
    
    return[
            dcc.Graph(figure=pie_fig),
            dcc.Graph(figure=line_fig)
        ]

if __name__ == '__main__':
    app.run_server()



