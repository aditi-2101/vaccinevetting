# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash import Input, Output, State
#import dash_core_components as dcc
#import dash_html_components as html
import sys
  
  


import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ["/assets/main1.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/user-info-page/')

"""colors = {
    'background': '#111111',
    'text': 'white'
}'''



app.layout = html.Div([
    html.Div(

        #style={'padding': 10, 'flex': 1,        'background-image': 'url(https://upload.wikimedia.org/wikipedia/commons/2/22/North_Star_-_invitation_background.png)'},

        #style={'padding': 10, 'flex': 1, },    # ,        'background-image': 'url(/assets/capui1.png)'},
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


            html.Div(id='container-button-basic',
             children='Enter a value and press submit', style={'font-family':'papyrus'})    #, style={"display":"none"})

        ])
        

], className="uip-outer") #style={'display': 'flex', 'flex-direction': 'row',       })      #, id="body1")

'''
@app.callback(
    Output('container-button-basic', 'children'),
    Input("submit-uip", "n_clicks"),
    State("age", "value"),
    State("gender", "value")
)
def map_values(n_clicks, age, gender):   #converts to appropriate format to send to flask
    if n_clicks==1:
        return 'The age value was "{}", the gender value was "{}", and the button has been clicked {} times'.format(
        age,
        gender,
        n_clicks
    )'''

#upon clicking the submit button, this callback gets triggered. it calls a function which registers the values entered in the input boxes
@app.callback(
    Output('container-button-basic', 'children'),
    Input("submit-uip", "n_clicks"),
    State("age", "value"),
    State("gender", "value"),
    State("meds", "value"),
    State("allergies", "value"),
    State("illness", "value")
)
def map_values(n_clicks, age, gender, meds, allergies, illness):   #converts to appropriate format to send to flask
    res={}
    #if n_clicks==1:
    if (age!=None) and age>0:
        res["age"]=age
    res["meds"]=meds
    res["allergies"]=allergies
    res["illness"]=illness
    if gender=="M" or gender=="m":
        res["gender"]=0
    elif gender=="F" or gender=="f":
        res["gender"]=1


    #if (res["age"]!=None) and res["meds"] and res["allergies"] and res["illness"] and res["gender"]:
    #keys=["age","meds","allergies","illness","gender"]
    sys.stdout.write("\n")
    sys.stdout.write(str(res))
    #sys.stdout.write("\n")

    if all (key in res for key in ("age","meds","allergies","illness","gender")) and (None not in res.values()):
        #MAKE CALL TO BACKEND HERE
    
        #submit-uip.disable
        sys.stdout.write("valid")
        return "Your results are being calculated. Please wait."
    else:
        #n_clicks=0
        sys.stdout.write("invalid")
        return "Please fill out all fields"



if __name__ == '__main__':
    app.run_server(debug=True)
    #sys.stdout.write('hello')
