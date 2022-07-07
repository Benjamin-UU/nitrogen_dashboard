# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 14:05:40 2022

@author: BRSch
"""

import dash
from dash import html, dcc

dash.register_page(__name__, path='/about')

def pageheader():
    return html.Div(
        className= "pagetext",
        children= [
            html.Div(
                className= "col",
                children= [
                    html.Div(
                        children= [
                            html.H2(
                                "About the Nitrogen- and Biodiversity Dashboard",
                                ),
                            dcc.Markdown('''
                                This dashboard has been developed as a data science project. It aims to summarise the nitrogen crisis
                                in the Netherlands by explaining the situation and visualising data on emissions and biodiversity. 
                                Data has been retreived from publicly available sources that are as much open access as possible. 
                                Open access data is essential for transparency, as it allows third parties to fact check and make sure
                                everything shown on this dashboard is correct. Sources include the Dutch government, the United Nations,
                                the WWF, and more (for a full list, including where to access the data, see below).
                                ''',
                            style= {
                                "text-align": "justify"
                                })
                            ]  
                        )
                    ]
                )
            ]
        )
                                       
def pagetext():
    return html.Div(
        className= "pagetext",
        children= [
            html.Div(
                className= "col",
                children= [
                    html.Div(
                        children= [
                            html.H3(
                                "About the nitrogen emission data",
                                ),
                            dcc.Markdown('''
                                The nitrogen emission data was sourced from the Dutch Central Bureau for Statistics (CBS). Updates are 
                                published on a yearly basis. Preliminary data is published during the first quarter, and then finalized 
                                data is published later in the year (last update 30-06-2022). First recordings stem from 1990. There was 
                                a three year gap in the data between 1991 and 1993. From 1994 onwards, emissions have been annually 
                                recorded. The last recorded year is 2021.  
                                Nitrogen emission data has been recorded in units of 1000kg. So for example, a value of 5000 on a figure
                                represents 5 000 000kg of nitrogen. Nitrogen losses have been recorded in units of 1000kg. For the purposes 
                                of this dashboard, losses have then been calculated as a percentage of the total emissions. 
                                ''',
                            style= {
                                "text-align": "justify"
                                }),
                            html.H3(
                                "About the Red List Index",
                                ),
                            dcc.Markdown('''  
                                Red List Index (RLI) data has been sourced from the United Nations DESA statistics Division. It is updated annually 
                                (last update 23-09-2021). RLI data has been recorded annually from the first recordings in 1994 onwards.  
                                The Red List Index (RLI) is a measure of extinction risk based on the IUCN Red List categorisation of 
                                species. Species are categorized in one of seven different categories ranging from "Least Concern" to 
                                "Extinct". RLI is a numerical value, ranging between 0 and 1, that summarizes categorisations of all 
                                species within a single geographical area (for example a single country). An RLI value of 1 means all 
                                species within that geographical area are categorized "Least Concern". An RLI value of 0 means all species 
                                within that geographical area are catergorized as "Extinct".
                                ''',
                            style= {
                                "text-align": "justify"
                                }),
                            html.H3(
                                "About the Living Planet Index",
                                ),
                            dcc.Markdown('''  
                                Global Living Planet Index (LPI) data has been sourced from a collaboration between the World Wide Fund for 
                                Nature (WWF) and the Zoological Society of London (ZSL). It has been sourced from the Living Planet Report
                                from 2020, which included data from 1970 through 2016. Dutch LPI data has been sourced from the Dutch 
                                "Compendium voor de Leefomgeving" (CLO). Data ranges from 1990 through 2020.  
                                The Living Planet Index (LPI) is a measure that summarizes population trends of vertebrate species in a 
                                single geographical area, and compares current trends to a reference year. The value is always 1 in the first
                                year of comparison. It will increase when population trends improve, or decrease when population trends worsen,
                                compared to the reference year. The global data's reference year is 1970. But to make a reasonable comparison 
                                to the Dutch data, which had 1990 as reference year, the reference year has been set to 1990. All other values
                                have been adjusted accordingly.
                                ''',
                            style= {
                                "text-align": "justify"
                                }),
                            html.H3(
                                "About the predictions",
                                ),
                            dcc.Markdown('''  
                                Model predictions have been made for all measures. This means that, using trends from the past, the most likely
                                future values are calculated. Each linegraph shows a vertical line, indicating the last recorded value. Values
                                from past this line are therefor not certain.  
                                Predictions are based on an auto-regression model. This is a simple model that is commonly used to predict
                                future values from time series data (i.e., data that changes through time). The "auto" part refers to that it 
                                uses regression to predict future values of a measurement based on past values of the same measurement. The 
                                powerful characteristic of this model, is that more recent trends are more important for predicting future values.
                                This is important, because trends from longer ago are less likely to still apply today. 
                                ''',
                            style= {
                                "text-align": "justify"
                                })  
                            ]  
                        )
                    ]
                )
            ]
        )

def pagelists():
    return html.Div(
        className= "pagetext",
        children= [
            html.Div(
                className= "col",
                children= [
                    html.Div(
                        children= [
                            html.Div(
                                children= [
                                    html.H3(
                                        "Data sources"
                                        ),
                                    html.Ul(
                                        children= [
                                            html.Li(
                                                children= [
                                                    "Nitrogen Emission Data",
                                                    html.Ul(
                                                        children= [
                                                            html.Li(
                                                                children= [
                                                                    dcc.Markdown('''
                                                                        Scope:  
                                                                            Netherlands; annual totals of nitrogen emission and 
                                                                            other nitrogen numbers for each business type individually 
                                                                            and for all business types together.
                                                                        ''')
                                                                    ]
                                                                ),
                                                            html.Li(
                                                                children= [
                                                                    dcc.Markdown('''
                                                                        License:  
                                                                            Creative Commons Attribution 4.0 International (CC-BY-4.0)
                                                                        ''')
                                                                    ]
                                                                ),
                                                            html.Li(
                                                                children= [
                                                                    dcc.Markdown('''
                                                                        Update:  
                                                                            Annual update (with update after latest entry confirmed final)
                                                                        ''')
                                                                    ]
                                                                ),
                                                            html.Li(
                                                                children= [
                                                                        dcc.Link(
                                                                            href= "https://opendata.cbs.nl/statline/portal.html?_la=nl&_catalog=CBS&tableId=83983NED&_theme=305",
                                                                            children= [
                                                                                dcc.Markdown('''
                                                                                    Source:  
                                                                                        Central Bureau for Statistics (CSB)
                                                                                    ''')
                                                                                ],
                                                                            target= "_blank"
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                ),
                                            html.Li(
                                                children= [
                                                    "Red List Index",
                                                    html.Ul(
                                                        children= [
                                                            html.Li(
                                                                children= [
                                                                    dcc.Markdown('''
                                                                        Scope:  
                                                                            Global; annual measure of the red list index, 
                                                                            i.e. trends in overall extinction risk for 242 countries.
                                                                        ''')
                                                                    ]
                                                                ),
                                                            html.Li(
                                                                children= [
                                                                    dcc.Markdown('''
                                                                        License:  
                                                                            No license reported.
                                                                        ''')
                                                                    ]
                                                                ),
                                                            html.Li(
                                                                children= [
                                                                    dcc.Markdown('''
                                                                        Update:  
                                                                            Annual update
                                                                        ''')
                                                                    ]
                                                                ),
                                                            html.Li(
                                                                children= [
                                                                        dcc.Link(
                                                                            href= "https://unstats-undesa.opendata.arcgis.com/datasets/undesa::indicator-15-5-1-red-list-index/explore?location=0.134976%2C1.232241%2C2.00&showTable=true",
                                                                            children= [
                                                                                dcc.Markdown('''
                                                                                    Source:  
                                                                                        United Nations DESA Statistics Devision
                                                                                    ''')
                                                                                ],
                                                                            target= "_blank"
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                ),
                                            html.Li(
                                                children= [
                                                    "Living Planet Index",
                                                    html.Ul(
                                                        children= [
                                                            html.Li(
                                                                children= [
                                                                    dcc.Markdown('''
                                                                        Scope:  
                                                                            Global and Netherlands; annual measure of the state of 
                                                                            vertebrate biodiversity compared to reference year 
                                                                            (1970 globally, 1990 Netherlands).
                                                                        ''')
                                                                    ]
                                                                ),
                                                            html.Li(
                                                                children= [
                                                                    dcc.Markdown('''
                                                                        License:  
                                                                            Global: no CC license or equivalent; data use policy 
                                                                            provided instead.  
                                                                            Netherlands: Creative Commons Attribution 3.0 Netherlands (CC-BY-3.0 NL)
                                                                        ''')
                                                                    ]
                                                                ),
                                                            html.Li(
                                                                children= [
                                                                    dcc.Markdown('''
                                                                        Update:  
                                                                            Global: last update in Living Planet Report 2020 (data from 2016)  
                                                                            Netherlands: last update 2020
                                                                        ''')
                                                                    ]
                                                                ),
                                                            html.Li(
                                                                children= [
                                                                        dcc.Link(
                                                                            href= "http://stats.livingplanetindex.org/",
                                                                            children= [
                                                                                dcc.Markdown('''
                                                                                    Source (Global):  
                                                                                        WWF & ZSL
                                                                                    ''')
                                                                                ],
                                                                            target= "_blank"
                                                                        ),
                                                                        dcc.Link(
                                                                            href= "https://www.clo.nl/nl156907",
                                                                            children= [
                                                                                dcc.Markdown('''
                                                                                    Source (Netherlands):  
                                                                                        Compendium voor Leefomgeving
                                                                                    ''')
                                                                                ],
                                                                            target= "_blank"
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                ),
                                            html.Li(
                                                children= [
                                                    dcc.Link(
                                                        href= "https://github.com/",
                                                        children= [
                                                            dcc.Markdown('''
                                                                Explore the entire dashboard on its Github page
                                                                ''')
                                                            ],
                                                        target= "_blank"
                                                        )
                                                    ]
                                                )
                                            ]
                                        ),
                                    html.H3(
                                        "Further reading"
                                        ),
                                    html.Ul(
                                        children= [
                                            html.Li(
                                                children= [
                                                    dcc.Link(
                                                        href= "https://www.rivm.nl/stikstof",
                                                        children= "RIVM page on Nitrogen (Dutch)", 
                                                        target="_blank"   
                                                        )
                                                    ]
                                                ),
                                            html.Li(
                                                children= [
                                                    dcc.Link(
                                                        href= "https://www.iucnredlist.org/assessment/red-list-index",
                                                        children= "Red List Index", 
                                                        target="_blank"   
                                                        )
                                                    ]
                                                ),
                                            html.Li(
                                                children= [
                                                    dcc.Link(
                                                        href= "https://stats.livingplanetindex.org/",
                                                        children= "Living Planet Report 2020", 
                                                        target="_blank"   
                                                        )
                                                    ]
                                                ),
                                            html.Li(
                                                children= [
                                                    dcc.Link(
                                                        href= "https://www.clo.nl/indicatoren/nl1569-living-planet-index",
                                                        children= "Compendium voor Leefomgeving on the Living Planet Index (Dutch)", 
                                                        target="_blank"   
                                                        )
                                                    ]
                                                ),
                                            html.Li(
                                                children= [
                                                    dcc.Link(
                                                        href= "http://www.n-print.org/WWFReport",
                                                        children= '"Nitrogen: too much of a vital resource"; 2015 WWF science brief', 
                                                        target="_blank"   
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
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
            pagetext(),
            pagelists()
            ]
        )