import dash
import plotly.express as px
import plotly.graph_objs as go
from dash import Input, Output, html, dcc

dash.register_page(__name__, path= "/nitrogen")
from data_loading import *

from emission_modelling import predict_emission



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

@dash.callback(
    Output('choropleth-map-1', 'figure'),
    Input("year-slider-1", 'value'),
    Input("data-type-1", "value"))
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


@dash.callback(
    Output("line-graph-1", 'figure'),
    Input("region-1", "value"))
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


@dash.callback(
    Output('choropleth-map-2', 'figure'),
    Input('year-slider-2', 'value'),
    Input("data-type-2", "value"))
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

@dash.callback(
    Output("line-graph-2", 'figure'),
    Input("region-2", "value"))
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
                         ]
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
                         ]
                     )
                 ]
             )
         ]
     )

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
                         ]
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
                         ]
                     )
                 ]
             )
         ]
     )




def layout():
    return html.Div(
        children= [
            pageheader(),
            graphSection1(),
            graphSection2()
            ]
        )
