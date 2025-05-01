# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36', 'font-size': '40px'}),
    html.Br(),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    #dcc.Dropdown(id='site-dropdown',...)

    dcc.Dropdown(
    id='site-dropdown',
    options=[
        {'label': 'All Sites', 'value': 'ALL'},
        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
    value='ALL',
    placeholder="Select a Launch Site",
    searchable=True),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site

    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3: Add a slider to select payload range
    #dcc.RangeSlider(id='payload-slider',...)

    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
      id='payload-slider',
      min=min_payload,
      max=max_payload,
      step=1000,
      marks={i: str(i) for i in range(int(min_payload), int(max_payload)+1, 1000)},
      value=[min_payload, max_payload]),
                                
    #TASK 4: Add a scatter chart to show the correlation between payload and launch success    
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))

])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
  #filtered_df = spacex_df
  if entered_site == 'ALL':
      fig = px.pie(spacex_df, values='class', names='Launch Site',
                   title='Total Successful Launches by Site')
  else:
    #filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    fig = px.pie(spacex_df[spacex_df['Launch Site'] == entered_site], 
                     names='class', title=f'Total Success launches at {entered_site}')

  fig.update_layout(margin=dict(t=50, b=10, l=10, r=10), showlegend=True)
  fig.update_traces(textinfo="percent+label") 
  
  return fig


# TASK 3:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id='payload-slider', component_property='value')]
)

def get_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(filtered_df, 
                     x='Payload Mass (kg)', 
                     y='class', 
                     color='Booster Version Category' if 'Booster Version Category' in filtered_df.columns else 'Launch Site',
                     title=f'Payload vs. Success Rate at {selected_site}' if selected_site != 'ALL' else 'Payload vs. Success Rate for All Sites')

    
    return fig


# Run the app without debug mode
#if __name__ == '__main__':
    #app.run()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
