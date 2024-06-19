import sys
import warnings
from IPython.display import Image
import pandas as pd
import time
import numpy as np
from PIL import Image
import os
sys.path.append('./scripts/')
import saimple_api as api
import utils as utils
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Authentify on Saimple
VRS = "v2" # Saimple version (currently v2)
URL = "https://app.saimple.com/api" # URL of the API
login = "Enter your login" #? Login
pwd = "Enter your password" #? Password
api = api.SaimpleAPI(URL, VRS, login, pwd)

# Upload the input image, save its ID, and print it
image_path_sign = '50.png' #? Input
image_sign_name  = os.path.basename(image_path_sign)
sign_input_id = api.post_input(image_path_sign)
img = Image.open(image_path_sign)
img

# Upload the model in onnx format and save its id
model_path_sign = 'model1.onnx' #? Model
sign_model_id  = api.post_model(model_path_sign)

# Configurate and launch the evaluation
conf_eval_sign  = {
        "name": "Question 5", #? Name of the evaluation
        "dataType": "Image", # Type of data, can be tabular but in this practical it will remain images
        "input": sign_input_id['inputId'], 
        "reference": 0,
        "model": sign_model_id['modelId'],
        "description": "Evaluation description", #? Description of the evaluation
        "inputDomain": [ # Domain of each variable, in this practical it will remain [0,255]
            "0",
            "255"
        ],
        "noise": {
            "intensity": "0.001", #? Noise intensity
            "mode": "ADDITIVE" #? Type of noise
        },
        "analysisType": "float",
        "channelOrder": "last",
        "normalize":  True,
        "evaluationEngine": "difann"
}
evalId = api.post_evaluations(conf_eval_sign)

# Print the state of the evaluation
while (api.get_eval_status(evalId) == 'IN_PROGRESS'):
    print("\rPlease wait for the end of the evaluation.", end='')
    time.sleep(2)
print('\n')
if (api.get_evaluations(evalId)['status'] == "FAILED"):
    print("Evaluation failed.")
elif (api.get_eval_status(evalId) == "DONE"):

    # If the evaluation succeeded, compute, print and plot the dominance
    dominance = api.get_dominance(evalId)['classes']
    df_dominance = pd.DataFrame(dominance)
    print('Dominance: ',df_dominance)
    utils.histDominance(df_dominance)

    # If the evaluation succeeded, compute and plot the relevance for the class examined_class
    examined_class=0 #? Class for which we want to plot the relevance
    threshold=0.6 #? Threshold value
    alpha=0.05 #? Alpha value
    relevance = api.get_relevance(evalId)['data']
    df_relevance = pd.DataFrame(relevance[examined_class])
    img = np.array(Image.open(os.path.join(image_path_sign)), dtype= float)
    utils.showRelevance(df_relevance, img, threshold, alpha)

