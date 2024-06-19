#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 08:17:57 2021

@author: noemie
"""
# utils
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from emoji import emojize
###########################################################################
###                                UTILS                                ###
###########################################################################
def get_good_df(filename, list_status = ["dominant", "dominated"]):
    """
    [Cette fonction permet de recuperer un dataset sous un format voulu]
    Args:
        - filename(str)[chemin ou se situe le dataset]
        - list_status(list)[list de statu de la classe par defaut = ["dominant", "dominated"]]
    Return:
        - df(pandas.DataFrame)[tableau de valeurs]
    """
    
    df = pd.read_csv(filename)
    
    df.columns = ["min","max"]     
    df["status"] = list_status
    #df["classe"] = df.index
    df = df.reset_index()
    df = df.rename(columns ={"index":"class"}) 
    
    return df


        
###########################################################################
###                        CAS 2 CLASSES                                ###
###########################################################################

def get_color_2class(df, cols = ["min","max"]):
    """
    Cette fonction permet de detecter si le dataset se trouve dans un conflit ou non
    Args:
        - df(pandas.DataFrame)[tableau de valeurs]
        - cols(list)[list des noms de colonne a etudier par defaut=["min","max"]]
    Return:
        - color(str)[couleur]
    
    """
    index_max = df["max"].argmax()  
    index_min = df["min"].argmax()  
    dominan_min, dominan_max = df.loc[index_min,"min"], df.loc[index_max,"max"]
    dominee_min, dominee_max = df.loc[abs(index_min-1),"min"], df.loc[abs(index_max-1),"max"]
   
    if index_min != index_max:
        color = "\U0001F534" #"rouge"   
    elif dominan_min < dominee_max:
        color = "\U0001F534" #"rouge"   
    else:
        dist = dominan_min - dominee_max
        if dist > 0.5:
            color = "\U0001F7E2" #"vert"
        elif 0.1 < dist < 0.5:
            color = "\U0001F7E0" #"orange"
        elif dist < 0.1:
            color = "\U0001F534" #"rouge"   
    return color




###########################################################################
###             CAS NBR DE CLASSE COMPRIS ENTRE 3 ET 30                 ###
###########################################################################

def recup_table(conf = '95'):
    if conf == '90':
        q = [0.941, 0.765, 0.642, 0.56, 0.507, 0.468, 0.437, 
               0.412, 0.392, 0.376, 0.361, 0.349, 0.338, 0.329, 
               0.32, 0.313, 0.306, 0.3, 0.295, 0.29, 0.285, 0.281, 
               0.277, 0.273, 0.269, 0.266, 0.263, 0.26
              ]
    elif conf == '95':
        q = [0.97, 0.829, 0.71, 0.625, 0.568, 0.526, 0.493, 0.466, 
               0.444, 0.426, 0.41, 0.396, 0.384, 0.374, 0.365, 0.356, 
               0.349, 0.342, 0.337, 0.331, 0.326, 0.321, 0.317, 0.312, 
               0.308, 0.305, 0.301, 0.29
              ]
    elif conf == '99':
        q = [0.994, 0.926, 0.821, 0.74, 0.68, 0.634, 0.598, 0.568, 
               0.542, 0.522, 0.503, 0.488, 0.475, 0.463, 0.452, 0.442, 
               0.433, 0.425, 0.418, 0.411, 0.404, 0.399, 0.393, 0.388, 
               0.384, 0.38, 0.376, 0.372
               ]
    return q

def outliers_test(df, cols = ["min","max"], conf = '95' ):
    """
    Cette fonction detecte les valeurs extremes du dataset.
    Args:
        - df: tableau contenant les valeurs a etudie(dataframe pandas) 
        - cols: colonnes a etudie pour detecter les valeurs extremes (list de string)
        - q_dict: table de statistique (dictionnaire)
    Return:
        - outliers: valeurs extremes (list)
    """

    # recuperer table de test Q
    q_dict = recup_table(conf = conf)
    
    # Debut recherche d un outlier(=dominant)
    outliers = []
    col_min, col_max = cols[0], cols[1]
    list_min, list_max = sorted(list(df[col_min])), sorted(list(df[col_max]))
    q_crit = q_dict[len(df)]
    
    # creation de l echantillon
    list_t = []
    for col in cols:
        for i in df[col]:
            list_t.append(i)
    # les valeurs doivent etre trier
    value_list = sorted(list_t)
    df_new = pd.DataFrame()
    df_new["value"] = sorted(list_t)

    
    for i in range(2,len(df_new)):
        
        q_ext = (np.abs(value_list[i] - value_list[i-2]))/(np.abs(max(value_list)-min(value_list))) 
        
        if q_ext >  q_crit:
            #print("  ")
            #print("outlier")
            #print(value_list[i])
            #print("  ")
            outliers.append(value_list[i])
        
        df_outliers = pd.DataFrame(outliers)

    return outliers


def get_color_2_30Classe(df,cols = ["min","max"], conf = "99"):
    """
    [Cette fonction determine la couleur de la dominance a partir de la logique definie 
    au debut du notebook.]
    Args: 
        - df(dataframe pandas)[tableau contenant les valeurs a etudie] 
        - list_outliers(list)[valeurs extremes] 
    Return:
        - color(str)[couleur (vert, orange ou rouge)]
    """

    if len(df) > 2:
        list_outliers = outliers_test(df, cols = cols, conf = conf)
    #print(emojize('- Recherche de outlier: :check_mark_button: ')) 
    dom_max = df[df["status"]=="Dominant"]["max"].tolist()
    dom_min = df[df["status"]=="Dominant"]["min"].tolist()
    if len(list_outliers) > 1:
        if list_outliers[0] == dom_min[0]:
            color = "\U0001F7E2"#"vert"
        elif list_outliers[0] != dom_min[0] and list_outliers[1] == dom_max[0]:
            color = "\U0001F7E0"#"orange"
        else:
            color = "\U0001F534" #"rouge"  

    elif len(list_outliers) == 1:
        if list_outliers[0] == dom_max[0]:
            color = "\U0001F7E0"#"orange"
        else:
            color = "\U0001F534" #rouge 
    elif len(list_outliers) == 0:
        color = "\U0001F534"  #rouge
    return color







###########################################################################
###                 CAS NBR DE CLASSE SUPERIEURE A 30                   ###
###########################################################################

def z_score(data):
    
    mean = np.mean(data)
    std = np.std(data)
    sort_data = np.sort(data)
    Q1 = np.percentile(data, 25, interpolation = 'midpoint') 
    Q2 = np.percentile(data, 50, interpolation = 'midpoint') 
    Q3 = np.percentile(data, 75, interpolation = 'midpoint')   
    IQR = Q3 - Q1 
    up_lim = Q3 + 1.96 * IQR # 1.96 pour 95% de confiance 
    low_lim = Q1 + 1.96 * IQR
    
    
    outlier =[]
    for x in data:
        if ((x> up_lim) or (x<low_lim)):
             outlier.append(x)

    Q1 = np.percentile(data, 25, interpolation = 'midpoint')
    Q2 = np.percentile(data, 50, interpolation = 'midpoint') 
    Q3 = np.percentile(data, 75, interpolation = 'midpoint') 
    
    IQR = Q3 - Q1 

    low_lim = Q1 - 1.96 * IQR
    up_lim = Q3 + 1.96 * IQR
    
    outlier = []
    """
    for i in data:
        z = (i-mean)/std
        if z > mean+1.95*std:
            outlier.append(i)
    print(mean+1.95*std)
 
    """
       
    for x in data:
        if ((x> up_lim) or (x<low_lim)):
             outlier.append(x)
    
    return outlier









###########################################################################
###                            GRAPHIQUE                                ###
###########################################################################



import matplotlib.pyplot as plt
def plot_interval(df, name_status = "status"):
    """
    [Cette fonction permet d afficher les intervalles sous forme de bar
    horizontal]
    Args:
        - df(pandas.DataFrame)[tableau de valeurs]
        - name_status(str)[nom de la colonne contenant les informations 
        sur l etat de la classe par defaut="status"]
    
    """
    fig, ax = plt.subplots(figsize=(15,5))
    for i in range(0,len(df)):
        d = (df.loc[i,["max"]])[0] - (df.loc[i,["min"]])[0]
        if d < 0.09:
            dist = 0.005
        else:
            dist = d
            
        values = ((df.loc[i,["min"]])[0], dist)
        if (df.loc[i,[name_status]])[0] == 'dominated' or (df.loc[i,[name_status]])[0] == 'Dominated':
            facecolors='tab:blue'
        elif (df.loc[i,[name_status]])[0] == 'dominant'or (df.loc[i,[name_status]])[0] == 'Dominant':
            facecolors='tab:green'
        elif (df.loc[i,[name_status]])[0] == 'conflict'or (df.loc[i,[name_status]])[0] == 'Conflict':
            facecolors='orange'
            
        ax.broken_barh([tuple(values)], (i-0.2, 0.4), facecolors=facecolors)
    ax.set_xticks([i*0.1 for i in range(0,11)])
    ax.set_yticks([i for i in range(0,len(df))])
    ax.set_yticklabels([str(l) for l in df["class_orig"]])#
    conflit = mpatches.Patch(color = 'orange', label='conflit')
    dominated = mpatches.Patch(color = 'tab:blue', label='dominated')
    dominan = mpatches.Patch(color = 'tab:green', label='dominant')
    
    plt.legend(handles=[dominan, dominated, conflit],bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.show()
    
###########################################################################
###                            GENERALITE                               ###
###########################################################################


def detect_color(df, cols = ["min","max"], conf = "99", max_var = None, list_check_label = None):
    """
    [Cette fonction permet de recuperer la couleur pour detecter si les intervalles
    se superposent ou non.
    - vert: les intervalles sont tres eloignes
    - orange: les intervalles sont proches mais se chevauchent pas 
    - red 
    """
    #print("\033[1m"+"Detection de conflit"+"\033[0m")
    print("----------------------------")
    nbr_class = len(df)
    print( f"- Nombre de classe: {nbr_class}")
    print("  ")
    if nbr_class == 2:
        color = get_color_2class(df, cols = cols)
    elif 2 < nbr_class < 30:
        color = get_color_2_30Classe(df,cols = cols, conf = conf)
    elif nbr_class > 30:
        color = "\U0001F7E2"#"vert"
    
    #print(f"- Dominance: {color}")
    print("  ")
    if list_check_label != None:
        print(f"- Classe predite: {list_check_label[0]} {list_check_label[1]} ")
        
        
    
    print("  ")
    print("\033[1m"+"Visualisation des intervalles"+"\033[0m")
    print("----------------------------") 
    if max_var == None:
        plot_interval(df)
    else:
        plot_interval(df[:max_var])
        
    
    
    
    
    
    
    
    
    