# NB: to run this app, the following commands need to be run first
#   pip3 install pandas dash wget

# Import required libraries
import pandas as pd
import dash
import wget
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')
spacex_df = pd.read_csv(csv_file)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print(max_payload, ' ', min_payload)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label':'All Sites', 'value':'all'},
                                        {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                        {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                        {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                        {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}
                                    ],
                                    value='all',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={
                                        0: '0 kg',
                                        1000: '1000 kg',
                                        2000: '2000 kg',
                                        3000: '3000 kg',
                                        4000: '4000 kg',
                                        5000: '5000 kg',
                                        6000: '6000 kg',
                                        7000: '7000 kg',
                                        8000: '8000 kg',
                                        9000: '9000 kg',
                                        10000: '10000 kg',
                                    },
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_launch_data(launch_site):
    if launch_site == 'all':
        fig = px.pie(spacex_df, values='class', names='Launch Site')
        fig.update_traces(textinfo='value')
        fig.update_layout(title='Successful Launches')
    else:
        fig = px.pie(spacex_df[spacex_df['Launch Site']==str(launch_site)].groupby('class').count().reset_index(), values='Launch Site', names='class')
        fig.update_traces(marker_colors=['#ef553b','#00cc96'])
        fig.update_layout(title='Successful Launches for %s' % launch_site)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
)
def build_scatter_plot(launch_site, payload_range):
    payload_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0], payload_range[1])]
    if launch_site == 'all':
        fig = px.scatter(payload_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    else:
        fig = px.scatter(payload_df[payload_df['Launch Site']==str(launch_site)], x='Payload Mass (kg)', y='class', color='Booster Version Category')
    fig.update_layout(title='Correlation between Payload Mass and Success')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
