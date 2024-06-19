from this import d
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
from pyparsing import alphas
import copy

#this function normalize the image in value local
def NormalizeImgData(img):
    data = copy.deepcopy(img)
    minData = np.amin(data[0][0])
    maxData = np.amax(data[0][0])
    
    for x in range(0,data.shape[0]):
        for y in range(0,data.shape[1]):
            minData = min(np.amin(data[x][y]), minData)
            maxData = max(np.amax(data[x][y]), maxData)

    M = max(abs(minData), abs(maxData))
    
    for x in range(0,data.shape[0]):
        for y in range(0,data.shape[1]):
            data[x][y] = 0.5 + (data[x][y] / (2 * M))
    
    return data

#this function normalize the image in value local
def NormalizeImgDataInput(img):
    data = copy.deepcopy(img)
    minData = np.amin(data[0][0])
    maxData = np.amax(data[0][0])
    
    for x in range(0,data.shape[0]):
        for y in range(0,data.shape[1]):
            minData = min(np.amin(data[x][y]), minData)
            maxData = max(np.amax(data[x][y]), maxData)

    M = max(abs(minData), abs(maxData))
    
    for x in range(0,data.shape[0]):
        for y in range(0,data.shape[1]):
            data[x][y] = (data[x][y] - minData)/ (maxData - minData)

    return data


#this function convert a dataFrame of relevance to a list format for image exploit
def imgRelevance(data, input, alpha, threshold):
    tab = data.to_numpy()
    tab = NormalizeImgData(tab)
    input = NormalizeImgDataInput(input)
    v1 = []
    for x in range(0,tab.shape[0]):
        v2 = []
        for y in range(0,tab.shape[1]):
            if tab[x][y][0]<0.5 and abs(tab[x][y][0]-0.5)>threshold:
                v2.append([input[x][y]*(1-alpha),input[x][y]*(1-alpha),(tab[x][y][0]*alpha + input[x][y]*(1-alpha))])
            else:
                if tab[x][y][0]>0.5 and abs(tab[x][y][0]-0.5)>threshold:
                    v2.append([(tab[x][y][0]*alpha + input[x][y]*(1-alpha)),input[x][y]*(1-alpha),input[x][y]*(1-alpha)])
                else:
                    v2.append([input[x][y]*(1-alpha),input[x][y]*(1-alpha),input[x][y]*(1-alpha)])
            tab[x][y]  = np.array(tab[x][y])
        v1.append(v2)
    return v1

#this function show the relevance with plt
def showRelevance(data, input, alpha, threshold):
    v1 = imgRelevance(data, input, alpha, threshold)
    plt.imshow(v1,cmap=cm.Blues)
    plt.axis("off")
    plt.title("relevance")
    plt.show()
    
#this function show all relevance with plt
def showAllRelevance(relevance, input, alpha,threshold):
    nb_r = len(relevance)
    fig, axs = plt.subplots(2,int(nb_r/2))
    for i in range(0, int(nb_r/2)):
        image = imgRelevance(pd.DataFrame(relevance[i]), input, alpha,threshold) 
        axs[0, i].imshow(image)
        axs[0, i].axis('off')
        axs[0, i].set_title(str(i), fontstyle='italic')
    for i in range(0, int(nb_r/2)):
        image = imgRelevance(pd.DataFrame(relevance[int(nb_r/2)+i]), input, alpha,threshold) 
        axs[1, i].imshow(image)
        axs[1, i].axis('off')
        axs[1, i].set_title(str(int(nb_r/2) + i), fontstyle='italic')
    plt.show()
    
def histDominance(data):
    nb = len(data)
    delta = 0.01
    fig, ax = plt.subplots()
    for i in range(0, nb):
        if(data["status"][i] == "Dominant"):
            color = 'tab:red'
        else:
            color = 'tab:blue'
        ax.broken_barh([(data["min"][i] - delta , ( data["max"][i] - data["min"][i]) + 2 * delta)],(0.0+ i, 0.9 ), facecolors=color)
        ax.set_xlim(0, 1)
    ax.set_yticks(np.linspace(0.5,nb+0.5 , num=nb, endpoint=False), labels=np.arange(0, nb, 1, dtype=int))
    ax.grid(axis='y')
    plt.show()