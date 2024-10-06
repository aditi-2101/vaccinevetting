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

user_info_page = html.Div([
    
    html.Div(

        className="uip",
        
        children=[

            
            html.Br(),
            html.H1(children='User Info Collection', style={'textAlign': 'center'}, className='heading'),
            html.H3(children='Provide Your Information As Shown Below', style={'textAlign': 'center'}, className='heading2'),

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
            html.Label('Please fill out all fields',  className='label'),

            html.Br(),
            html.Br(),
            html.Br(),
            #dcc.Link(html.Button('Check Results', className='submit'), href='/results/', refresh=True),

            #html.Label('Please fill out all fields',  className='label')


            #html.Div(id='container-button-basic', children='Enter a value and press submit', style={'font-family':'papyrus'})

        ])
        

], className="uip-outer") 


#upon clicking the submit button, this callback gets triggered. it calls a function which registers the values entered in the input boxes
@app.callback(
    Output('session', 'data'),
    #Output('pc-2', 'children'),
    #Output("url", "pathname"),
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

            #path=dcc.Location(pathname="/results/", id="page-content")
            return data #, dcc.Location(pathname="/results/", id="page-content")      #, results_page
            #return str(res)
            #return dcc.Location(pathname="/results/", id="page-content")
            #dcc.Location(pathname="/results/", id="page-content")
        else:
            sys.stdout.write("invalid")
            return None, None
            #return
            #return "Please fill out all fields"
    return None, None

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



@app.callback(
    Output("results-page","children"),
    Input("url", "pathname"),
    State("session","data")
    
)
def get_results(n_clicks, data):

    def on_data(ts, data):
        if ts is None:
            raise PreventUpdate
    
       
    sys.stdout.write("\ninside store read callback\n")

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
                                html.Ol(className="label3", id="mod-symp", children=[html.Li(i) for i in ms]),
                                


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
                                html.Ol(className="label3", id="pf-symp", children=[html.Li(i) for i in ps]),

                                html.Br(),
                                html.H5("- Risk Percentage", className="label2"),
                                html.Ul(children=[pr], className="label3", id="pf-risk")
                            ]
                            
                        )
                    ]
                    )
        ])


    
    
    return new#ms,mr,ps,pr  #, dcc.Location(pathname="/results/", id="pc2")




results_page=html.Div([
    html.Div(

        className="r",
        id="results-page",
        
        children=[
            
            
            

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