import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# Read the data
Base_Dados = pd.read_csv('data/Dados_Diários.csv')
Base_Valor = pd.read_csv('data/Dados_Mes_Valor.csv')
Base_Valor.columns = ['Mes', 'Quantidade']

# Create the Dash app
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.DARKLY,
                                      'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css',
                                      'https://fonts.googleapis.com/css2?family=Joan&family=Roboto:ital,wght@0,100;1,300&family=Source+Sans+Pro:ital,wght@0,400;1,300&display=swap'],
                title='Evento Dashboard')

# Define the layout of the app
app.layout = html.Div(children=[
    html.Div(className='banner',
             style={'height': 'fit-content',
                    'background-color': '#1e2130',
                    'display': 'flex',
                    'flex-direction': 'row',
                    'align-items': 'center',
                    'justify-content': 'space-between',
                    'border-bottom': '1px solid #4b5460',
                    'padding': '1rem 5rem',
                    'width': '100%'},
             children=[
                 html.Div(className='banner-title',
                          children=[
                              html.H5('Dashboard',
                                      style={'font-family': 'open sans semi bold, sans-serif',
                                             'font-weight': '500'}),
                              html.H6('Análise de multas PRF 2022'),
                          ]),
                 html.Div(className='banner-logo',
                          children=[
                              html.Img(src=app.get_asset_url('logo.webp'), height='30px', alt='Logo')
                          ])
             ]),
    html.Div(className='app-content',
             style={'padding': '1rem 5rem',
                    'width': '100%'},
             children=[
                 html.Div(className='content',
                          style={'display': 'grid',
                                 'grid-template-columns': '20% 80%',
                                 'height': '500px'},
                          children=[
                              html.Div(className='left-div',
                                       style={'display': 'flex',
                                              'flex-direction': 'column',
                                              'justify-content': 'space-evenly',
                                              'align-items': 'center',
                                              'margin': '0',
                                              'padding': '0',
                                              'width': '100%',
                                              'margin-bottom': '3rem',
                                              'background-color': '#161a28',
                                              'border': '#1e2130 solid 0.2rem'},
                                       children=[
                                           html.Div(className='top',
                                                    children=[
                                                        html.H5('Total multas',
                                                                style={'line-height': '1.6',
                                                                       'box-sizing': 'border-box',
                                                                       'margin': '1rem',
                                                                       'font-weight': '500',
                                                                       'align-self': 'flex-start'})
                                                    ]),
                                           html.Div(className='inner-div',
                                                    children=[
                                                        html.H5('Total valores',
                                                                style={'line-height': '1.6',
                                                                       'box-sizing': 'border-box',
                                                                       'margin': '1rem',
                                                                       'font-weight': '500',
                                                                       'align-self': 'flex-start'})
                                                    ])
                                       ]),
                              html.Div(className='right-div',
                                       style={'display': 'flex',
                                              'flex-direction': 'column',
                                              'justify-content': 'space-evenly',
                                              'align-items': 'center',
                                              'margin': '0',
                                              'padding': '0',
                                              'width': '100%',
                                              'margin-bottom': '3rem',
                                              'background-color': '#161a28',
                                              'border': '#1e2130 solid 0.2rem'},
                                       children=[
                                           html.Div(className='inner-div',
                                                    style={'margin': '0',
                                                           'padding': '0',
                                                           'width': '100%',
                                                           'height': '350px',
                                                           'border-bottom': '#1e2130 solid 0.2rem'},
                                                    children=[
                                                        dcc.Graph(id='grafico1',
                                                                  figure=go.Figure(data=[
                                                                      go.Scatter(y=Base_Dados.Quantidade,
                                                                                 x=Base_Dados.Data,
                                                                                 mode='lines',
                                                                                 name='Gráfico 1',
                                                                                 line=dict(color='yellow', width=3)
                                                                                 )],
                                                                                 layout=go.Layout(title='Multas diárias',
                                                                                                  template='plotly_dark',
                                                                                                  plot_bgcolor='#161a28',
                                                                                                  paper_bgcolor='#161a28',
                                                                                                  font={'color': 'white'},
                                                                                                  xaxis={'showgrid': False},
                                                                                                  yaxis={'showgrid': False},
                                                                                                  height=350,
                                                                                                  width=1050,
                                                                                                  xaxis_title='Período',
                                                                                                  yaxis_title='Quantidade'
                                                                                                  )
                                                                                 )
                                                                  )
                                                    ]),
                                           html.Div(className='inner-div',
                                                    style={'margin': '0',
                                                           'padding': '0',
                                                           'width': '100%',
                                                           'height': '350px',
                                                           'border-top': '#1e2130 solid 0.2rem'},
                                                    children=[
                                                        dcc.Graph(id='grafico2',
                                                                  figure=go.Figure(data=[
                                                                      go.Bar(y=Base_Valor['Quantidade'],
                                                                             x=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                                                                             marker=dict(color='#3a8c5d'),
                                                                             textposition='outside'
                                                                             )],
                                                                                 layout=go.Layout(title='Valores mensais aplicados',
                                                                                                  template='plotly_dark',
                                                                                                  plot_bgcolor='#161a28',
                                                                                                  paper_bgcolor='#161a28',
                                                                                                  font={'color': 'white'},
                                                                                                  xaxis={'showgrid': False},
                                                                                                  yaxis={'showgrid': False},
                                                                                                  height=300,
                                                                                                  width=1050,
                                                                                                  xaxis_title='Período',
                                                                                                  yaxis_title='Valor em R$'
                                                                                                  )
                                                                                 )
                                                                  )
                                                    ])
                                       ])
                          ])
             ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
