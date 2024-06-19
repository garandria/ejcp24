#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tues Jan 17 09:08:20 2022

@author: noemie
"""
import numpy as np
import pandas as pd 


import plotly.express as px
import plotly.graph_objects as go

import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual, Layout

#from IPython.display import display
from IPython.core.display import display, HTML
from IPython.display import display as display_
from IPython.display import Image as Image_ipy
from IPython.display import Markdown

import matplotlib.pyplot as plt
from PIL import Image


import scripts.call_api as call_api
import scripts.detect_color_dominance as detect_color_dominance
#####################################################################################################################
########                                          RELEVANCE                                                  ########
#####################################################################################################################

def plot_img_rlv(filename_img_orig, df_rel_nan, option = "plot"):
    """
    [Cette fonction permet de visualiser l image d origine et la relevance]
    Args:
        - filename_img_orig(str)[chemin de l image d origine]
        - df_rel_nan(pandas.DataFrame)[tableau de valeur de relevance]
        - option(str)[choix pour afficher l image d origine avec la relevance:
                        - plot: pour uniquement afficher l image d origine avec la relevance(par defaut)
                        - fig: pour uniquement l image d origine avec la relevance
    Return:
        - fig.show() si option = "plot" ou fig si option = "fig"
        
    """
    # plot relevance
    list_color_rlv = [
                [0.0,"rgb(150, 183, 227)"],
                [0.1, "rgb(69,117,180)"],
                [0.2, "rgb(35, 115, 219)"],
                [0.3, "rgb(6, 86, 191)"],
                [0.4, "rgb(2, 72, 163)"],
                [0.5, "rgb(0, 0, 0)"],
                 [0.6, "rgb(173, 0, 0)"],
                 [0.7,"rgb(224, 2, 2)"],
                 [0.8, "rgb(242, 48, 48)"],
                 [0.9, "rgb(242, 85, 85)"],
                 [1.0, "rgb(245, 137, 137)"]]
    fig = px.imshow(df_rel_nan, color_continuous_scale=list_color_rlv,aspect='auto')#'Bluered'
    
    #load image origine
    im = Image.open(filename_img_orig)

    fig.add_layout_image(
            dict(
                source=im,
                xref="x",
                yref="y",
                x=0,
                y=1,
                sizex=128,
                sizey=128,
                sizing="stretch",
                layer="below")
    )

    fig.update_layout(width=600, height=600, margin=dict(l=30, r=50, b=50, t=50))
    
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(
        font_family="Courier New",
        font_color="blue",
        title_font_family="Times New Roman",
        title_font_color="red",
        legend_title_font_color="green"
    )
    fig.update_layout(
        #title ="Nom de l'image:  "+"test",
        font_family="Arial",
        font_color="black",

    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    if option == "plot":
        return fig.show()
    elif option =="fig":
        return fig

def plot_relevance(url, version, user, password, evalId):
    """
    [Cette fonction permet de visualiser l image d origine et la relevance]
    Args:
        - url(str)[url pour l evaluation]
        - version(str)[version de saimple]
        - user(str)[nom de l utilisateur]
        - password(str)[mot de passe de l utilisateur]
        - evalId(str)[nom de l evaluation]
    Return:
        
        
    """

    api, df_dominance, df_relevance = call_api.get_result_eval(url, version, user, password, evalId)
    json_eval = api.get_evaluations(evalId)
    filename_img_orig = "data/inputs/"+json_eval['inputName']
    df_rlv = df_relevance.copy()
    transparence = widgets.IntSlider(
        value=30,
        min=0,
        max=100,
        step=1,
        description='Threshold:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )
    def plot_rlv_transparence(transparence):
        df_rlv.loc[:,:] = np.where((df_relevance.loc[:,:] < transparence) & (df_relevance.loc[:,:] > -transparence) , np.nan, df_relevance.loc[:,:])
        plot_img_rlv(filename_img_orig,df_rlv, option = "plot")

    widgets.interact(plot_rlv_transparence, transparence=transparence)


#####################################################################################################################
########                                          DOMINANCE                                                  ########
#####################################################################################################################
def plot_dominance(url, version, user, password, evalId):
    """
    [Cette fonction permet de visualiser l image d origine et la dominance]
    Args:
        - url(str)[url pour l evaluation]
        - version(str)[version de saimple]
        - user(str)[nom de l utilisateur]
        - password(str)[mot de passe de l utilisateur]
        - evalId(str)[nom de l evaluation]
    Return:
        
        
    """
    api, df_dominance, df_relevance = call_api.get_result_eval(url, version, user, password, evalId)
    df_dom = df_dominance.copy()
    class_dominante = df_dom[df_dom["status"]=="Dominant"]["id"].values.tolist()[0]
    # todo: generaliser ce type de check
    if len(df_dom) == 5:
        class_csv = "classes_tanks.csv"
        name_class_dom = "tanks"
    elif len(df_dom) == 3:
        if evalId ==  "52e109dc-6284-11ee-b3a4-0242ac140007":
            class_csv = "classes_tanks_.csv"
            name_class_dom = "tanks"
        else:
            class_csv = "classes.csv"
            name_class_dom = "benign"
      
        
    
    list_check_label, df_label = call_api.check_label(class_csv, name_class_dom, class_dominante)
    df_dom_orig = df_dom.copy()
    list_class_orig = []
    for i in df_dom['id']:
        list_class_orig.append(df_label.loc[i, "class_orig"])
    df_dom_orig["class_orig"] = list_class_orig

    detect_color_dominance.detect_color(df_dom_orig, cols = ["min","max"], conf = "99", max_var = None, list_check_label = list_check_label)


############## plot relevance and dominance

    
def plot_result_interact():#type_result
    """
    cette fonction permet d afficher les resultats de saimple (relevance et dominance) de maniere interactive
    """

    url_widget = widgets.Text(value = "https://sales.saimple.com",#"https://team-usecases.lan",
                        placeholder = 'https://localhost:8080',
                        description = "url " ,
                        readout = True,
                        disabled = False,
                        #layout=Layout(height='30px')#width='50%'
                             )

    version_widget = widgets.Dropdown(options=["v2"],
                                     layout=Layout( height='30px'))

    user_widget = widgets.Text(value = "sales",#"templatemvp",#"saimplev2",
                        placeholder = "User name *",
                        description = "User name " ,
                        readout = True,
                        disabled = False,
                        #layout=Layout(width='28%', height='60px')
                              )


    password_widget = widgets.Password(value = "sales",#flag32manitoba",#"templatemvp",#"saimplev2",
                                       description='Password ', 
                                       placeholder='***********',
                                       layout=Layout(height='60px')
                                      )

    ## widget run eval
    ## Evaluation name
    id_eval_widget = widgets.Text(value = "",
                             placeholder = "Evaluation uuid *",
                             description = "Eval uuid" ,
                             readout = True,
                             disabled = False,
                             #layout=Layout(width='70%', height='60px')
                                   )
    #all_eval_wid = widgets.Combobox(
    #                                value=list_all_eval,
    #                                placeholder='Choose eval',
    #                                options=list_class,
    #                                description='Eval uuid:',
    #                                ensure_option=True,
    #                                disabled=False
    #                            )
    def plot_result(url, version, user, password, evalId):
        
        out1 = widgets.Output()
        out2 = widgets.Output()

        tab = widgets.Tab(children = [out1, out2])
        tab.set_title(0, 'Dominance')
        tab.set_title(1, 'Relevance')
        display_(tab)
        
        with out2:
            display_(Markdown('**Relevance**'))
            plot_relevance(url, version, user, password, evalId)
            
        with out1:
            display_(Markdown('**Dominance**'))
            plot_dominance(url, version, user, password, evalId)
            
    my_interact_manual = interact_manual.options(manual_name="🔷 View results 🔷")
    my_interact_manual(plot_result,url=url_widget, version=version_widget, user=user_widget, password=password_widget, evalId=id_eval_widget)


#####################################################################################################################
########                                          DELTA MAX                                                  ########
#####################################################################################################################


def api_plot_delta_max(df_delta_resum, max_var):
    """
    [Cette fonction permet de visualiser les courbes des bornes de dominance pour le delta max]
    Args:
        - df_delta_resum(pandas.DataFrame)[tableau resumant tous les informations des evals du delta max]
        - max_var(int)[maximum de classe a afficher (utile lorsque le nombre de classe est superieurs a 10]
    """
    # ajout des traces plotly
    palette = px.colors.qualitative.Plotly+px.colors.qualitative.Safe+px.colors.qualitative.Prism
    fig = go.Figure()
    nbr_class = int((np.shape(df_delta_resum)[1]-1)/3) 
    classes = [i for i in range(0,nbr_class)]
    for i in range(0, max_var):
        x = df_delta_resum["delta"].tolist()
        y = ((df_delta_resum[str(i)+"/min"]+df_delta_resum[str(i)+"/max"])/2).tolist()

        y_lower = df_delta_resum[str(i)+"/min"].tolist()
        y_upper = df_delta_resum[str(i)+"/max"].tolist()

        t = y_upper[:]
        t.reverse()
        if i < len(palette):
            k = i
            color = palette[k]
        elif i >= len(palette):
            n = i//len(palette)
            k = i - len(palette)*n
            color = palette[k]


        t = t + t
        fig.add_trace(
            go.Scatter(
                name=classes[i],
                x=x+x[::-1], 
                y=y_upper+y_lower[::-1],
                fill='toself',
                mode="lines+markers",
                customdata=t,
                line=dict(color=color),

                text=df_delta_resum[str(i)+"/max"].tolist()[0],

                hovertemplate =                                            
                        '<b>[ %{y:.2E}'+ " ; "+
                        '%{customdata:.2E}'+']</b> ',


                showlegend=True,

        )),


    if max_var < 7:
        hovermode_layout = 'x unified'
    else:
        hovermode_layout = 'x'

    fig.update_layout(
                template="plotly_dark",
                title="<b>Comparaison entre les bornes de dominance<b> ",
                font=dict(family="Lato bold"),
                title_font_family="Lato bold",
                title_font_size=20,
                annotations=[
                    go.layout.Annotation(
                        text="Source: Saimple",
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        x=1.15,
                        y=0,
                        opacity = 0.3)],
                hovermode = 'x unified',
                width=900,
                height=500,
                showlegend=True,
                legend_title="<b>Nom des classes<b>: ",
    )
    fig.show()

def plot_delta_max_interact():#type_result
    """
    [Cette fonction permet de visualiser les resultats de saimple (relevance, dominance 
    et courbe des bornes de dominance) pour l ensemble des evals du delta max
    """

    url_widget = widgets.Text(value = "https://sales.saimple.com",#"https://team-usecases.lan",
                        placeholder = 'https://localhost:8080',
                        description = "url " ,
                        readout = True,
                        disabled = False,
                             )

    version_widget = widgets.Dropdown(options=["v2"],
                                     layout=Layout( height='30px'))

    user_widget = widgets.Text(value = "sales",#"templatemvp",#"sales",
                        placeholder = "User name *",
                        description = "User name " ,
                        readout = True,
                        disabled = False,
                              )

    password_widget = widgets.Password(value = "sales",#"flag32manitoba",#"templatemvp",#"sales",
                                       description='Password ', 
                                       placeholder='***********',
                                       layout=Layout(height='60px')
                                      )

    ## widget run eval
    ## Evaluation name
    tag_eval_widget = widgets.Text(value = "tanks_demo delta max",#"tank_military",
                             placeholder = "Evaluation TAG *",
                             description = "Eval TAG" ,
                             readout = True,
                             disabled = False,
                             #layout=Layout(width='70%', height='60px')
                                   )
    def plot_result(url, version, user, password, TAG):
        
        out1 = widgets.Output()
        out2 = widgets.Output()
        out3 = widgets.Output()

        tab = widgets.Tab(children = [out1, out2, out3])
        tab.set_title(0, 'Dominance')
        tab.set_title(1, 'Relevance')
        tab.set_title(2, 'Espace stable')
        display_(tab)
        api = call_api.get_authent(url, version, user, password)  
        all_eval = api.get_all_eval_v2()
        df_delta_max = call_api.savedeltamax(TAG, all_eval, api, save = False)
        eval_id_delta_max, value_delta_max = call_api.get_eval_id_delta_max(df_delta_max)
        
        with out3:            
            print("valeur du delta max: " +str("{:.5e}".format(np.float64(value_delta_max))))
            call_api.api_get_evals_deltaMax(url, version, user, password, TAG)

        with out2:
            display_(Markdown('**Relevance**'))
            print("valeur du delta max:" +str("{:.5e}".format(np.float64(value_delta_max))))
            plot_relevance(url, version, user, password, eval_id_delta_max)
            
        with out1:
            display_(Markdown('**Dominance**'))
            print("valeur du delta max:" +str("{:.5e}".format(np.float64(value_delta_max))))
            plot_dominance(url, version, user, password, eval_id_delta_max)
            
    my_interact_manual = interact_manual.options(manual_name="🔷 View results 🔷")
    my_interact_manual(plot_result,url=url_widget, version=version_widget, user=user_widget, password=password_widget, TAG=tag_eval_widget)
    
    
    
    

    
