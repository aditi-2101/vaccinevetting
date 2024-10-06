from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import re
import os
import shutil
import smart_open
from sys import platform
import gensim

from vector_model import get_vector, get_similarity

from risk_score import get_risk_score

from symptoms import get_symptoms, get_sympt_count


# ----------------------------------------------------------------------------------------------------------------------
# Convert free text to tags
from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import STOPWORDS


extra = [
    "twice",
    "thrice",
    "likely",
    "having",
    "apply",
    "applied",
    "morning",
    "afternoon",
    "noon",
    "evening",
    "night",
    "ate",
    "eat",
    "day",
    "days",
    "everyday",
    "dose",
    "doses",
    "yes",
    "remove",
    "removes",
    "vanish",
    "vanishes",
    "vanished",
    "see patients chart.",
    "took",
    "I",
    "weeks",
    "disappears",
    "disappear",
    "disappeared",
    "away",
    "goes",
    "dog",
    "bite",
    "mg/day",
    "mcg/day",
    "/week",
    "week",
    "mg",
    "mcg",
    "scratch",
    "scratches",
    "wound",
    "wounds",
    "till",
    "daily",
    "weekly",
    "patient",
    "reaction",
    "started",
    "age",
    "drank",
    "yesterday",
    "today",
    "ingest",
    "!",
    "?",
    "#",
    "*",
    "&",
    "^",
    "%",
    ":",
]

all_stopwords_gensim = STOPWORDS.union(set(extra))


def filter_stopwords(text):

    # filter out digits
    rem_digits = "".join([i for i in text if not i.isdigit()])

    # replace all "and" and "with" with ","
    rem_digits = rem_digits.replace(" and ", ",")
    rem_digits = rem_digits.replace(" with ", ",")

    # filter out all stopwords inlcuding extra added words
    text_tokens = word_tokenize(rem_digits)
    res = " ".join([word for word in text_tokens if not word in all_stopwords_gensim])

    return res


def split_and_clean(string):
    if "," in string:
        list_ = list(map(str.strip, string.split(",")))
        # print("comma:::::", list_)

    elif ";" in string:
        list_ = list(map(str.strip, string.split(";")))
        # print("semi colon:::::", list_)

    else:
        list_ = []
        list_.append(string)
        # print("none:::::",list_)

    res = [i for i in list_ if i]  # getting rid of all empty strings in list of strings
    return res


# ----------------------------------------------------------------------------------------------------------------------


# tags to vectors
exp = "[a-zA-Z0-9]+"


def vector_avg(vec_list):
    if vec_list:
        return sum(vec_list)/len(vec_list)
    else:
        return ''


# return np.mean(vec_list)


def get_vector_given_word(med):  # "kirk vit"
    split_med = med.split()  # ["kirk","vit"]

    vec_list = []
    for item in split_med:
        try:
            vec_list.append(
                get_vector(item)
            )  # converting each word in the medicine name to a
        except:
            # print("exception!!")
            continue

        """if model[item]:
            vec_list.append(model[item])  #converting each word in the medicine name to a 
        else:
            continue"""

    # calc vector avg of all words in medicine name
    vector = vector_avg(vec_list)

    return vector


# def get_similarity(vector):
#     sim=model.similar_by_vector(vector, topn=11, restrict_vocab=None)
#     return sim


def medstring_to_vector(medstring):
    print(f"medstring_to_vector : {medstring}")
    meds = re.findall(exp, medstring)
    # print(meds)    #['kirkland multivitamin', 'kirkland calcium vitamin', 'vitamin d', 'fish oil']

    # list of vectors of the medicine names in each row
    # [v(kirkland multivitamin), v(kirkland calcium vitamin), v(vitamin d), v(fish oil)]
    print(f"meds: {meds}")
    vec_list = []

    for item in meds:
        # try:
        v = get_vector_given_word(item)
        vec_list.append(v)

    # avg of all med vectors in a row (for a user/entry)
    if vec_list:
        meds_avg = vector_avg(vec_list)
        return meds_avg
    else:
        return -1


# ----------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Get tags from free text
    if data["meds"]:
        meds_tags = filter_stopwords(data["meds"])
        meds_tags = split_and_clean(meds_tags)
        print("meds_tags:", meds_tags)
    if data["illness"]:
        illness_tags = filter_stopwords(data["illness"])
        illness_tags = split_and_clean(illness_tags)
        print("illness_tags:", illness_tags)
    if data["allergies"]:
        allergies_tags = filter_stopwords(data["allergies"])
        allergies_tags = split_and_clean(allergies_tags)
        print("allergies_tags:", allergies_tags)

    # # Get vector from tags
    # print(meds_tags[0])
    # vect=get_vector(meds_tags[0])
    # print("vect:", vect)

    # pls
    # print("this is main med vector")
    # print(medstring_to_vector(str(meds_tags)))

    meds_vector = medstring_to_vector(str(meds_tags))
    # print("similarrity meds")
    # print(get_similarity(meds_vector))

    allergies_vector = medstring_to_vector(str(allergies_tags))
    # print("similarrity allergies")
    # print(get_similarity(allergies_vector))

    illness_vector = medstring_to_vector(str(illness_tags))
    # print("similarrity illness")
    # print(get_similarity(illness_vector))



    age=data["age"]
    gender=data["gender"]

    meds_vector=np.append(meds_vector, age)
    allergies_vector=np.append(allergies_vector, age)
    illness_vector=np.append(illness_vector, age)

    if gender==1:
        meds_vector=np.append(meds_vector,1)
        meds_vector=np.append(meds_vector,0)
        allergies_vector=np.append(allergies_vector,1)
        allergies_vector=np.append(allergies_vector,0)
        illness_vector=np.append(illness_vector,1)
        illness_vector=np.append(illness_vector,0)
    else:
        meds_vector=np.append(meds_vector,0)
        meds_vector=np.append(meds_vector,1)
        allergies_vector=np.append(allergies_vector,0)
        allergies_vector=np.append(allergies_vector,1)
        illness_vector=np.append(illness_vector,0)
        illness_vector=np.append(illness_vector,1)



    risk_and_sym=get_risk_score(age, gender, meds_vector, allergies_vector, illness_vector)
    print(risk_and_sym)
    # data = {"status": 200, "payload": {"vaccineName": "Pfizer", "riskScore": 3}}
    return jsonify(risk_and_sym)
    # return str(meds_tags)


    # {
    #     "pfizer" : {
    #         "symptoms" : ["fever", "cough", "sore throat"],
    #         "score" : 3
    #     }
    # }
