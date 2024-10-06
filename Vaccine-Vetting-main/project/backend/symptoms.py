import numpy as np
import pandas as pd

data=pd.read_csv("someeee.csv")

sympt_df=pd.read_csv("2021VAERSSYMPTOMS_clean3.csv")

vax_df=pd.read_csv("2021VAERSVAX_clean3.csv")

janssen_df = vax_df[vax_df['VAX_NAME'] == 'COVID19 (COVID19 (JANSSEN))']
moderna_df = vax_df[vax_df['VAX_NAME'] == 'COVID19 (COVID19 (MODERNA))']
pfizer_df = vax_df[vax_df['VAX_NAME'] == 'COVID19 (COVID19 (PFIZER-BIONTECH))']

print(moderna_df.head())

#def get_symptoms(vax_df,age_grp_df,user_medvec,user_allervec,user_hoivec):
def get_symptoms(vaxname,age,sympt_dict,user_vec):
    if vaxname=='COVID19 (COVID19 (PFIZER-BIONTECH))':
        vax_df=pfizer_df
    elif vaxname=='COVID19 (COVID19 (MODERNA))':
        vax_df=moderna_df
    elif vaxname=='COVID19 (COVID19 (JANSSEN))':
        vax_df=janssen_df
    else:
        symptoms=["No symptoms found"]
        return symptoms

    age_grp_df = data.loc[(data['AGE_YRS'] >= age-5) & (data['AGE_YRS'] <= age+5)]
    age_vax_df = pd.merge(vax_df, age_grp_df, how = 'inner', on = 'VAERS_ID')
    #age_vax_df = age_vax_df[['VAERS_ID','VAX_NAME','meds_vector']]
    # age_vax_df = age_vax_df[['VAERS_ID','VAX_NAME','meds_vector']]
    #print(len(age_vax_df))
    #print(age_vax_df.head())
    #exit()

    age_vax_df['similarity_score']=""
    #for i,j in age_vax_df["meds_vector"].iteritems():
    for i,j in age_vax_df["meds_vector"].iteritems():
        if type(j) == np.ndarray:
            #print(type(j))
            '''
            meds_sim_score = np.dot(user_medvec, j)/(np.linalg.norm(user_medvec)* np.linalg.norm(j))
            allergy_sim_score = np.dot(user_allervec, j)/(np.linalg.norm(user_allervec)* np.linalg.norm(j))
            hoi_sim_score = np.dot(user_hoivec, j)/(np.linalg.norm(user_hoivec)* np.linalg.norm(j))
            #avg of 3 vectors
            sim_score = (meds_sim_score + allergy_sim_score + hoi_sim_score)/3
            '''
            sim_score = np.dot(user_vec, j)/(np.linalg.norm(user_vec)* np.linalg.norm(j))
            #age_vax_df["similarity_score"].loc[i]= sim_score
            age_vax_df.loc[i, "similarity_score"]= sim_score
            #print(i,type(sim_score))
        else:
            #print(type(sim_score))
            type(j)
            #age_vax_df["similarity_score"].loc[i]=None
            age_vax_df.loc[i, "similarity_score"]= None

    #age_vax_df.sort_values(by=['similarity_score'], ascending=False)
    #print(age_vax_df.head())
    #exit()

    #sympt_match_df = pd.merge(age_vax_df, sympt_df, how = 'left', on = 'VAERS_ID')
    sympt_match_df = pd.merge(age_vax_df, sympt_df, how = 'inner', on = 'VAERS_ID')
    sympt_match_df = sympt_match_df[['VAERS_ID','meds_vector','similarity_score','SYMPTOM1','SYMPTOM2','SYMPTOM3','SYMPTOM4','SYMPTOM5']]
    #sympt_match_df = sympt_match_df[sympt_match_df['similarity_score'].notna()]

    #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
    #sympt_match_df = sympt_match_df.sort_values(by=['similarity_score'], ascending=False)
    sympt_match_df.sort_values(by=['similarity_score'], ascending=False, inplace=True)
    sympt_match_df = sympt_match_df.reset_index(drop=True)
    #print(sympt_match_df.head())
    #return []


    pred_symptoms = []
    for i in range(len(sympt_match_df)):
            if len(pred_symptoms) >=5:
                break

            if not (pd.isnull(sympt_match_df.at[i,'SYMPTOM1'])) and (sympt_match_df['SYMPTOM1'][i] not in pred_symptoms):
                symp_perc = sympt_dict[sympt_match_df['SYMPTOM1'][i]]/sum(sympt_dict.values())
                pred_symptoms.append(sympt_match_df['SYMPTOM1'][i]+' ('+str(round(symp_perc*100,4))+'% occurrence)')   
            if len(pred_symptoms) >=5:
                break
            if not (pd.isnull(sympt_match_df.at[i,'SYMPTOM2'])) and sympt_match_df['SYMPTOM2'][i] not in pred_symptoms:
                symp_perc = sympt_dict[sympt_match_df['SYMPTOM2'][i]]/sum(sympt_dict.values())
                pred_symptoms.append(sympt_match_df['SYMPTOM2'][i]+' ('+str(round(symp_perc*100,4))+'% occurrence)')
            if len(pred_symptoms) >=5:
                break
            if not (pd.isnull(sympt_match_df.at[i,'SYMPTOM3'])) and sympt_match_df['SYMPTOM3'][i] not in pred_symptoms:
                symp_perc = sympt_dict[sympt_match_df['SYMPTOM3'][i]]/sum(sympt_dict.values())
                pred_symptoms.append(sympt_match_df['SYMPTOM3'][i]+' ('+str(round(symp_perc*100,4))+'% occurrence)')
            if len(pred_symptoms) >=5:
                break
            if not (pd.isnull(sympt_match_df.at[i,'SYMPTOM4'])) and sympt_match_df['SYMPTOM4'][i] not in pred_symptoms:
                symp_perc = sympt_dict[sympt_match_df['SYMPTOM4'][i]]/sum(sympt_dict.values())
                pred_symptoms.append(sympt_match_df['SYMPTOM4'][i]+' ('+str(round(symp_perc*100,4))+'% occurrence)')
            if len(pred_symptoms) >=5:
                break
            if not (pd.isnull(sympt_match_df.at[i,'SYMPTOM5'])) and sympt_match_df['SYMPTOM5'][i] not in pred_symptoms:
                symp_perc = sympt_dict[sympt_match_df['SYMPTOM5'][i]]/sum(sympt_dict.values())
                pred_symptoms.append(sympt_match_df['SYMPTOM5'][i]+' ('+str(round(symp_perc*100,4))+'% occurrence)')
    sorted_sympts = sorted(pred_symptoms, key = lambda x: round((sympt_dict[x[:(x.index('.')-3)]]/sum(sympt_dict.values()))*100,4), reverse = True)
    return sorted_sympts



def get_sympt_count():
    sympt_dict = {}
    for i in range(len(sympt_df)):
        if not (pd.isnull(sympt_df.at[i,'SYMPTOM1'])):
            if sympt_df['SYMPTOM1'][i] not in sympt_dict:
                sympt_dict[sympt_df['SYMPTOM1'][i]] = 0
            else:
                sympt_dict[sympt_df['SYMPTOM1'][i]] +=1

        if not (pd.isnull(sympt_df.at[i,'SYMPTOM2'])):
            if sympt_df['SYMPTOM2'][i] not in sympt_dict:
                sympt_dict[sympt_df['SYMPTOM2'][i]] = 0
            else:
                sympt_dict[sympt_df['SYMPTOM2'][i]] +=1

        if not (pd.isnull(sympt_df.at[i,'SYMPTOM3'])):
            if sympt_df['SYMPTOM3'][i] not in sympt_dict:
                sympt_dict[sympt_df['SYMPTOM3'][i]] = 0
            else:
                sympt_dict[sympt_df['SYMPTOM3'][i]] +=1

        if not (pd.isnull(sympt_df.at[i,'SYMPTOM4'])):
            if sympt_df['SYMPTOM4'][i] not in sympt_dict:
                sympt_dict[sympt_df['SYMPTOM4'][i]] = 0
            else:
                sympt_dict[sympt_df['SYMPTOM4'][i]] +=1

        if not (pd.isnull(sympt_df.at[i,'SYMPTOM5'])):
            if sympt_df['SYMPTOM5'][i] not in sympt_dict:
                sympt_dict[sympt_df['SYMPTOM5'][i]] = 0
            else:
                sympt_dict[sympt_df['SYMPTOM5'][i]] +=1
    return sympt_dict

# age=30
# user_vector=[0.13973989, 0.23836088, 0.021824023, 0.2290081, 0.29007113, 0.12275258, -2.4536555, 0.3400934, 0.3685603, -0.30112228, 0.3155959, 0.21167116, -0.035278182, -0.15464646, -0.14362535, -0.19436912, -0.058589995, -0.19675334, 0.19468999, -0.26137277, 0.41554782, -0.023785405, 0.009864915, 0.2879687, -0.18352903, -0.022547515, -0.11650363, -0.021304345, 0.10404649, 0.12093672, 0.31221464, -0.13223068, 0.028739564, -0.30094585, 0.33206397, 0.10290256, -0.044768017, -0.035804003, 0.28731117, -0.082659766, -0.2689247, 0.44767395, -0.24672009, 0.022098025, -0.123516224, -0.15329112, 0.025134444, 0.06614014, 0.5362251, -0.1160472, 0.041441668, 0.068297446, -0.16824298, -0.108935244, -0.27976653, -0.042046476, -0.26716185, 0.111297436, 0.44109288, -0.10353676, 0.0190865, -0.17105341, -0.050157826, -0.1379696, 0.07516887, -0.13179071, -0.32399437, -0.060380336, -0.06454936, -0.3308281, -0.08892748, -0.30134425, 0.02589042, 0.2144053, 0.11764423, -0.104768924, 0.35657468, -0.1371022, -0.14129588, 0.1777126, 0.044662368, -0.15583955, 0.0666633, -0.12147122, 0.011226472, 0.002958338, 0.24712567, -0.03867674, 0.11610087, 0.02893556, -0.05480125, -0.032574933, 0.14672667, -0.0029637043, 0.082697056, 0.58953434, -1.7778193, -0.012094222, 0.3214045, 0.49481508, -0.07577906, -0.38043022, -0.17880271, 0.07396254, 0.020331495, -0.26879275, -0.11854651, 0.42328557, -0.06549558, -0.1625061, 0.25846308, 0.15303093, -0.28541526, 0.3221862, -0.32535478, 0.38754645, 0.59328526, 0.16128016, 0.18818152, -0.050084997, -0.009982018, -0.063988976, 0.0859508, -0.09460441, 0.30530345, -0.34752047, -0.19795388, -0.010691927, 0.22289115, -0.14700411, -0.4655455, -0.003747085, -0.14073993, 0.028235393, 0.052675698, -0.060496554, 0.23704171, 0.09421214, -0.23306729, 0.6914032, 0.044204492, 0.2058909, -0.03290375, -0.15303738, 0.15412879, -0.5260331, 0.09093531, -0.07313767, -0.15884048, 0.03720272, 0.20690793, -0.1217907, -0.12104529, -0.14677352, -0.2753177, -0.032919917, -0.0013412926, 0.14156185, 0.061063766, 0.1326497, -0.12474387, 0.06823009, -0.3123549, -0.4669253, -0.016715087, -0.16029945, -0.019250704, -0.050808683, 0.007078932, 0.10829193, 0.025298761, 0.0029326088, -0.096440785, 0.24446838, -0.042746942, 0.2341026, -0.29326814, -0.081687935, 0.072382234, 0.1651329, -0.085524656, 0.17773479, -0.03875992, -0.04588285, -0.18582426, -0.19947813, 0.16655935, 0.21561663, 0.2078891, 0.026576938, 0.13904123, -0.21839005, 0.056482524, 0.23439252, 0.09227845, -0.37006864, 0.11855308, 0.13152003, 0.19659846, -0.46482685, -0.025522238, 0.06650684, -0.11586672, 0.03197428, 0.05517224, -0.07812186, 0.0014836608, -0.12468508, 0.25229743, 0.18799645, 0.21846907, -0.15735865, -0.17049079, -0.08731848, 0.00659355, -0.15837452, -0.09335504, 0.019482022, -0.23304929, -0.15550041, 0.3838118, 0.06870092, 0.08055854, 0.07826076, -3.370643, 0.11981785, -0.19593774, -0.29847506, 0.14825878, 0.024335941, -0.017263336, -0.11070609, -0.08859644, -0.069170155, -0.18627559, -0.107450485, 0.10638401, 0.004957475, -0.21795662, -0.061861873, -0.012760878, 0.15929143, -0.15268089, -0.057644796, 0.007913079, 0.31892693, 0.07604047, 0.029000685, -0.059662268, 0.123322755, 0.11686171, -0.049657594, -0.025987498, 0.036571417, -0.11935442, -0.08542591, 0.02071436, 0.035999313, 0.023059987, 0.2421366, -0.15159406, -0.022166876, 0.15317646, -0.33146033, -0.027017012, 0.05383232, 0.17387962, -0.26545525, 0.13625519, -0.055333078, 0.2846078, -0.11891326, -0.003577811, 0.016855158, -0.062738754, 0.027325833, 0.039367292, 0.25633505, 0.37223792, -0.1146647, 0.045639385, 0.036743544, 0.07395653, 0.24851172, 0.2080753, 0.016608465, -0.07933307, 0.2605201, -0.055695143, -0.046811312, -0.0222397, -0.07160348, -0.14803497, 0.24806501, 0.053246323, -0.04436873, 0.039472345, -0.06902423, 0.47848344, -0.13215016, 43,0,1]


# # # age_grp_df = data.loc[(data['AGE_YRS'] >= age-5) & (data['AGE_YRS'] <= age+5)]

# symptom_set = get_symptoms("COVID19 (COVID19 (PFIZER-BIONTECH))",40,user_vector)

# print(symptom_set)
