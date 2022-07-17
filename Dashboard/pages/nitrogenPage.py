# =============================================================================
# Import relevant modules and objects from scripts
# =============================================================================
import dash
import plotly.express as px
import plotly.graph_objs as go
from dash import Input, Output, html, dcc

from data_loading import *

from emission_modelling import predict_emission
# =============================================================================
# This script is a page in the dashboard. Each page will contain all content
# from the script, plus all content from the app.py script.
# =============================================================================
dash.register_page(__name__, path= "/nitrogen")

# The pageheader is div that includes the main topic of the page
def pageheader():
    return html.Div(
        id= "pageheader",
        children= [
            html.Div(
                className= "col",
                children= [
                    html.Div(
                        children= [
                            html.H2(
                                "Nitrogen emissions: past, present and future",
                                ),
                            dcc.Markdown('''
                                This page contains two maps and two line graphs showing the past, present and predicted future nitrogen emissions and losses 
                                throughout the Netherlands. It contains data from 1990 and then from 1994 to 2021. Data in the line graphs from 2022 onwards 
                                is based on model predictions. The first two figures show the total annual nitrogen emissions in kilograms. The second row of 
                                figures show the annual percentage of nitrogen that is lost to the environment. The maps show data for each province individually. 
                                They default to total emission values of all business types together, but the drop-down menu can be used to visualise other 
                                business types. The slider below the maps can be used to visualise the situation in past years. The line graphs show trendlines for 
                                all different business types. They default to information on the Netherlands, but the drop-down menu can be used to visualise regional trends.
                                Different business types can be shown or hidden by clicking on the name in the legend.
                            ''',
                            style= {
                                "margin-bottom": "5%",
                                "text-align": "justify"
                                })                        
                            ]
                        )
                    ]
                )
            ]
        )
                                       
# Defines the div that calls the choropleth map function
def choroplethMap(graphID, sliderID, dropdownID, title= "Graph Title"):
    return html.Div(
        children= [
            html.H4(
                style= {
                    "text-align": "left",
                    "font-weight": "bold"
                    },
                children= title
                ),
            html.Div(
                children= [
                    dcc.Dropdown(
                        options= code2business_ENG,
                        value= "T001061",
                        id= dropdownID
                        )                    
                    ],
                style= {
                    "width":"40%",
                    "text-align": "left"
                    }
                ),
            dcc.Graph(id= graphID),
            html.Div(
                dcc.Slider(
                    emission_data['Jaar'].min(),
                    emission_data['Jaar'].max(),
                    step=None,
                    value=emission_data['Jaar'].max(),
                    marks={str(year): str(year) for year in emission_data['Jaar'].unique()},
                    id= sliderID,
                    )           
                )
            ]
        )

# Defines the div that calls the line graph function
def lineGraph(graphID, dropdownID, title= "Graph Title"):
    return html.Div(
        children= [
            html.H4(
                style= {
                    "text-align": "left",
                    "font-weight": "bold"
                    },
                children= title
                ),
            html.Div(
                children= [
                    dcc.Dropdown(
                        options= list(regional_emission_data),
                        value= "Nederland",
                        id= dropdownID
                        )                    
                    ],
                style= {
                    "width":"40%",
                    "text-align": "left"
                    }
                ),
            dcc.Graph(id= graphID)
            ]
        )

# Defines that input and output for the interactive drop-down menu and slider
@dash.callback(
    Output('choropleth-map-1', 'figure'),
    Input("year-slider-1", 'value'),
    Input("data-type-1", "value"))
# Defines the function that draws the choropleth map for N emission
# and is called within the choroplethMap div
def update_figure(selected_year, selected_business_type):
    filtered_data_type= emission_data.query(f'Bedrijfstype== "{selected_business_type}" and RegioS in {province_list}')
    filtered_data= filtered_data_type.query(f'Jaar== {selected_year}')
    
    fig= px.choropleth(
        filtered_data,
        geojson= netherlands_geojson,
        locations= "RegioS",
        featureidkey= "properties.name",
        color= "TotaalStikstofuitscheiding_5",
        color_continuous_scale="Inferno_r",
        range_color= (0, filtered_data_type["TotaalStikstofuitscheiding_5"].max()*1.1),
        labels= {"TotaalStikstofuitscheiding_5": colname2ENG["TotaalStikstofuitscheiding_5"],
                 "RegioS": colname2ENG["RegioS"]})
    
    fig.update_geos(fitbounds="locations", visible=False)
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    return fig

# Defines that input and output for the interactive drop-down menu
@dash.callback(
    Output("line-graph-1", 'figure'),
    Input("region-1", "value"))
# Defines the function that draws the line graph for N emission
# and is called within the lineGraph div
def update_figure(selected_region):
    
    fig= go.Figure()    

    for business_type in code2business_ENG:
        
        model_results= predict_emission(regional_emission_data, 
                                        selected_region, 
                                        business_type, 
                                        "TotaalStikstofuitscheiding_5")
        predicted_results= model_results["predicted_results"]
        
        
        fig.add_traces([go.Scatter(name= f'{code2business_ENG[business_type]}',
                                   x= predicted_results.Jaar,
                                   y= predicted_results.emission_values,
                                   mode= "lines"),
                        go.Scatter(name= "Upper Bound",
                                   x= predicted_results.Jaar,
                                   y= predicted_results.Upper,
                                   mode= "lines",
                                   marker= dict(color= "#444"),
                                   line= dict(width= 0),
                                   showlegend= False,
                                   hoverinfo= "skip"),
                        go.Scatter(name= "Lower Bound",
                                   x= predicted_results.Jaar,
                                   y= predicted_results.Lower,
                                   mode= "lines",
                                   marker= dict(color= "#444"),
                                   line= dict(width= 0),
                                   fillcolor= "rgba(68, 68, 68, 0.3)",
                                   showlegend= False,
                                   hoverinfo= "skip")
                        ])
        
    fig.update_yaxes(title_text='Living planet Index',
                     showline=True, linewidth=2, 
                     linecolor='rgba(68, 68, 68, 0.3)', 
                     gridcolor= 'rgba(68, 68, 68, 0.1)')
    fig.update_xaxes(title_text='Year',
                     showline=True, linewidth=2, 
                     linecolor='rgba(68, 68, 68, 0.3)', 
                     gridcolor= 'rgba(68, 68, 68, 0.1)')
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

        
    return fig

# Defines that input and output for the interactive drop-down menu and slider
@dash.callback(
    Output('choropleth-map-2', 'figure'),
    Input('year-slider-2', 'value'),
    Input("data-type-2", "value"))
# Defines the function that draws the choropleth map for N losses
# and is called within the choroplethMap div
def update_figure(selected_year, selected_business_type):
    
    filtered_data_type= emission_data.query(f'Bedrijfstype== "{selected_business_type}" and RegioS in {province_list}')
    filtered_data= filtered_data_type.query(f'Jaar== {selected_year}')

    fig= px.choropleth(
        filtered_data,
        geojson= netherlands_geojson,
        locations=  "RegioS",
        featureidkey="properties.name",
        color= "PercentageStikstofverliezen",
        color_continuous_scale="Inferno_r",
        range_color= (0, 100),
        labels= {"PercentageStikstofverliezen": colname2ENG["PercentageStikstofverliezen"],
                 "RegioS": colname2ENG["RegioS"]})

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                                  plot_bgcolor='rgba(0,0,0,0)',
                                  geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    return fig

# Defines that input and output for the interactive drop-down menu
@dash.callback(
    Output("line-graph-2", 'figure'),
    Input("region-2", "value"))
# Defines the function that draws the line graph for N losses
# and is called within the lineGraph div
def update_figure(selected_region):
    
    fig= go.Figure()    

    for business_type in code2business_ENG:
        
        model_results= predict_emission(regional_emission_data, 
                                        selected_region, 
                                        business_type, 
                                        "PercentageStikstofverliezen")
        predicted_results= model_results["predicted_results"]
        
        
        fig.add_traces([go.Scatter(name= f'{code2business_ENG[business_type]}',
                                   x= predicted_results.Jaar,
                                   y= predicted_results.emission_values,
                                   mode= "lines"),
                        go.Scatter(name= "Upper Bound",
                                   x= predicted_results.Jaar,
                                   y= predicted_results.Upper,
                                   mode= "lines",
                                   marker= dict(color= "#444"),
                                   line= dict(width= 0),
                                   showlegend= False,
                                   hoverinfo= "skip"),
                        go.Scatter(name= "Lower Bound",
                                   x= predicted_results.Jaar,
                                   y= predicted_results.Lower,
                                   mode= "lines",
                                   marker= dict(color= "#444"),
                                   line= dict(width= 0),
                                   fillcolor= "rgba(68, 68, 68, 0.3)",
                                   showlegend= False,
                                   hoverinfo= "skip")
                        ])
        
    fig.update_yaxes(title_text='Living planet Index',
                     showline=True, linewidth=2, 
                     linecolor='rgba(68, 68, 68, 0.3)', 
                     gridcolor= 'rgba(68, 68, 68, 0.1)')
    fig.update_xaxes(title_text='Year',
                     showline=True, linewidth=2, 
                     linecolor='rgba(68, 68, 68, 0.3)', 
                     gridcolor= 'rgba(68, 68, 68, 0.1)')
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

        
    return fig

# Defines the div that includes the N emission choropleth map on the left of the
# dashboard, and the N emission line graph on the right of the dashboard
def graphSection1(): 
    return html.Div(
     id= "float-parent-element",
     children= [
         html.Div(
             className= "float-child-element",
             children= [
                 html.Div(
                     className= "left-N",
                     children= [
                         choroplethMap(
                             title= "Total nitrogen emissions per province",
                             graphID= "choropleth-map-1",
                             sliderID= "year-slider-1",
                             dropdownID= "data-type-1"
                             )
                         ],
                     style= {
                         "margin-left": "5%"
                         }
                     )
                 ]
             ),
         html.Div(
             className= "float-child-element",
             children= [
                 html.Div(
                     className= "right-N",
                     children= [
                         lineGraph(
                             title= "Total nitrogen emissions per business type",
                             graphID= "line-graph-1",
                             dropdownID= "region-1"                                  
                             )                       
                         ],
                     style= {
                         "margin-right": "5%"
                         }
                     )
                 ]
             )
         ]
     )

# Defines the div that includes the N losses choropleth map on the left of the
# dashboard, and the N losses line graph on the right of the dashboard
def graphSection2(): 
    return html.Div(
     id= "float-parent-element-2",
     children= [
         html.Div(
             className= "float-child-element",
             children= [
                 html.Div(
                     className= "left-N",
                     children= [
                         choroplethMap(
                             title= "Percentage nitrogen losses per province",
                             graphID= "choropleth-map-2",
                             sliderID= "year-slider-2",
                             dropdownID= "data-type-2"
                             )                        
                         ],
                     style= {
                         "margin-left": "5%"
                         }
                     )
                 ]
             ),
         html.Div(
             className= "float-child-element",
             children= [
                 html.Div(
                     className= "right-N",
                     children= [
                         lineGraph(
                             title= "Percentage nitrogen losses per business type",
                             graphID= "line-graph-2",
                             dropdownID= "region-2"                                  
                             )                       
                         ],
                     style= {
                         "margin-right": "5%"
                         }
                     )
                 ]
             )
         ]
     )


# Defines the layout function that is called from the main app.py script when 
# navigating to this page

def layout():
    return html.Div(
        children= [
            pageheader(),
            graphSection1(),
            graphSection2()
            ]
        )
