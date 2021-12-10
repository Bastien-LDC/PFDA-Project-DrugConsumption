from django.shortcuts import render
from django.http import HttpResponse
import joblib
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os 
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import copy

pio.renderers.default = 'browser'


#%% Data preprocessing

demographic_col = [
    'Age', 
    'Gender', 
    'Education', 
    'Country',
    'Ethnicity',
]

relevant_demographic_col = [
    'Age', 
    'Education'
]

personality_col = [
    'Neuroticism',
    'Extraversion',
    'Openness to experience',
    'Agreeableness',
    'Conscientiousness',
    'Impulsiveness',
    'Sensation seeking'
]

drugs_col = [
    'Alcohol consumption',
    'Amphetamines consumption',
    'Amyl nitrite consumption',
    'Benzodiazepine consumption',
    'Caffeine consumption',
    'Cannabis consumption',
    'Chocolate consumption',
    'Cocaine consumption',
    'Crack consumption',
    'Ecstasy consumption',
    'Heroin consumption',
    'Ketamine consumption',
    'Legal highs consumption',
    'Lysergic acid diethylamide consumption',
    'Methadone consumption',
    'Magic mushrooms consumption',
    'Nicotine consumption',
    'Fictitious drug Semeron consumption',
    'Volatile substance abuse consumption'
]

legal_drugs = ['Alcohol consumption',
               'Caffeine consumption',
               'Chocolate consumption',
               'Nicotine consumption']

illegal_drugs = []

for drug in drugs_col:
    if drug not in legal_drugs:
        illegal_drugs.append(drug)

relevant_features = relevant_demographic_col + personality_col
features = demographic_col + personality_col
all_col = features + drugs_col

current_path = os.path.dirname(__file__)
path = os.path.join(current_path, 'drug_consumption.data')


data = pd.read_csv(path, names= all_col)
data = data.reset_index()
data = data.drop('index',axis=1)

Age_info = pd.DataFrame(data=[[-0.95197,"18-24",643,"34.11%"],
                              [-0.07854,"25-34",481,"25.52%"],
                              [0.49788,"35-44",356,"18.89%"],
                              [1.09449,"45-54",294,"15.60%"],
                              [1.82213,"55-64",93,"4.93%"],
                              [2.59171,"65+",18,"0.95%" ]],
                       columns = ["Value", "Meaning", "Cases", "Fraction"])

Gender_info = pd.DataFrame(data=[[0.48246,"Female",942,"49.97%"],
                                 [-0.48246,"Male",943,"50.03%"]],
                           columns = ["Value", "Meaning", "Cases", "Fraction"])

Education_info = pd.DataFrame(data=[[-2.43591,"Left school before 16 years",28,"1.49%"],
                                    [-1.73790,"Left school at 16 years",99,"5.25%"],
                                    [-1.43719,"Left school at 17 years",30,"1.59%"],
                                    [-1.22751,"Left school at 18 years",100,"5.31%"],
                                    [-0.61113,"Some college or university, no certificate or degree",506,"26.84%"],
                                    [-0.05921,"Professional certificate/ diploma",270,"14.32%"],
                                    [0.45468,"University degree",480,"25.46%"],
                                    [1.16365,"Masters degree",283,"15.01%"],
                                    [1.98437,"Doctorate degree",89,"4.72%"]],
                              columns = ["Value", "Meaning", "Cases", "Fraction"])

clean_data = data.copy()
clean_data.isnull().values.any()

def map_conso_score(df):    
    for i in range(0,len(df)):
        for drug in drugs_col:
            if df.loc[i,drug] == "CL0":
                df.loc[i,drug] = 0
            if df.loc[i,drug] == "CL1":
                df.loc[i,drug] = 1
            if df.loc[i,drug] == "CL2":
                df.loc[i,drug] = 2
            if df.loc[i,drug] == "CL3":
                df.loc[i,drug] = 3
            if df.loc[i,drug] == "CL4":
                df.loc[i,drug] = 4
            if df.loc[i,drug] == "CL5":
                df.loc[i,drug] = 5
            if df.loc[i,drug] == "CL6":
                df.loc[i,drug] = 6
                
map_conso_score(clean_data)
clean_data = clean_data[clean_data["Fictitious drug Semeron consumption"]==0]
clean_data.reset_index(drop=True,inplace=True)
clean_data = clean_data.drop("Fictitious drug Semeron consumption",axis=1)

clean_data_numeric = data.copy()
map_conso_score(clean_data_numeric)
clean_data_numeric = clean_data_numeric[clean_data_numeric["Fictitious drug Semeron consumption"]==0]
clean_data_numeric.reset_index(drop=True,inplace=True)
clean_data_numeric = clean_data_numeric.drop("Fictitious drug Semeron consumption",axis=1)

def replace_by_meaning(dataset):
    Age = ["18-24" if age <=-0.9 else
           "25-34" if age <=-0 else
           "35-44" if age <=0.5 else
           "45-54" if age <=1.5 else
           "55-64" if age <=2 else
           "65+"
           for age in dataset["Age"]]
    
    Gender = ["Male" if gender <=-0.4 else "Female" for gender in dataset["Gender"]]
    
    Education = ["Left school before 16 years" if education <=-2 else
                 "Left school at 16 years" if education <=-1.5 else
                 "Left school at 17 years" if education <=-1.4 else
                 "Left school at 18 years" if education <=-1 else
                 "Some college or university, no certificate or degree" if education <=-0.5 else
                 "Professional certificate/ diploma" if education <= 0 else
                 "University degree" if education <= 0.5 else
                 "Masters degree" if education <= 1.5 else
                 "Doctorate degree"
                 for education in dataset["Education"]]
    
    Country = ["USA" if cty <=-0.5 else
               "New Zealand" if cty <=-0.4 else
               "Other" if cty <=-0.2 else
               "Australia" if cty <=0 else
               "Republic of Ireland" if cty <=0.22 else
               "Canada" if cty <=0.25 else
               "UK"
               for cty in dataset["Country"]]
    
    Ethnicity = ["Black" if eth <=-1 else
                 "Asian" if eth <=-0.5 else
                 "White" if eth <=-0.3 else
                 "Mixed-White/Black" if eth <=-0.2 else
                 "Other" if eth <=0.12 else
                 "Mixed-White/Asian" if eth <=0.13 else
                 "Mixed-Black/Asian"
                 for eth in dataset["Ethnicity"]]
    dataset["Age"] = Age
    dataset["Gender"] = Gender
    dataset["Education"] = Education
    dataset["Country"] = Country
    dataset["Ethnicity"] = Ethnicity
    
replace_by_meaning(clean_data)
clean_data[demographic_col].head()
semeron_users = data[data["Fictitious drug Semeron consumption"]!="CL0"].copy()
semeron_users.reset_index(drop=True,inplace=True)
map_conso_score(semeron_users)
replace_by_meaning(semeron_users)

drugs_col = [
    'Alcohol consumption',
    'Amphetamines consumption',
    'Amyl nitrite consumption',
    'Benzodiazepine consumption',
    'Caffeine consumption',
    'Cannabis consumption',
    'Chocolate consumption',
    'Cocaine consumption',
    'Crack consumption',
    'Ecstasy consumption',
    'Heroin consumption',
    'Ketamine consumption',
    'Legal highs consumption',
    'Lysergic acid diethylamide consumption',
    'Methadone consumption',
    'Magic mushrooms consumption',
    'Nicotine consumption',
    'Volatile substance abuse consumption'
]

legal_drugs = ['Alcohol consumption',
               'Caffeine consumption',
               'Chocolate consumption',
               'Nicotine consumption']

illegal_drugs = []

for drug in drugs_col:
    if drug not in legal_drugs:
        illegal_drugs.append(drug)


features = demographic_col + personality_col
all_col = features + drugs_col

colors = px.colors.sequential.YlOrRd

def count_cases(feature,dataset):
    res = {"keys":list(sorted(set(dataset[feature]))),"vals":[0 for i in range(len(set(dataset[feature])))]}
    for i in range(0,len(res["keys"])):
        for element in dataset[feature]:
            if element==res["keys"][i]:
                res["vals"][i]+=1
    return res

def strip_consumption(label_list):
    res = copy.deepcopy(label_list)
    for i in range(len(res)):
        if type(res[i]) == str:
            if "consumption" in res[i]:
                res[i]=res[i][:-12]
    return res

def heatmap(df,category):
    X=df.loc[:,category].astype(float)
    x_list = strip_consumption(category)
    y_list = strip_consumption(list(df.index))
    X=X.to_numpy()
    #X=np.around(X,2)
    fig = ff.create_annotated_heatmap(X, colorscale='Reds',x=x_list, y=y_list,reversescale=False)
    if(len(category)>10):
        fig.update_layout(
        autosize=False,
        width=900,
        height=900
        )
    else:   
        fig.update_layout(
        autosize=False,
        width=700,
        height=700
        )
    return fig


def corr_heatmap(category,df):
    X=df[category].astype(float).corr(method='spearman')
    if any("consumption" in elem for elem in category):
        x_list = list(X.index)
        for i in range(len(x_list)):
            x_list[i] = x_list[i][:-12]
        y_list=x_list
    else:
        x_list = list(X.index)
        y_list = list(X.columns)
    X=X.to_numpy()
    X=np.around(X,2)
    fig = ff.create_annotated_heatmap(X, colorscale='RdBu',x=x_list, y=y_list,reversescale=True)
    if(len(category)>10):
        fig.update_layout(
        autosize=False,
        width=900,
        height=900
        )
    else:   
        fig.update_layout(
        autosize=False,
        width=700,
        height=700
        )
    return fig

def corr_heatmap_2(category1,category2,df):
    all_labels = category1+category2
    X=df[all_labels].astype(float).corr(method='spearman')
    x_list = strip_consumption(list(category2))
    y_list = strip_consumption(list(category1))
    X = X.loc[category1,category2]
    X=X.to_numpy()
    X=np.around(X,2)
    fig = ff.create_annotated_heatmap(X, colorscale='RdBu',x=x_list, y=y_list,reversescale=True)
    if(len(category1)>10 or len(category2)>10):
        fig.update_layout(
        autosize=False,
        width=900,
        height=900
        )
    else:   
        fig.update_layout(
        autosize=False,
        width=700,
        height=700
        )
    return fig

def pieChart(feature,dataset,rotation=0):
    count_values = count_cases(feature,dataset)
    fig = go.Figure(data=[go.Pie(values=count_values["vals"], labels=count_values["keys"],marker_colors=colors,rotation=rotation)])
    fig.update_layout(title_text=f"{feature} of the participants")
    return go.FigureWidget(fig)



#%% Views


def first(request):
    return render(request,'firstpage.html')

def index(request):
    return render(request,'index.html')


def dataviz(request):
    return render(request, 'dataviz.html')


def corrFeatures(request):
    fig=corr_heatmap(relevant_features,clean_data_numeric)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.write_html("templates/corrMatF.html")
    return render(request, 'corrMatF.html')

def corrOutputs(request):
    fig2=corr_heatmap_2(illegal_drugs,relevant_features,clean_data_numeric)
    fig2.update_geos(fitbounds="locations", visible=False)
    fig2.write_html("templates/corrMatO.html")
    return render(request, 'corrMatO.html')

def map1(request):
    list_countries = ["GBR","AUS","CAN","NZL","IRL","USA"]
    count_cases_cty = pd.DataFrame.from_dict(count_cases("Country",clean_data))
    count_cases_cty = count_cases_cty[count_cases_cty["keys"]!='Other']
    count_cases_cty["iso_alpha"] = list_countries

    fig = px.choropleth(count_cases_cty, locations="iso_alpha",
                    color="vals", # lifeExp is a column of gapminder
                    hover_name="keys", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma,
                    projection="natural earth")
    fig.update_geos(fitbounds="locations", visible=True)
    fig.write_html("templates/map1.html")
    return render(request, 'map1.html')

def pie(request):
    fig=pieChart("Age",semeron_users)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.write_html("templates/pie.html")
    return render(request, 'pie.html')


def result(request):
    cls=joblib.load("models/regModel.sav")
    l=[]
    
    l.append({'Age': request.GET['X1'],'Education':request.GET['X2'],
          'Nscore':request.GET['X3'],'Escore':request.GET['X4'],
          'Oscore':request.GET['X5'],'Ascore':request.GET['X6'],
          'Cscore':request.GET['X7'],'Impulsive':request.GET['X8'],
          'SS':request.GET['X9']})

    df=pd.DataFrame(l)
    val=df.iloc[0]
    val=list(val)
    print(val)
    ans=cls.predict(df)
    if ans==1:
        ans="is likely to have used illegal drugs in the last 30 days... Sorry !"
        
    else: 
        ans="has not used illegal drugs in the last 30 days... Good News !"
        
    return render(request,'result.html',{'ans':ans})

