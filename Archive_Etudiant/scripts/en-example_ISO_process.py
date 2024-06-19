#!/usr/bin/env python
# coding: utf-8

# <div style='color: #369dbf;
#            background-color: #EAF6F6;
#            font-size: 150%;
#            border-radius:50px;
#            text-align:center;
#            font-weight:500;
#            border-style: solid;
#            border-color: #369dbf;
#            font-family: "Cambria";'>   
# <h1 style="font-family: lato; padding: 12px; font-size: 30px; color: #0066A1; text-align: center; line-height: 1.25;">Numalis<br><span style="color: #00ABE0; font-size: 48px"><b>Example ISO process</b></span><br><span style="padding: 12px;color: #00ABE0; font-size: 30px ; text-align: center; line-height: 1.25">   Using Saimple</span></h1>
# <hr>

# The objective of this notebook is to show how Saimple outputs can be used to meet most of the requirements described in ISO/IEC 24029-2.

# <a id='top'></a>
# <div class="list-group" id="list-tab" role="tablist">
#     
# <h1 style="padding: 8px;color:white; display:fill;background-color:#555555; border-radius:5px; font-size:150%"><b> Contents  </b></h1>
# 
#  - [**Librairies**](#1)
# 
#  - [**Launch an evaluation**](#2)
#      
#  - [**Retrieve data from Saimple**](#3)
#     - [**Relevance and stability of behaviour**](#3_1)
#     - [**Delta max**](#3_2)
# 
#  - [**Local Noise**](#4)
#     
#  - [**Clean Workspace**](#5)

# <a id='1'></a>
# <div class="list-group" id="list-tab" role="tablist">
#     
# <h1 style="padding: 8px;color:white; display:fill;background-color:#555555; border-radius:5px; font-size:150%"><b> 
# Required Libraries </b></h1>
# 

# In[1]:


import scripts.call_api as call_api
import scripts.plot_result_api as plot_result_api
import scripts.local_noise as local_noise

import warnings
warnings.filterwarnings("ignore")

get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:





# <a id='2'></a>
# <div class="list-group" id="list-tab" role="tablist">
#     
# <h1 style="padding: 8px;color:white; display:fill;background-color:#555555; border-radius:5px; font-size:150%"><b> 
# Launch an evaluation</b></h1>
# 
# **Expliquer lancement de saimple pour visualiser, les boutons (normali delta surtout...)

# https://saimple.uc.lan/
# templatemvp

# 
#  

# In[2]:


call_api.run_saimple()


# <a id='3'></a>
# <div class="list-group" id="list-tab" role="tablist">
#     
# <h1 style="padding: 8px;color:white; display:fill;background-color:#555555; border-radius:5px; font-size:150%"><b> 
# Retrieve data from Saimple</b></h1>
# 
# <a id='3_1'></a>
# ### Relevance and stability of behaviour
# Feature identification

# In[3]:


plot_result_api.plot_result_interact()


# <a id='3_2'></a>
# ## Delta max

# In[4]:


plot_result_api.plot_delta_max_interact()


# ## Behavior stability against custom noise
# Noise impact on model
# 

# In[5]:


local_noise.draw_mask_img_interact()


# load the mask image in the folder input to create the new image

# In[6]:


local_noise.upload_save_img()


# In[7]:


local_noise.get_trans_img_interact()


# Start an evaluation with the newly created image
# <h1 style="padding: 8px;color:#555555; display:fill;background-color:white; border-radius:5px; font-size:100%"><b>   
# 
#  - [**Launch an evaluation**](#2)
# </b></h1>     
# 

# In[ ]:




