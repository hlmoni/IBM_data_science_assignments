# IMPORTANT NOTE:
# execute the following commands in terminal before running the application:
    # python3.11 -m pip install pandas dash
    # wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
    # wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"

# run the application: 
    # python3.11 spacex_dash_app.py

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id = 'site-dropdown',
                                    options = [
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                        ],
                                    value = 'ALL',
                                    placeholder = "Select a Launch Site",
                                    searchable = True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                # TASK 3: Add a slider to select payload range
                                html.P("Payload Range (kg):"),
                                dcc.RangeSlider(id='payload-slider', 
                                    min=0, max=10000, step=1000, 
                                    marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000', 10000: '10000'}, 
                                    value=[2000, 5000]
                                    ),
    
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
#    success_all_sites = (spacex_df['class'] == 1)
    if entered_site == 'ALL': 
        fig = px.pie(spacex_df, 
            values = 'class', 
            names = 'Launch Site',
#            names = 'class',
            title = 'Successful Launches on All Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, 
        names='class', 
        labels={"0": "failed", "1": "success"},
        title=f'Successful Launches on Site {entered_site}')  
    return fig        
        # return the outcomes piechart for a selected site
        # if entered_site == 'CCAFS LC-40':
            # df_site1 = (spacex_df['Launch site'] == 'CCAFS LC-40')
            # df_site1_success_rate = spacex_df.groupby('class').value_counts()
            # fig = px.pie(df_site1_success_rate,
                # values = 'class',
                # names = 'class',
                # title = 'Success Rate on Site CCAFS LC-40'
                # )
            # return fig
        # if entered_site == 'CCAFS SLC-40':
            # df_site2 = (spacex_df['Launch site'] == 'CCAFS SLC-40')
            # df_site2_success_rate = spacex_df.groupby('class').value_counts()
            # fig = px.pie(df_site2_success_rate,
                # values = 'class',
                # names = 'class',
                # title = 'Success Rate on Site CCAFS SLC-40'
                # )
            # return fig
        # if entered_site == 'KSC LC-39A':
            # df_site3 = (spacex_df['Launch site'] == 'KSC LC-39A')
            # df_site3_success_rate = spacex_df.groupby('class').value_counts()
            # fig = px.pie(df_site3_success_rate,
                # values = 'class',
                # names = 'class',
                # title = 'Success Rate on Site KSC LC-39A'
                # )
            # return fig
        # if entered_site == 'VAFB SLC-4E':
            # df_site4 = (spacex_df['Launch site'] == 'VAFB SLC-4E')
            # df_site4_success_rate = spacex_df.groupby('class').value_counts()
            # fig = px.pie(df_site4_success_rate,
                # values = 'class',
                # names = 'class',
                # title = 'Success Rate on Site VAFB SLC-4E'
                # )
            # return fig
        # else:
            # return None

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_payload_scatter_chart(entered_site, payload_range):
#    success_all_sites = (spacex_df['class'] == 1)
    low, high = payload_range
    
    if entered_site == 'ALL':  
        df_mask = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
        fig = px.scatter(df_mask, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation of Payload and Successful Missions for All Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        df_mask = filtered_df[(filtered_df['Payload Mass (kg)'] >= low) & (filtered_df['Payload Mass (kg)'] <= high)]
        fig = px.scatter(df_mask, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f'Correlation of Payload and Successful Missions on Site {entered_site}')
    return fig        

# Run the app
if __name__ == '__main__':
    app.run_server()
