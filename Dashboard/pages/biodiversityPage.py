# =============================================================================
# Import relevant modules and objects from scripts
# =============================================================================
import dash
import plotly.graph_objs as go
from dash import Input, Output, html, dcc

from data_loading import regional_rli_data, regional_lpi_data

from emission_modelling import predict_rli, predict_lpi
# =============================================================================
# This script is a page in the dashboard. Each page will contain all content
# from the script, plus all content from the app.py script.
# =============================================================================
dash.register_page(__name__, path= "/biodiversity")

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
                                "Biodiversity: how is the Netherlands doing?",
                                ),
                            dcc.Markdown('''
                                This page contains two line graphs. The left graph shows the Red List Index, an measure of endangered species within a country. 
                                Data for the Red List Index ranges from 1994 to 2021. Data from 2022 onwards is based on model predictions. It always shows the 
                                trendline for the Netherlands, and defaults to add a trendline of the average of Western Europe. The drop-down menu can be used
                                to visualise trendlines of other European countries as comparison. The right graph shows the Living Planet Index, a measure of 
                                biological diversity compared to a baseline measurement, 1990 in this case. Data for the Living Planet Index ranges from 1990 
                                to 2019 for the Netherlands and from 1990 to 2016 for Europe and central Asia. Data from 2020 (for the Netherlands) and 2017 
                                (for Europe and central Asia) onwards is based on model predictions. 
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

# Defines the div that calls the line graph function
def compareGraph(graphID, dropdownID, title= "Graph Title"):
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
                        options= list(regional_rli_data),
                        value= "Western Europe",
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

# Defines that input and output for the interactive drop-down menu
@dash.callback(
    Output("biodiv-graph-left", 'figure'),
    Input("region-left", "value"))
# Defines the function that draws the RLI line graph and is called within the compareGraph div
def update_figure(selected_country):

    fig= go.Figure()    

    data_NL= predict_rli(regional_rli_data, "Netherlands")["predicted_results"] 
    
    
    fig.add_traces([go.Scatter(name= "Netherlands",
                               x= data_NL.year,
                               y= data_NL.RLI,
                               mode= "lines",
                               line= dict(color= "#FFA500")),
                    go.Scatter(name= "Upper Bound",
                               x= data_NL.year,
                               y= data_NL.Upper,
                               mode= "lines",
                               marker= dict(color= "#444"),
                               line= dict(width= 0),
                               showlegend= False,
                               hoverinfo= "skip"),
                    go.Scatter(name= "Lower Bound",
                               x= data_NL.year,
                               y= data_NL.Lower,
                               mode= "lines",
                               marker= dict(color= "#444"),
                               line= dict(width= 0),
                               fillcolor= "rgba(68, 68, 68, 0.3)",
                               fill= "tonexty",
                               showlegend= False,
                               hoverinfo= "skip")
                    ])

    if selected_country is not None and selected_country!= "Netherlands":
        
        data_comp= predict_rli(regional_rli_data, selected_country)["predicted_results"]
        
        fig.add_traces([go.Scatter(name= f"{selected_country}",
                                   x= data_comp.year,
                                   y= data_comp.RLI,
                                   mode= "lines"),
                        go.Scatter(name= "Upper Bound",
                                   x= data_comp.year,
                                   y= data_comp.Upper,
                                   mode= "lines",
                                   marker= dict(color= "#444"),
                                   line= dict(width= 0),
                                   showlegend= False,
                                   hoverinfo= "skip"),
                        go.Scatter(name= "Lower Bound",
                                   x= data_comp.year,
                                   y= data_comp.Lower,
                                   mode= "lines",
                                   marker= dict(color= "#444"),
                                   line= dict(width= 0),
                                   fillcolor= "rgba(68, 68, 68, 0.3)",
                                   fill= "tonexty",
                                   showlegend= False,
                                   hoverinfo= "skip")
                        ])

    fig.update_yaxes(title_text='Red List Index',
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


# Defines the div that calls the line graph function
def lpiGraph(title= "Graph Title"):
    return html.Div(
        children= [
            html.H4(
                style= {
                    "text-align": "left",
                    "font-weight": "bold"
                    },
                children= title
                ),
            dcc.Graph(
                figure= lpi_figure()
                )
            ]
        )

# Defines the function that draws the LPI line graph and is called within the compareGraph div
def lpi_figure():

    fig= go.Figure()    
    
    for region in regional_lpi_data:
        data= predict_lpi(regional_lpi_data, region)["predicted_results"] 

        fig.add_traces([go.Scatter(name= region,
                                   x= data.Year,
                                   y= data.LPI_final,
                                   mode= "lines",
                                   line= {'color': '#FFA500' if region== "Netherlands" else '#DC24EE'}),
                        go.Scatter(name= "Upper Bound",
                                   x= data.Year,
                                   y= data.CI_high,
                                   mode= "lines",
                                   marker= dict(color= "#444"),
                                   line= dict(width= 0),
                                   showlegend= False,
                                   hoverinfo= "skip"),
                        go.Scatter(name= "Lower Bound",
                                   x= data.Year,
                                   y= data.CI_low,
                                   mode= "lines",
                                   marker= dict(color= "#444"),
                                   line= dict(width= 0),
                                   fillcolor= "rgba(68, 68, 68, 0.3)",
                                   fill= "tonexty",
                                   showlegend= False,
                                   hoverinfo= "skip")
                        ])
        
    fig.update_yaxes(title_text='Living Planet Index',
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

# Defines the div that serves as the main body of this page. Includes RLI line
# graph on the left of the dashboard, and LPI line graph on the right of the dashboard
def graphSectionBio1(): 
    return html.Div(
    id= "float-parent-element",
    children= [
        html.Div(
            className= "float-child-element",
            children= [
                html.Div(
                    className= "left-Bio",
                    children= [
                        compareGraph(
                            title= "Red List Index from 1994 to 2031",
                            graphID= "biodiv-graph-left",
                            dropdownID= "region-left"
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
                    className= "right-Bio",
                    children= [
                        lpiGraph(title= "Living planet index from 1990 to 2026")                       
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
            graphSectionBio1()
            ]
        )
