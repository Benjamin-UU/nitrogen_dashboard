# =============================================================================
# Import relevant modules and objects from scripts
# =============================================================================
import dash
from dash import Dash, html, dcc
# =============================================================================
# This script is the main app. In includes the content that is shown across
# all pages. It also includes the main functional layout div.
# =============================================================================




# Tells dash that it should include pages in the app
app = Dash(__name__, use_pages= True)

# Defines the div that makes the banner on the top of all pages
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
                                                src= 'assets/cm_hs_new_logo_2021.png',
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
    
       
# Defines the div that makes the navigation menu the top of all pages
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

# Defines the main layout function that is called to run the app
app.layout = html.Div(
    children= [
        top_banner(app),
        menu(),
        dash.page_container
        ]
    )


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)

