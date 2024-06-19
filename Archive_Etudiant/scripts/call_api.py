#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tues dec 15 09:08:20 2022

@author: noemie
"""

import scripts.saimple_api as api_
import scripts.plot_result_api as plot_result_api

import numpy as np
import pandas as pd
from io import StringIO
import sys
import os
import time
import emoji

import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual, Layout
from IPython.display import display as display_
#pd.plotting.register_matplotlib_converters()
from IPython.core.display import display, HTML
import matplotlib.pyplot as plt
from PIL import Image
from IPython.display import Image as Image_ipy
from IPython.display import Markdown

import plotly.express as px
from PIL import Image

#######################################################################################################
####                                    RUN EVALUATION                                             ####
#######################################################################################################

def get_authent(url, version, user, password):
    """
    [Cette fonction permet de s authentifier]
    Args:
        - url(str)[url pour l evaluation]
        - version(str)[version de saimple]
        - user(str)[nom de l utilisateur]
        - password(str)[mot de passe de l utilisateur]
    Return:
        - api()[api saimple]
    """
    #print((str(url)+'/api', version, str(user), str(password)))
    api = api_.SaimpleAPI(str(url)+'/api', version, str(user), str(password))  
    # recuperer les informations de configuration de l'API en consultant la ressource versions à l'aide de :
    #info_version = api.get_versions()
    #df_info_version = pd.DataFrame(info_version)
    #df_info_version
    return api  

def run_eval(api, name_eval, description, input_path, input_type, model_path, normalize, precision_type, intensity, mode, delta_max):
    """
    [Cette fonction permet de lancer une evaluation sur saimple]
    Args:
        - api
        - name_eval
        - description
        - input_path
        - input_type
        - model_path
        - normalize
        - precision_type
        - intensity
        - mode
        - delta_max
    Return:
        - evalId(str)[uuid de l evaluation]
    """

    
    # preprocessing
    input_path_b = input_path#os.path.join(resources, input_path)
    input_name  = os.path.basename(input_path_b)
    print(emoji.emojize(' Upload input '+input_name+ ': :check_mark_button: '))
    image1 = Image_ipy(input_path_b)
   
    display(image1)
    input_id = api.post_input(input_path_b)  
    model_path_b = model_path#os.path.join(resources, model_path)
    model_name  = os.path.basename(model_path_b)
    # Post models & save IDs models
    model_id  = api.post_model(model_path_b)
    print(emoji.emojize(' Upload model '+model_name+': :check_mark_button: '))
    
    # determiner input Domain   
    if normalize == "True":
        input_domain = ["0","1"]
    elif normalize == "False":
        input_domain = ["0","255"]
    #if model_type == "svm":
    #    "evaluationEngine": "svm" 
        
    conf_eval  = {
        "name": name_eval,
        "dataType": input_type,
        "input": input_id['inputId'],
        #"reference": 0,
        "model": model_id['modelId'],
        "description": description,
        "inputDomain": input_domain,
        
        "noise": {
            "intensity": str(intensity),
            "mode": mode
        },
        "analysisType": precision_type[0].lower() + precision_type[1:],
        "channelOrder": "last", # a supprimer plus tard
        "normalize":  normalize,
        "evaluationEngine": "difann" 
    }

    if delta_max == True or delta_max == str(True):
        conf_eval["algo"] = "brent"
        conf_eval["name"] = name_eval+" delta max"
        evalId = api.post_delta_max(conf_eval)
        time_approx = 25
    elif delta_max == False or delta_max == str(False):
        evalId = api.post_evaluations(conf_eval)
        time_approx = 10
    #show_eval_status(api, evalId)
    
    #barre de chargement
  
    my_pb = widgets.IntProgress(
                        value=0,
                        min=0,
                        max=time_approx,
                        description='Loading:',
                        bar_style= 'success', # 'success', 'info', 'warning', 'danger' or ''
                        style={'bar_color': '#61C6E4'},
                        orientation='horizontal')

    display(my_pb)
    

    for i in range(time_approx):

        time.sleep(1)
        my_pb.value = i + 2
        if i<3 :
            my_pb.style.bar_color = '#BADBF1'
        elif i>3 and i<10:
            my_pb.style.bar_color = '#42A4E5'
        elif i>10:
            my_pb.style.bar_color = '#0868A9'
        
    
    # Waiting for the end of the evaluation
    while (api.get_eval_status(evalId) == 'IN_PROGRESS'):
        #print("\rPlease wait the end of the evaluation.", end='')
        time.sleep(2)
    #print('\n')

    if (api.get_eval_status(evalId) == "DONE"):
        my_pb.close()

        display(Markdown('***Evaluation finished !***'))
        #print("Evaluation uuid: ", evalId)
        print("                 ---              ")
        if delta_max == True or delta_max == str(True):
            display(Markdown('**Evaluation search delta max TAG:**'))
            print(conf_eval["name"])

        elif delta_max == False or delta_max == str(False):
            display(Markdown('**Evaluation uuid:**'))
            print(evalId)
    
    return evalId

def content_parser(up_value):
    if up_value == {}:
        with out:
            print('No image loaded')    
    else:
        typ, content = "", ""
        for i in up_value.keys():
            typ = up_value[i]["metadata"]["type"]
            if typ == "image/png":
                content = "data/inputs/"+i#up_value[i]["content"]
                #print(up_value)
                #keys_model = [*up_value.value]
                
                #model_path_ = keys_model[0]
                #print("content parser",content)
                #content_str = str(content, 'utf-8')
                print(content)
                return content
            else:
                content = "data/models/"+i
                print(content)
                return content
                


def process_run_saimple(url, version, user, password, name_eval,description, input_path, model_path, input_type, normalize, precision_type,intensity, mode, delta_max):
    """
    [Cette fonction permet de s authentifier et de creer un json pour pouvoir lancer une evaluation sur saimple]
    Args:
        - api
        - name_eval
        - description
        - input_path
        - input_type
        - model_path
        - normalize
        - precision_type
        - intensity
        - mode
        - delta_max
    Return:
        - evalId(str)[uuid de l evaluation]
    """

    print("        ")
    print("------------------------------------------------")
    print("        ")
    print("\033[1m"+"Authentification"+"\033[0m")
    api = get_authent(url, version, user, password)
    print(emoji.emojize(' Done :check_mark_button: '))
    
    print("  ")
    print("\033[1m"+"Lancement de l'évaluation"+"\033[0m")

    input_path_ = os.path.join("data/inputs/",input_path)

    model_path_ = os.path.join("data/models/",model_path)
    
    evalId = run_eval(api, 
                      name_eval, 
                      description, 
                      input_path_, 
                      input_type, 
                      model_path_, 
                      normalize, 
                      precision_type, 
                      intensity, 
                      mode,
                     delta_max)
    print("  ")
    print("\033[1m"+"Résultat de l'évaluation"+"\033[0m")
    print(" view Saimple:", url)
    #return api
    
    
    
def run_saimple():
    """
    [Cette fonction permet de lancer une evaluation de maniere interactive]
    """
    ## widget authentification
    widgets.Layout(
        border='solid 1px black',
        margin='0px 10px 10px 0px',
        padding='5px 5px 5px 5px')

    url_widget = widgets.Text(value = "https://sales.saimple.com",#"https://team-usecases.lan",
                        placeholder = 'https://localhost:8080',
                        description = "url " ,
                        readout = True,
                        disabled = False,
                        #layout=Layout(height='30px')#width='50%'
                             )

    version_widget = widgets.Dropdown(options=["v2"],
                                     layout=Layout( height='30px'))

    user_widget = widgets.Text(value = "sales",#"saimplev2",#"templatemvp",#"sales",
                        placeholder = "User name *",
                        description = "User name " ,
                        readout = True,
                        disabled = False,
                        #layout=Layout(width='28%', height='60px')
                              )


    password_widget = widgets.Password(value = "sales",#"flag32manitoba",#"templatemvp",#"sales",
                                       description='Password ', 
                                       placeholder='***********',
                                       layout=Layout(height='60px'))

    ## widget run eval
    ## Evaluation name
    name_eval_widget = widgets.Text(value = "default name",
                             placeholder = "Evaluation name *",
                             description = "Eval name" ,
                             readout = True,
                             disabled = False,
                             #layout=Layout(width='70%', height='60px')
                                   )


    ## Description (optional)
    descript_eval_widget = widgets.Textarea(value = "",
                                     placeholder = "Description (Optional)",
                                     description = "descript eval" ,
                                     readout = True,
                                     disabled = False,
                                     layout=Layout(width='70%', height='80px')       )

    ## File upload
    upload_input = widgets.FileUpload(description='Upload Image',
                                      accept="", 
                                      multiple=False, 
                                      button_style='primary', 
                                      #icon='image'
                                     )
    text_input = widgets.Text(value = "benign_(126)_resized.png",
                             placeholder = "Name input",
                             description = "Name input" ,
                             readout = True,
                             disabled = False,
                             #layout=Layout(width='70%', height='60px')
                             )
    input_type_widget = widgets.Dropdown(options=['Image'],
                                description='Input type:',)

    upload_model = widgets.FileUpload(description='Upload Model',
                                      accept="", 
                                      multiple=False, 
                                      button_style='info')
                                       
    text_model = widgets.Text(value = "model_breast_cancer_cnn1.onnx",
                             placeholder = "Name model",
                             description = "Name model" ,
                             readout = True,
                             disabled = False,
                             layout=Layout(width='70%', height='60px'))

    upload_file = widgets.HBox([upload_input, upload_model])


    normalize_value_widget = widgets.ToggleButtons(options=[('Yes','True'), ('No','False')],
                                            description='Normalize:',
                                            disabled=False,
                                            button_style='', # 'success', 'info', 'warning', 'danger' or ''
                                            tooltips=['Description of normalize', 'Description of ', 'Description of '],
                                            layout=Layout(width='100%',height='100px')
                                        #     icons=['check'] * 3
                                        )
    delta_max_value_widget = widgets.ToggleButtons(options=[('No','False'),('Yes','True')],
                                            description='Delta max:',
                                            disabled=False,
                                            button_style='', # 'success', 'info', 'warning', 'danger' or ''
                                            tooltips=['Description of delta max', 'Description of ', 'Description of '],
                                            layout=Layout(width='100%',height='100px')
                                        #     icons=['check'] * 3
                                        )
    ## Precision
    precision_widget = widgets.Dropdown(options=['Double', 'Float', 'Float 128'],
                                description='Precision:',)

    ## Noise type
    noise_type_widget = widgets.Dropdown(options=["ADDITIVE", "MULTIPLICATIVE", "BOKEH", "GAUSSIAN"],
                                 description='Noise type:',
                                 )


    ## Noise intensity
    intensity_noise_widget = widgets.BoundedFloatText(value=0.00001,
                                                      min=0,
                                                      #max=1.0,
                                                      step=0.00001,
                                                      description='Intensity:',
                                                      readout=True,
                                                      readout_format='.5f',
                                                      disabled=False
                                                    )
    my_interact_manual = interact_manual.options(manual_name="🔷 Run saimple 🔷")

    my_interact_manual(process_run_saimple, url = url_widget, version = version_widget, user = user_widget, password = password_widget, name_eval = name_eval_widget, description =  descript_eval_widget, input_path = text_input, model_path = text_model, input_type = input_type_widget, normalize = normalize_value_widget, precision_type = precision_widget,intensity = intensity_noise_widget, mode = noise_type_widget, delta_max = delta_max_value_widget)

    
    
#######################################################################################################"
####                                    RECUPERATION DES RESULTATS
#######################################################################################################"  



def get_result_eval(url, version, user, password, evalId):
    api = get_authent(url, version, user, password)
    dominance = api.get_dominance(evalId)['classes']
    df_dominance = pd.DataFrame(dominance)
    
    relevance = api.get_relevance(evalId)['data']
    df_relevance = pd.DataFrame(np.transpose(np.transpose(relevance[0])[0]))
    return api, df_dominance, df_relevance

############### RELEVANCE #######################





############### DOMINANCE #######################
def check_label(filename_class, name_class, class_dominante, print_option = None):
    """
    [Cette fonction permet de verifier si le modele a classe correctement]
    Args:
        - filename_class(str)[chemin du csv contenant le nom des labels]
        - name_class(str)[nom de la classe predite]
        - class_dominante(str)[classe dominante]
        - print_option()[option pour afficher les resultats de la classification par defaut = None]
    Return:
        - [name_class_pred, color](list)[liste de deux elements: name_class_pred 
        - df_label
    """
    df_label = pd.read_csv(filename_class, header = None)
    df_label.columns = ["class_out", "class_orig"]
    df_label['class_orig'] = [classe for classe in df_label["class_orig"]]
    name_class_pred = df_label.loc[class_dominante,"class_orig"]

    if name_class.strip() == name_class_pred.strip():
        color = "\U0001F7E2"#"vert"
        #print(f"- Classe predite: {name_class_pred} {color} ")
    else:
        color = "\U0001F534" #"rouge"
        if print_option != None:
            print(f"- Classe predite: {name_class_pred} {color} (Classe origine: {name_class})")
    return [name_class_pred, color], df_label  




############### DELTA MAX #######################


def savedeltamax(TAG, all_eval, api, save = True) : 
    """
        [   - Retourne le dataframe de la liste des deltamax avec le <TAG>, sous le nom de path <file_path>
        - Génère un  .csv de la liste des deltamax si save=True    ] 

    Args : 
        - TAG(str)[Tags qui se trouve dans le nom des évaluations qu'on recherche]
        - all_eval(list)[Lisre de toute les évaluations ]
        - file_path(str)[chemin du fichier csv qui va être générer]
        - api()
    Returns : 
        - df(Dataframe)[dataframe de la liste des deltamax avec le <TAG>]
        
    """

    #filtred_eval = list(filter(lambda x : ((TAG in x["name"]) & ("delta max" in x["name"])) , all_eval))
    filtred_eval = list(filter(lambda x : ((TAG in x["name"])) , all_eval))
    #print(filtred_eval)
    # # for eval in filtred_eval : 
    # #     l = [eval['id'],eval["name"], eval["inputName"],float(eval['noise']['intensity']), eval["modelName"]]

    rows = []
    for i in range(len(filtred_eval)): 
        eval = filtred_eval[i]

        dominance = api.get_dominance(eval['id'])["classes"]
        for j in range(0,len(dominance)):
            #dom = list(filter(lambda x : (("Dominant" or "Conflict" in x["status"])) , dominance))
            dom = dominance[j]
            classe_dominante = dom["id"]
            mind = dom["min"]
            maxd = dom["max"]
            status = dom["status"]


            l = [eval['id'],eval["name"], eval["inputName"],float(eval['noise']['intensity']), eval["modelName"], classe_dominante, mind, maxd, status]
            rows.append(l)

    df = pd.DataFrame(rows, columns= ["eval_id","eval_name","inputName","deltamax", "modelName", "dominantClass", "min_dominance", "max_dominance", "status"])

    if save : 
        # save_dir = os.path.join("data/deltamax/", filename)
        file_path = "df_"+TAG.replace(" ","_")+".csv"
        df.to_csv(file_path,index = False)
    return df


def api_preprocessing_delta_max(df_delta_max):
    """
    """
    list_delta_sc = []
    list_delta = df_delta_max["deltamax"].value_counts().index.tolist()
    list_delta.sort()
    for k in range(0,len(list_delta)):
        delta = "{:.4e}".format(np.float64(list_delta[k]))
        list_delta_sc.append(delta)
        
        df_delta = df_delta_max[df_delta_max["deltamax"]==list_delta[k]]
        max_var = len(df_delta)

        df_delta_sort = df_delta.sort_values(by="min_dominance", ascending=False)
        df_delta_sort.index = [j for j in range(0,len(df_delta_sort))]

        list_max_delta = df_delta_sort.loc[:max_var-1,"max_dominance"].tolist()
        list_min = df_delta_sort["min_dominance"].tolist()
        list_max = df_delta_sort["max_dominance"].tolist()
        list_status = df_delta_sort["status"].tolist()

        df_delta_resum_b = pd.DataFrame()

        for i in range(0,len(df_delta)):
            name_cols = [str(i)+"/min", str(i)+"/max", str(i)+"/status"]
            df_delta_resum_b[name_cols[0]] = [list_min[i]]
            df_delta_resum_b[name_cols[1]] = [list_max[i]]
            df_delta_resum_b[name_cols[2]] = [list_status[i]]

        if k != 0:
            df_delta_resum = pd.concat([df_delta_resum,df_delta_resum_b])
        else:
            df_delta_resum = df_delta_resum_b
    df_delta_resum["delta"] = list_delta_sc
    df_delta_resum.index = [i for i in range(0,len(df_delta_resum))]
    
    return df_delta_resum

def api_get_evals_deltaMax(url, version, user, password, TAG):
    
    api = get_authent(url, version, user, password)  
    all_eval = api.get_all_eval_v2()
    df_delta_max = savedeltamax(TAG, all_eval, api, save = True)
    nbr_class = len(df_delta_max["dominantClass"].value_counts().index.tolist())
    df_delta_resum = api_preprocessing_delta_max(df_delta_max)
    if nbr_class > 10:
        max_var = 10
    else:
        max_var = nbr_class
    plot_result_api.api_plot_delta_max(df_delta_resum, max_var=max_var)

def get_eval_id_delta_max(df_delta_max):
    list_name_eval = df_delta_max["eval_name"].value_counts().index.tolist()
    for i in range(0,len(list_name_eval)):
        if "(delta max)" in list_name_eval[i]:
            line_delta_max = df_delta_max[df_delta_max["eval_name"]==list_name_eval[i]].reset_index()
            eval_id_delta_max = line_delta_max.loc[0,"eval_id"]
            value_delta_max = line_delta_max.loc[0,"deltamax"]
            
    return eval_id_delta_max, value_delta_max
    
  
    


    


