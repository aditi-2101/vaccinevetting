import dash
from dash import dcc
from dash import html
#import dash_core_components as dcc
#import dash_html_components as html
from dash import Input, Output, State
import sys
from dash.exceptions import PreventUpdate
import requests
import ast
from datetime import datetime

external_stylesheets = ['/assets/main-final.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    #dcc.Location(id='url2', refresh=False),
    html.Div(id='page-content'),
    #html.Div(id='pc-2')
    dcc.Store(id='session', storage_type='session')

    
])

#---------------------------------------------------------

landing_page = html.Div([
    html.Div(

        style={'padding': 10, 'flex': 1}, 
        
        children=[
            
            html.Br(),
            html.H1(children='Welcome to Deltoid!', style={'textAlign': 'center'}, className='heading'),
            html.H3(children='Your Very Own Vaccine Vetting App!', style={'textAlign': 'center'}, className='heading2'),


            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),

            
            dcc.Link(html.Button('Get Started', className='submit2'), href='/user-info-page/', refresh=True)

            
        ]
    )
])

#---------------------------------------------------------

user_info_page = html.Div(className="uip-outer", children=[
                dcc.Link(html.Button('Deltoid', className='deltoid-button'), href='/', refresh=True),
    #html.H1(children='User Info Collection', style={'textAlign': 'center'}, className='heading'),
    #html.H3(children='Provide Your Information As Shown Below', style={'textAlign': 'center'}, className='heading2'),
                html.Div(className="uip-middle", children=[
                        
                        html.H1(children='User Info Collection', style={'textAlign': 'center'}, className='heading'),
                        html.H3(children='Provide Your Information As Shown Below', style={'textAlign': 'center'}, className='heading2'),
                        html.Div(className="uip", children=[

                                    html.Br(),
                                    #html.H1(children='User Info Collection', style={'textAlign': 'center'}, className='heading'),
                                    #html.H3(children='Provide Your Information As Shown Below', style={'textAlign': 'center'}, className='heading2'),

                                    html.Br(),
                                    html.Br(),
                                

                                    html.Label('Age    ', className='label'),
                                    dcc.Input(type="number", id="age", placeholder='(enter in numbers)', size='15',   className='tb', autoComplete="off"),

                                    html.Br(),
                                    html.Br(),

                                    html.Label('Gender    ', className='label'),
                                    dcc.Input(id="gender", placeholder='M / F', type='text', size='15',   className='tb', autoComplete="off"),

                                    html.Br(),
                                    html.Br(),
                                    
                                    html.Label('Current Medications    ',  className='label'),
                                    dcc.Input(id="meds", placeholder='medicine A, medicine B, medicine C, ...', type='text', size='50',   className='tb', autoComplete="off"),

                                    html.Br(),
                                    html.Br(),
                                    
                                    html.Label('Allergies    ',  className='label'),
                                    dcc.Input(id="allergies", placeholder='allergy A, allergy B, allergy C, ...', type='text', size='50',   className='tb', autoComplete="off"),

                                    html.Br(),
                                    html.Br(),
                                    
                                    html.Label('History of Illness    ',  className='label'),
                                    dcc.Input(id="illness", placeholder='illness A, illness B, illness C, ...', type='text', size='50',   className='tb', autoComplete="off"),

                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Button('Submit', className='submit', id="submit-uip", n_clicks=0),
                                    html.Br(),
                                    #red1 - #701816
                                    #red2 - #ba2d1e
                                    html.Label('(Please fill out all fields)',  style={'font-family':'papyrus', 'color': '#b00c09',  'font-weight':'bold'}),

                                    html.Br(),
                                    html.Br(),
                                    
                                    
                                    #dcc.Link(html.Button('Check Results', id="res-button", className='submit', disabled=True), href='/results/', refresh=True),
                                    #html.Button('Check Results', id="res-button", disabled=True , className='submit')

                                    #html.Label('Please fill out all fields',  className='label')
                                    
                                    html.H3(id="res-loading-message", style={'font-family':'papyrus', 'display':'inline-block', 'color': '#086c80', 'background-color':'#57c98c', 'font-weight':'bold'}, children=[]),
                                    html.Br(),
                                    

                                    html.Div(id="res-button-div", style={'font-family':'papyrus', 'display':'block'}, children=[])

                                    #html.Div(id='container-button-basic', children='Enter a value and press submit', style={'font-family':'papyrus'})

                    ])
                ])       
            ]) 


#CALLBACK TO DISPLAY LOADING MESSAGE
@app.callback(
    Output("res-loading-message","children"),
    Output("submit-uip", "disabled"),
    Output("submit-uip", "style"),
    Input("submit-uip","n_clicks"),
    State("age", "value"),
    State("gender", "value"),
    State("meds", "value"),
    State("allergies", "value"),
    State("illness", "value"),
)
def print_loading_message(n_clicks, age, gender, meds, allergies, illness):
    if n_clicks!=None and n_clicks>0:
        if (age!=None and age>0) and (gender in ["M","F","m","f"]) and (None not in (age,gender,meds,allergies,illness)) and ('' not in (age,gender,meds,allergies,illness)):
            sys.stdout.write("\n")
            sys.stdout.write("\n")
            sys.stdout.write("in loading message callback")
            disable=True
            disable_style={"background-color": "gray", "cursor": "default"}
            return "The results are being calculated, please wait...", disable, disable_style
    return None, None, None



#1st store callback (writing to store)
#CLICKING SUBMIT BUTTON CALLBACK
@app.callback(
    Output('session', 'data'),
    #Output('pc-2', 'children'),
    #Output("url", "pathname"),
    #Output("res-button", "disabled"),
    Output("res-button-div", "children"),
    #Output("submit-uip", "disabled"),
    #Output("submit-uip", "style"),
    Input("submit-uip", "n_clicks"),
    State("age", "value"),
    State("gender", "value"),
    State("meds", "value"),
    State("allergies", "value"),
    State("illness", "value"),
    State("session", "data"),
    State("session","modified_timestamp")
)
def map_values(n_clicks, age, gender, meds, allergies, illness, data, modified_timestamp):   #converts to appropriate format to send to flask

    if n_clicks is None:
            # prevent the None callbacks is important with the store component.
            # you don't want to update the store for nothing.
            raise PreventUpdate
            
    if n_clicks>0:
        res={}
        if (age!=None) and age>0:
            res["age"]=age
        res["meds"]=meds
        res["allergies"]=allergies
        res["illness"]=illness
        if gender=="M" or gender=="m":
            res["gender"]=0
        elif gender=="F" or gender=="f":
            res["gender"]=1


        sys.stdout.write("\n")
        sys.stdout.write("\n")
        sys.stdout.write("-------------------------")
        sys.stdout.write("starting a fresh run")
        sys.stdout.write("-------------------------")
        sys.stdout.write("\n")
        sys.stdout.write(str(datetime.now()))
        
        sys.stdout.write("\n")
        sys.stdout.write("\n")
        sys.stdout.write("user's values-")
        sys.stdout.write("\n")
        sys.stdout.write(str(res))
        

        if all (key in res for key in ("age","meds","allergies","illness","gender")) and (None not in res.values()) and '' not in res.values():
            #MAKE CALL TO BACKEND HERE
            sys.stdout.write("\n")
            sys.stdout.write("Making the backend call")
            sys.stdout.write("\n")

            b_data=requests.post("http://127.0.0.1:5000/predict", json=res)

            sys.stdout.write("\n")
            sys.stdout.write("returned from backend-\n")
            b_res_str=b_data.text
            sys.stdout.write(b_res_str)

            sys.stdout.write("\n")
            sys.stdout.write("backend returns string-\n")
            sys.stdout.write(str(type(b_res_str)))

            #sys.stdout.write("\n")
            #sys.stdout.write(str(b_res_str))

            #b_res=dict(b_res_str)
            b_res=ast.literal_eval(b_res_str)
            sys.stdout.write("\n")
            sys.stdout.write("converted it to dict type-")
            sys.stdout.write("\n")
            sys.stdout.write(str(type(b_res)))
            sys.stdout.write("\n")

            
            #backend returns var called "b_res"
            # b_res={
            #             "moderna" : {
            #                     "symptoms" : ["m_symptom1", "m_symptom2", "m_symptom3"],
            #                     "score" : 23
            #                 },
            #             "pfizer": {
            #                     "symptoms" : ["p_symptom1", "p_symptom2", "p_symptom3"],
            #                     "score" : 46
            #                 }
            #         }
        
            #sys.stdout.write(str(b_res))
        
            sys.stdout.write("\n")
            sys.stdout.write("valid")

            sys.stdout.write("\n")
            sys.stdout.write("************************************************")
            sys.stdout.write("\n")

            
            data = data or {'stored_data': None}
            data={}
            data['stored_data']=b_res
            sys.stdout.write("\n")
            sys.stdout.write(str(data))

            sys.stdout.write("\n")
            sys.stdout.write("\n")
            sys.stdout.write("************************************************")
            sys.stdout.write("\n")
            
            #dcc.Link(html.Button('Check Results', className='submit'), href='/results/', refresh=True),
            #disable=False
            #path="/results/"
            #path=dcc.Location(pathname="/results/", id="page-content")

            #result_button=html.Button('Check Results', id="res-button", className='submit')#, n_clicks=1)
            result_button=dcc.Link(html.Button('Check Results', id="res-button", className='submit'),href="/results/")
            #disable=True
            #disable_style={"background-color": "gray", "cursor": "default"}
            return data, result_button #, disable, disable_style
            #return data, result_button       #disable #, path #dcc.Location(pathname="/results/", id="page-content")      #, results_page
            #return str(res)
            #return dcc.Location(pathname="/results/", id="page-content")
            #dcc.Location(pathname="/results/", id="page-content")
        else:
            sys.stdout.write("invalid")
            return None, None #, None, None
            #return
            #return "Please fill out all fields"
    return None, None #, None, None

"""
#CLICKING GET RESULTS BUTTON CALLBACK
@app.callback(
    Output('url','pathname'),
    Input('res-button','n_clicks'))
def redirect_to_results_page(n_clicks):
    if n_clicks!=None and n_clicks>0:
        sys.stdout.write("\n")
        sys.stdout.write("\n")
        sys.stdout.write("--------------  ")
        sys.stdout.write("inside get results button click callback. redirecting to results page...")
        sys.stdout.write("  --------------")
        sys.stdout.write("\n")
        sys.stdout.write("\n")
        return "/results/" #dcc.Location(id="page-content", pathname="/results/")
"""

#---------------------------------------------------------
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
}'''


#2nd store callback (reading from store upon url change)
@app.callback(
    Output("results-page","children"),
    Input("url", "pathname"),
    State("session","data")
    
)
def get_results(n_clicks, data):

    sys.stdout.write("\ninside store read callback\n")

    def on_data(ts, data):
        if ts is None:
            raise PreventUpdate
    
    if data is None:
        #return None
        ms="Nothing to display!"
        mr="Nothing to display!"
        ps="Nothing to display!"
        pr="Nothing to display!"

    else:

        ms=data["stored_data"]["COVID19 (COVID19 (MODERNA))"]["symptoms"] #list
        mr=str(round(data["stored_data"]["COVID19 (COVID19 (MODERNA))"]["score"], 2))+"%"
        ps=data["stored_data"]["COVID19 (COVID19 (PFIZER-BIONTECH))"]["symptoms"]
        pr=str(round(data["stored_data"]["COVID19 (COVID19 (PFIZER-BIONTECH))"]["score"], 2))+"%"

    sys.stdout.write(str(ms))
    sys.stdout.write("\n")

    sys.stdout.write(mr)
    sys.stdout.write("\n")

    sys.stdout.write(str(ps))
    sys.stdout.write("\n")

    sys.stdout.write(pr)
    sys.stdout.write("\n")



    new=html.Div(

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
                                html.Ol(className="label3", id="mod-symp", children=([html.Li(i) for i in ms if type(ms) is list] or str([ms for i in "a" if type(ms) is str]).strip("['']") )),   #children=[html.Li(i) for i in ms]
                                


                                html.Br(),
                                html.H5("- Risk Percentage", className="label2"),
                                html.Ul(children=[mr], className="label3", id="mod-risk")
                            ]
                        ),

                        html.Div(
                            className="flex-child",
                            children=[
                                html.H4("PFIZER", className="label3"),

                                html.H5("- Symptoms", className="label2"),
                                html.Ol(className="label3", id="pf-symp", children=([html.Li(i) for i in ps if type(ps) is list] or str([ps for i in "a" if type(ps) is str]).strip("['']") )),      #children=[html.Li(i) for i in ps]

                                html.Br(),
                                html.H5("- Risk Percentage", className="label2"),
                                html.Ul(children=[pr], className="label3", id="pf-risk")
                            ]
                            
                        )
                    ]
                    )
        ])

    
    return new  #, data#ms,mr,ps,pr  #, dcc.Location(pathname="/results/", id="pc2")




results_page=html.Div([
                html.Div( className="r", children=[
                                dcc.Link(html.Button('Deltoid', className='deltoid-button'), href='/', refresh=True),
                                dcc.Link(html.Button('Calculate Again', className='calc-again-button'), href='/user-info-page/', refresh=True),
                                html.Div(

                                    #className="r",
                                    id="results-page",
                
                                    children=[
                                
                                    ])
                ])

    ], className="r-outer")


#---------------------------------------------------------


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/user-info-page/':
        return user_info_page
    elif pathname == '/results/':
        return results_page
    else:
        return landing_page
    # You could also return a 404 "URL not found" page here



if __name__ == '__main__':
    app.run_server(debug=True)