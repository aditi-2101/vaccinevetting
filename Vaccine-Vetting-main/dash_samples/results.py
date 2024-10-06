# visit http://127.0.0.1:8050/ in your web browser.

import dash
# from dash import dcc
# from dash import html
import dash_core_components as dcc
import dash_html_components as html
import requests
import json

external_stylesheets = ['/assets/main2.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, eager_loading=True, url_base_pathname='/results/')
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

'''res={'MODERNA': [['symptom 1', 'symptom 2', 'symptom 3'],["23%"]],
    'PFIZER': [['symptom 4', 'symptom 5', 'symptom 6'],["46%"]]}'''

'''
 {
        "pfizer" : {
            "symptoms" : ["fever", "cough", "sore throat"],
            "score" : 3
        }
    }
'''
res={
    "moderna" : {
            "symptoms" : ["m_symptom1", "m_symptom2", "m_symptom3"],
            "score" : 23
        },
    "pfizer": {
            "symptoms" : ["p_symptom1", "p_symptom2", "p_symptom3"],
            "score" : 46
        }
}

#trends=["a","b","c"]

def serve_layout():
    return html.Div([
    html.Div(

        #style={'padding': 10, 'flex': 1,        'background-image': 'url(https://upload.wikimedia.org/wikipedia/commons/2/22/North_Star_-_invitation_background.png)'},
        className="r",
        #style={'padding': 10, 'flex': 1},    # ,        'background-image': 'url(/assets/capui1.png)'},
        
        children=[
            
            html.Br(),
            html.H1(children='Results', style={'textAlign': 'center'}, className='heading'),
            

            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),

            html.H3("Available Vaccines", className="heading"),
            
            #this is being displayed statically (assuming only two vaccines are available, since we're only doing covid)
            html.Div(
                    className="flex-container",
                    children=[

                        html.Div(
                            className="flex-child",
                            children=[
                                html.H4("MODERNA", className="label3"),

                                html.H5("- Symptoms", className="label2"),
                                html.Ol(className="label3", children=[html.Li(i) for i in res["moderna"]["symptoms"]]),

                                html.Br(),
                                html.H5("- Risk Percentage", className="label2"),
                                html.Ul(str(res["moderna"]["score"])+"%", className="label3")
                            ]
                        ),

                        html.Div(
                            className="flex-child",
                            children=[
                                html.H4("PFIZER", className="label3"),

                                html.H5("- Symptoms", className="label2"),
                                html.Ol(className="label3", children=[html.Li(i) for i in res["pfizer"]["symptoms"]]),

                                html.Br(),
                                html.H5("- Risk Percentage", className="label2"),
                                html.Ul(str(res["pfizer"]["score"])+"%", className="label3")
                            ]
                             
                        )
                    ]
                    )
            

        ])
    ], className="r-outer")   #style={'display': 'flex', 'flex-direction': 'row'  })

app.layout=serve_layout


if __name__ == '__main__':
    app.run_server(debug=True)