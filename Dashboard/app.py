# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import Dash, html, dcc

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

#from data_loading import *


app = Dash(__name__, use_pages= True)

colors = {
    'test': '#FFFFFF',
    'background': '#2AD04A',
    'text': '#000000',
    'menu_text': '#000000'
}


def top_banner(app):
    return html.Div(
        children= [
            html.Nav(
                children= [
                    html.Ul(
                        id= 'topbanner',
                        children= [
                            html.Li(
                                children= [
                                    html.A(
                                        href= "https://www.uu.nl/en",
                                        children= [
                                            html.Img(
                                                src= app.get_asset_url('cm_hs_new_logo_2021.png'),
                                                style= {
                                                    'height': 'inherit',
                                                    'width': '320px'}
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
    
       

def menu():
    return html.Div(
        id= "menu",
        children= [
            html.Nav(
                style= {"margin-left": "5%"},
                children= [
                    html.Ul(
                        id= "topnav",
                        style= {"marin-left":"50%"},
                        children= [
                            html.Li(
                                children= [
                                    dcc.Link(
                                        dcc.Markdown(
                                            children= 
                                            '''
                                            Nitrogen- and Biodiversity  
                                            Dashboard
                                            ''',
                                            style= {
                                                "color":"#555",
                                                "font-weight": "bold",
                                                "textAlign":"left"
                                                }           
                                            ),
                                        href= "/"
                                        )
                                    ]
                                ),
                            html.Li(
                                children= [
                                    dcc.Link(
                                        href= "/nitrogen",
                                        children= "Nitrogen"
                                        )
                                    ]
                                ),
                            html.Li(
                                children= [
                                    html.A(
                                        href= "/biodiversity",
                                        children= "Biodiversity"
                                        )
                                    ]
                                ),
                            html.Li(
                                children= [
                                    html.A(
                                        href= "/about",
                                        children= "About this Dashboard"
                                        )
                                    ]
                                )                          
                            ]
                        )
                    ]
                )
            ]
        )






app.layout = html.Div(
    children= [
        top_banner(app),
        menu(),
        dash.page_container
        ]
    )






if __name__ == '__main__':
    app.run_server(debug=True)

