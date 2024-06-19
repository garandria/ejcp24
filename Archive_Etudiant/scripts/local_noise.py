#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tues Jan 27 09:08:20 2022

@author: noemie
"""
import numpy as np
import pandas as pd 

from PIL import Image
import cv2
import plotly.graph_objects as go
import plotly.express as px
    
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual, Layout


import ipywidgets as widgets
from IPython.display import display
def upload_save_img():
    file_upload = widgets.FileUpload(accept='.png', multiple=False)

    display(file_upload)

    def handle_upload(file_upload):
        #print(file_upload)
        uploaded_file = file_upload["new"]
        if uploaded_file != None:
            print(uploaded_file[list(uploaded_file.keys())[0]]['metadata']["name"])
            with open("data/inputs/"+uploaded_file[list(uploaded_file.keys())[0]]['metadata']["name"], 'wb') as f:
                f.write(uploaded_file[list(uploaded_file.keys())[0]]['content'])
            print("File uploaded successfully!")

    file_upload.observe(handle_upload, names='value')



def resize_img(name_img, type_format, new_size=(128,128)):
    
    image1 = Image.open("data/inputs/"+name_img+type_format)

    # Attention : Les images doivent avoir la meme taille et le meme mode !
    image1 = image1.convert("RGB")
    image1 = image1.resize(new_size)
    image1.save("data/inputs/"+name_img+"_resized"+type_format)
    #image1.show()from PIL import Image


def draw_mask_img(name_img):
    """
    [Cette fonction permet de dessiner le mask souhaite]
    Args:
        - name_img(str)[nom de l image]
    """
    filename_img_orig = 'data/inputs/'+name_img
    im = Image.open(filename_img_orig)
    img = np.array(im)
    
    fig = px.imshow(img, color_continuous_scale='gray')

    fig.update_layout(dragmode='drawrect',
                      newshape=dict(line_color='rgb(66,164,229)',
                                    fillcolor='rgb(66,164,229)',
                                    opacity=1))
    fig.update_layout(dragmode='drawopenpath',
                      newshape=dict(line_color='#42A4E5',
                                    fillcolor='#42A4E5',
                                    opacity=1))
    fig.update_layout(dragmode='drawline',
                      # style of new shapes
                      newshape=dict(line_color='turquoise',
                                    fillcolor='turquoise',
                                    opacity=1))


    fig.update_layout(width=400, height=400, margin=dict(l=0, r=0, b=0, t=0),)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.show(config={'modeBarButtonsToAdd':['drawline',
                                            'drawopenpath',
                                            'drawclosedpath',
                                            'drawcircle',
                                            'drawrect',
                                            'eraseshape'
                                           ],
                    'toImageButtonOptions': {
                                            'format': 'png', # one of png, svg, jpeg, webp
                                            'filename': name_img+"_mask",
                                            'height': 128,
                                            'width': 128,
                                            'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
                                            },
                    'displaylogo': False})
    
    

def draw_mask_img_interact():
    """
    [Cette fonction permet de dessiner le masque de maniere interactive]
 
    """
    text_input = widgets.Text(value = "benign_(126)_resized.png",
                         placeholder = "Name input",
                         description = "Name input" ,
                         readout = True,
                         disabled = False,
                         #layout=Layout(width='70%', height='60px')
                         )
    my_interact_manual = interact_manual.options(manual_name="🔷 Load image 🔷")
    my_interact_manual(draw_mask_img,name_img=text_input)    

def get_trans_img(name_img, name_img_mask):
    """
    [Cette fonction permet:
    - d ajouter de la transparence avec le canal alpha en fusionnant l image original et l image avec masque
    - d afficher le resultat de la fusion]
    Args:
        - name_img(str)[nom de l image original]
        - name_img_mask[nom de l image avec le masque]
    
    """
    type_format = ".png"
    
    # load image original 
    image = Image.open("data/inputs/"+name_img)
    img_orig = np.array(image).reshape(128,128,1)
    shape_img_orig = np.shape(img_orig)
    nbr_line, nbr_col = shape_img_orig[0], shape_img_orig[1]
    
    # load image with mask
    img_orig_mask_plotly = cv2.imread("data/inputs/"+name_img_mask)
    shape_img_orig_mask_plotly = np.shape(img_orig_mask_plotly)
    img_orig_mask = img_orig_mask_plotly.copy()
    alpha = np.zeros((nbr_line,nbr_col,1))
    # add canal alpha
    img_orig_rgb = cv2.imread("data/inputs/"+name_img)
    img_orig_with_alpha = np.concatenate((img_orig, alpha), axis=2)
    img_mask_with_alpha = np.concatenate((img_orig_rgb, alpha), axis=2)
    
    # add transparence
    img_orig_with_alpha_c = img_orig_with_alpha.copy()
    img_mask_with_alpha_c = img_mask_with_alpha.copy()
    for i in range(0,nbr_line):
        for j in range(0,nbr_col):
            if int(img_orig_mask[i,j,2])==64 and int(img_orig_mask[i,j,1])==224 or int(img_orig_mask[i,j,0])==208: 
                img_orig_with_alpha_c[i,j,1] = 255
                img_mask_with_alpha_c[i,j,3] = 255

    
    im = Image.fromarray((img_orig_with_alpha_c).astype(np.uint8))
    im.save("data/inputs/"+name_img[:-4]+"_transp.png")
    
    
    ## pour afficher l image il faut soit du rgb ou du rgba
    im_rgba = Image.fromarray((img_mask_with_alpha_c).astype(np.uint8))
    fig = px.imshow(img_mask_with_alpha_c, color_continuous_scale='gray')
    fig.update_layout(width=400, height=400, margin=dict(l=0, r=0, b=0, t=0),)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.show(config={'toImageButtonOptions': {
                                        'format': 'png', # one of png, svg, jpeg, webp
                                        'filename': name_img+"_transp",
                                        'height': 128,
                                        'width': 128,
                                        'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
                                        },
                'displaylogo': False})
    print("Image save:")
    print(name_img[:-4]+"_transp.png")
    #return im
    
    
def get_trans_img_interact():
    """
    [Cette fonction permet d obtenir une image avec de la transparence selon un masque de maniere interactive]
    """
    text_input = widgets.Text(value = "benign_(126)_resized.png",
                         placeholder = "Name input",
                         description = "Input" ,
                         readout = True,
                         disabled = False,
                         #layout=Layout(width='70%', height='60px')
                         )
    text_input_mask = widgets.Text(value = "benign_(126)_resized_mask.png",
                         placeholder = "Name input",
                         description = "mask Input" ,
                         readout = True,
                         disabled = False,
                         #layout=Layout(width='70%', height='60px')
                         )
    my_interact_manual = interact_manual.options(manual_name="🔷 Merge images 🔷")
    my_interact_manual(get_trans_img,name_img=text_input, name_img_mask=text_input_mask)  