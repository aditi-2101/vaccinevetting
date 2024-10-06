from flask import Flask, render_template, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.i18n import messages_path
from wtforms.validators import DataRequired
import uuid
import requests
import json
import time

from totags import convert_to_tags

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb"
Bootstrap(app)


DISEASE_CHOICES = ["COVID", "Influenza"]
STATE_CHOICES = [
    "Alaska",
    "Alabama",
    "Arkansas",
    "American Samoa",
    "Arizona",
    "California",
    "Colorado",
    "Connecticut",
    "District ",
    "of Columbia",
    "Delaware",
    "Florida",
    "Georgia",
    "Guam",
    "Hawaii",
    "Iowa",
    "Idaho",
    "Illinois",
    "Indiana",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Massachusetts",
    "Maryland",
    "Maine",
    "Michigan",
    "Minnesota",
    "Missouri",
    "Mississippi",
    "Montana",
    "North Carolina",
    "North Dakota",
    "Nebraska",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "Nevada",
    "New York",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Puerto Rico",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Virginia",
    "Virgin Islands",
    "Vermont",
    "Washington",
    "Wisconsin",
    "West Virginia",
    "Wyoming",
]
SEX_CHOICES = ["M", "F"]


class NameForm(FlaskForm):
    Disease = SelectField("Disease", choices=DISEASE_CHOICES)
    # name = StringField('Name of Disease', validators=[DataRequired()])
    Age = IntegerField("Age?", validators=[DataRequired()])
    Sex = SelectField("Sex?", choices=SEX_CHOICES)
    State = SelectField("US State of residence?", choices=STATE_CHOICES)
    Medication = StringField("Current Medication?", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():

    form = NameForm()
    message = ""
    id = str(uuid.uuid4())
    if form.validate_on_submit():
        disease = form.Disease.data
        age = form.Age.data
        sex = form.Sex.data
        state = form.State.data
        medication = form.Medication.data

        medication_li = convert_to_tags(medication)
        # med_li=",".join(med_li)
        # time.sleep(5)

        user = {
            "uuid": id,
            "disease": disease,
            "age": age,
            "sex": sex,
            "state": state,
            # "allergies":allergies_li,
            # "illness":illness_li,
            "medication": medication_li,
        }

        x = requests.post(
            "https://ii13si51v7.execute-api.us-west-2.amazonaws.com/test", json=user
        )

        if disease == "COVID":
            return redirect("COVID/" + id)

        elif disease == "Influenza":
            return redirect("Influenza/" + id)

        # message = "Thank you for your responsee"+ name
    return render_template("index.html", form=form)


@app.route("/COVID/<uuid>")
def covid_vaccines(uuid):
    return render_template("covid.html")


@app.route("/Influenza/<uuid>")
def influenza_vaccines(uuid):
    return render_template("influenza.html")
