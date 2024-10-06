import numpy as np
import pandas as pd
from scipy import spatial
from symptoms import get_symptoms

only_risky=pd.read_csv('onlyrisky.csv')

print("in RISK SCORE")


def vector_avg(vec_list):
    vec_list=[np.array(i) for i in vec_list]
    return sum(vec_list)/len(vec_list)


def tofloatlist(row):
    row_list=(((row)).split())
    return list(map(float,row_list))


for i,j in only_risky["meds_vector"].iteritems():
    only_risky["meds_vector"][i]=tofloatlist(only_risky["meds_vector"][i])

for i,j in only_risky["allergies_vector"].iteritems():
    only_risky["allergies_vector"][i]=tofloatlist(only_risky["allergies_vector"][i])

for i,j in only_risky["history_vector"].iteritems():
    only_risky["history_vector"][i]=tofloatlist(only_risky["history_vector"][i])

return_data={}

def get_risk_score(age, gender, user_med_vector, user_allergy_vector, user_history_vector):

    print(type(age))
    age=int(age)
    gender=int(gender)

    age_grp_df = only_risky.loc[(only_risky['AGE_YRS'] >= age-20) & (only_risky['AGE_YRS'] <= age+20)]

    age_and_gender_df=age_grp_df[age_grp_df["SEX_F"]==gender]

    # vec_list=[]

    vaccine_list=[ "COVID19 (COVID19 (PFIZER-BIONTECH))","COVID19 (COVID19 (MODERNA))","COVID19 (COVID19 (JANSSEN))"]

    for vaccine in vaccine_list:
        print(vaccine)
        vec_list_meds=[]
        vec_list_allergies=[]
        vec_list_history=[]

        vacdf=age_and_gender_df[age_and_gender_df['VAX_NAME']==vaccine]


        # print(vacdf)


        for i in vacdf["meds_vector"]:
            if len(i)==303:
                vec_list_meds.append(i)
            
        for i in vacdf["allergies_vector"]:
            if len(i)==303:
                vec_list_allergies.append(i)
            
        for i in vacdf["history_vector"]:
            if len(i)==303:
                vec_list_history.append(i)

        avg_vector_meds=vector_avg(vec_list_meds)
        avg_vector_allergies=vector_avg(vec_list_allergies)
        avg_vector_history=vector_avg(vec_list_history)

        
        result_meds=spatial.distance.cosine(avg_vector_meds,user_med_vector)
        result_allergies=spatial.distance.cosine(avg_vector_allergies,user_allergy_vector)
        result_history=spatial.distance.cosine(avg_vector_history,user_history_vector)
        
        print("Vaccine name:", vaccine)

        print("Risk Percentage :",max(result_meds,result_allergies, result_history)*100)


        symptoms=get_symptoms(vaccine, age, user_med_vector)

        return_data[vaccine]={
            "symptoms":symptoms,
            "score":max(result_meds,result_allergies, result_history)*100
        }
    
    return return_data