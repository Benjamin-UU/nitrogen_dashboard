import dash
import plotly.graph_objs as go
from dash import html, dcc
from data_loading import *

dash.register_page(__name__, path='/')

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
                                "Nitrogen emissions and the Nitrogen crisis",
                                ),
                            dcc.Markdown('''
                                On the 29th of May 2019, the Dutch government was forced to take action on the increasing rates of nitrogen emissions. 
                                The Dutch Council of State (Raad van State) made important rulings around the "Programma Aanpak Stikstof" (PAS), a Dutch 
                                policy concerning the protection of Natura 2000 nature reserves in the Netherlands. These rulings state that the PAS would 
                                no longer be allowed to be used as argument for permitting activities that cause additional nitrogen emission. This resulted 
                                in the halting of countless building projects and other planning activities, something that would quickly be referred to as 
                                the "nitrogen crisis". This nitrogen crisis forced the hand of the Dutch government, and ways to reduce nitrogen emission 
                                nation-wide were essential to prevent a long term freeze on building- and public space planning activities.
                                  
                                **This dashboard is meant to provide clear and unbiased information to the general public on the Nitrogen crisis. This page 
                                will provide general information on the Nitrogen crisis, the effects of nitrogen on biodiversity, and more. Use the menu to
                                navigate to the Nitrogen or Biodiversity pages to see figures on the past, current, and predicted future situation**
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

def chartsection(dataFrame, title= "Graph Title"):
    return html.Div(        
        children= [
            dcc.Graph(
                figure= pieChart(dataFrame, title)
                )
            ]
        )

def pieChart(dataFrame, title):
    
    fig= go.Figure()
    
    
    fig.add_traces(go.Pie(labels= dataFrame["Source"],
                          values= dataFrame["Percentage"]))
    
    fig.update_traces(hoverinfo= "label+percent", 
                      textposition='inside', textinfo='label+percent')
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      showlegend= False,
                      height= 400,
                      title_text= title
                      )    
    
    return fig
                                      
def textSection(): 
    return html.Div(
    id= "float-parent-element",
    children= [
        html.Div(
            className= "float-child-element",
            children= [
                html.Div(
                    className= "left-Main",
                    children= [
                        html.H3(
                            "Why is Nitrogen bad for the environment?",
                            ),
                        dcc.Markdown('''
                            The entire Nitrogen crisis was caused by measurements of exessive nitrogen levels in Dutch nature reserves, in particular the 
                            Natura 2000 nature reserves. **But why are high nitrogen levels a bad thing?**  
                            The answer to this is biodiversity. Throughout the past two decades much research has been done on the effects of high nitrogen 
                            levels in the soil of natural systems. The conclusive evidence of numerous experiments, surveys and reviews is that **high nitrogen 
                            levels cause biodiversity decline**. Healthy natural ecosystems have a naturally low level of nitrogen in the soil. This makes it that
                            there are a lot of different niches, or comfort zones, that can be filled by different plant species. When there are many different 
                            plant species, this will also create living space for many different animals. But even more importantly, **a healthy and diverse 
                            ecosystem will be more stable and resilient.** Droughts, floods, fires, and other major disturbances can all heavily damage ecosystems. 
                            But when an ecosystem is healthy and most of its niches are filled, there will always be species that will survive the event. And from 
                            here, it can regrow to its former glory.  
                            However, when nitrogen levels become higher, it becomes very easy for some plant species to outcompete others. Grasses are especially 
                            good at this. These are often very quick growing plants that love soil with a lot of nitrogen. This can be fine as long as there are
                            no disturbances, but if something happens now that will kill most nitrogen loving plants, suddenly there are far fewer species left.
                            And so **high nitrogen levels can make it very difficult for an ecosystem to recover**. 
                            
                            ''',
                        style= {
                            "margin-bottom": "5%",
                            "text-align": "justify"
                            }),
                        html.H3(
                            "Where does the nitrogen come from?"
                            ),
                        dcc.Markdown('''
                            Most of the nitrogen emmitted into the air is either ammoniak or nitrous oxide and comes from human activities such as agriculture, 
                            industry and traffic. According to the Central Bureau for Statistics (CBS), 87% of human caused ammonia emissions, and 7,5% of human 
                            caused nitrogen oxide comes from the agricultural sector. In total, **over 55% of the nitrogen emissions in the Netherlands are caused
                            by the agricultural sector**. 
                            ''',
                        style= {
                            "margin-bottom": "5%",
                            "text-align": "justify"
                            }),                         
                        html.H3(
                            "How bad is the nitrogen situation in the Netherlands?"
                            ),
                        dcc.Markdown('''
                            The Netherlands is  
                            ''',
                        style= {
                            "margin-bottom": "5%",
                            "text-align": "justify"
                            })                      
                        ]
                    )
                ]
            ),
        html.Div(
            className= "float-child-element",
            children= [
                html.Div(
                    className= "left-Main",
                    children= [
                        html.H3(
                            "Why is Nitrogen bad for the environment?",
                            ),
                        dcc.Markdown('''
                            The entire Nitrogen crisis was caused by measurements of exessive nitrogen levels in Dutch nature reserves, in particular the 
                            Natura 2000 nature reserves. **But why are high nitrogen levels a bad thing?**  
                            The answer to this is biodiversity. Throughout the past two decades much research has been done on the effects of high nitrogen 
                            levels in the soil of natural systems. The conclusive evidence of numerous experiments, surveys and reviews is that **high nitrogen 
                            levels cause biodiversity decline**. Healthy natural ecosystems have a naturally low level of nitrogen in the soil. This makes it that
                            there are a lot of different niches, or comfort zones, that can be filled by different plant species. When there are many different 
                            plant species, this will also create living space for many different animals. But even more importantly, **a healthy and diverse 
                            ecosystem will be more stable and resilient.** Droughts, floods, fires, and other major disturbances can all heavily damage ecosystems. 
                            But when an ecosystem is healthy and most of its niches are filled, there will always be species that will survive the event. And from 
                            here, it can regrow to its former glory.  
                            However, when nitrogen levels become higher, it becomes very easy for some plant species to outcompete others. Grasses are especially 
                            good at this. These are often very quick growing plants that love soil with a lot of nitrogen. This can be fine as long as there are
                            no disturbances, but if something happens now that will kill most nitrogen loving plants, suddenly there are far fewer species left.
                            And so **high nitrogen levels can make it very difficult for an ecosystem to recover**. 
                            
                            ''',
                        style= {
                            "margin-bottom": "5%",
                            "text-align": "justify"
                            })                    
                        ]
                    )
                ]
            ),
        html.Div(
            className= "float-child-element",
            children= [
                html.Div(
                    className= "right-Main",
                    children= [
                        html.Div(
                            id= "float-parent-element-3",
                            children= [
                                html.Div(
                                    className= "float-child-element",
                                    children= [
                                        html.Div(
                                            className= "left-sub",
                                            children= [
                                                chartsection(CBS_NHx, 
                                                             title= "Percentage NHx emissions per sector")
                                                ]
                                            )
                                        ]
                                    ),
                                html.Div(
                                    className= "float-child-element",
                                    children= [
                                        html.Div(
                                            className= "right-sub",
                                            children= [
                                                chartsection(CBS_NOx, 
                                                             title= "Percentage NOx emissions per sector")
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
            textSection()
            ]
        )