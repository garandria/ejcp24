"""
This module contains usefull tools to manipulate Saimple API v1.
"""


from requests import get, post, delete
import os
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class SaimpleAPI():
    def __init__(self, url, vrs, login="", password=""):
        """
        Class constructor.

        Params
        ------
        url : str
            The URL of the running API.
        vrs : str
            The version of the API used.
        login : str
            The login used to connect to the API.
        password : str
            The password used to connect to the API.
        """

        self._url  = url
        self._vrs  = vrs
        self.headers = {}
        if self._vrs == "v2":
            self.get_token(login, password)

##-----function post-----##
    def post_input(self, img_path):
        """
        Post an image to the API dataset.

        Parameters
        ----------
        img_path : str
            The path to the image.

        Returns
        -------
        boolean
            True if the image was successfully uploaded.
        """

        img = open(img_path, "rb")
        try:
            data_endpoint = "inputs"

            req = post(f"{self._url}/{self._vrs}/{data_endpoint}",
                        files={
                            "filedata": img,
                            "filetype": "Data"
                            },headers=self.headers, verify=False)

            req.raise_for_status()
            #print(f"Successfully uploaded image : {img_path}")
            return req.json()
        except Exception as err:
            raise err

    def post_model(self, model_path):
        """
        Post a model to the API.

        Parameters
        ----------
        model_path : str
            The path to the model.

        Returns
        -------
        boolean
            True if the model was successfully uploaded.
        """

        model = open(model_path, "rb")
        model_name = os.path.basename(model_path)

        try:
            model_endpoint = "models"
            req = post(f"{self._url}/{self._vrs}/{model_endpoint}", 
                        files={"filedata": model},headers=self.headers, verify=False)
            req.raise_for_status()
            #print(f"Successfully uploaded model : {model_name}")
            return req.json()
            #['modelId']
        except Exception as err:
            raise err

    def post_evaluations(self, conf_eval):
        #post_eval(self, conf_eval):
        """
        Post a evaluation to the API.

        Parameters
        ----------
        conf_eval : dict
            The configuration of the evaluation

        Returns
        -------
        JSON
            The id of the evaluation
        """

        try:
            req = post(f"{self._url}/{self._vrs}/evaluations", json=conf_eval ,headers=self.headers, verify=False)
            req.raise_for_status()
            response = json.loads(req.content.decode("utf-8"))
            #return req.json()['evalId']
            return response['evalId']
        except Exception as err:
            raise err

    def get_models_id_meta(self, model_id):
        """
        Get a model of the API by id.

        Parameters
        ----------
        model_id : str
            The path to the model.

        Returns
        -------
        boolean
            True if the model was successfully uploaded.
        """

        try:
            req = post(f"{self._url}/{self._vrs}/models/{model_id}/meta",headers=self.headers, verify=False)
            req.raise_for_status()
            return req
        except Exception as err:
            raise err

# token
    def get_token(self, login, password):
        """
        Get a token for a authentification

        Parameters
        ----------
        login : str
            The login used to connect to the API.
        password : str
            The pass used to connect to the API.

        Returns
        -------
        boolean
            True if the token was successfully uploaded.
        """
        try:
            conf_auth = {
                "login" : f"{login}",
                "password" : f"{password}",
            }
            req = post(f"{self._url}/{self._vrs}/authentification", json=conf_auth, verify=False)
            req.raise_for_status()
            data = json.loads(req.json())
            self.token = data["access_token"]
            self.headers = { 'Authorization': f'Bearer {self.token}'}
            return req
        except Exception as err:
            raise err

##-----function get------##

#evaluation
    def get_evaluations(self, eval_id):
        """
        Get a evaluation of the API.

        Parameters
        ----------
        eval_id : dict
            The id of the evaluation

        Returns
        -------
        dict
            The description of the evaluation
        """

        try:
            req = get(f"{self._url}/{self._vrs}/evaluations/{eval_id}",headers=self.headers,verify=False)
            req.raise_for_status()
            return req.json()
        except Exception as err:
            raise err

    def get_evaluations_trace_by_id(self, id):
        try:
            req = get(f"{self._url}/{self._vrs}/evaluations/{id}/trace",headers=self.headers,verify=False)
            return req.json()
        except Exception as err:
            raise err

    def get_evaluations_dominance_by_id(self, id):
        try:
            req = get(f"{self._url}/{self._vrs}/evaluations/{id}/dominance",verify=False)
            req.raise_for_status()
            response = json.loads(req.content.decode("utf-8"))
            return response
        except Exception as err:
            raise err


    def get_all_eval(self,offset = 0 ):
        """
        Get all evaluations of the API.

        Parameters
        ----------
        offset : the starting index for selecting the evaluations returned


        Returns
        -------
        dict
            The list of all evaluations
        """

        try:
            req = get(f"{self._url}/{self._vrs}/evaluations?offset={offset}",headers=self.headers,verify=False)
            if req.raise_for_status() != None:
                logging.critical(req.json)
                return []
            return req.json()
        except Exception as err:
            logging.exception(err)
            # raise err
            return []

    def get_all_eval_v2(self) : 
        """
            [Retourne toute les évaluations ]
        """
        nb_total = self.get_all_eval()['nbResults']

        All_really = []

        offset = 0
        while offset < nb_total :
            all_now = self.get_all_eval(offset)["evaluations"]
            All_really = [j for i in [All_really, all_now] for j in i] 
            offset += 100

        return All_really

    def get_all_eval_test_(self):
        """
        Get all evaluations of the API.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            The list of all evaluations
        """

        try:
            req = get(f"{self._url}/{self._vrs}/evaluations",headers=self.headers,verify=False)
            print(len(req.json()["evaluations"]))
            for eval in req.json()["evaluations"]:
                if eval["name"] == "Benchmark":
                    print(eval["name"])
                    self.delete_eval(eval["id"])
            req.raise_for_status()
            return req.json()
        except Exception as err:
            raise err

# dominance
    def get_dominance(self, eval_id):
        """
        Get dominance of a evaluation of the API.

        Parameters
        ----------
        eval_id : dict
            The id of the evaluation

        Returns
        -------
        dict
            The dominance of the evaluation
        """

        try:
            req = get(f"{self._url}/{self._vrs}/evaluations/{eval_id}/dominance",headers=self.headers,verify=False)
            req.raise_for_status()
            return req.json()
        except Exception as err:
            #raise err
            return {"classes":[]}

# relevance
    def get_relevance(self, eval_id):
        """
        Get relevance of a evaluation of the API.

        Parameters
        ----------
        eval_id : dict
            The id of the evaluation

        Returns
        -------
        dict
            The relevance of the evaluation
        """
        try:
            req = get(f"{self._url}/{self._vrs}/evaluations/{eval_id}/relevance",headers=self.headers,verify=False)
            req.raise_for_status()
            return req.json()
        except Exception as err:
            raise err

    def get_eval_status(self, eval_id):
        """
        Get status of a evaluation of the API.

        Parameters
        ----------
        eval_id : dict
            The id of the evaluation

        Returns
        -------
        str
            The satuts of the evaluation
        """
        return self.get_evaluations(eval_id)['status']

    def get_versions(self):
        """
        Get version of the API.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            The description of the api
        """
        try:
            req = get(f"{self._url}/{self._vrs}/versions",headers=self.headers,verify=False)
            req.raise_for_status()
            return req.json()
        except Exception as err:
            raise err
    # delta max
    def post_delta_max(self, delta_max_conf):
            #post_eval(self, conf_eval):
            """
            Post a evaluation to the API.

            Parameters
            ----------
            conf_eval : dict
                The configuration of the evaluation

            Returns
            -------
            JSON
                The id of the evaluation
            """


            try:
                req = post(f"{self._url}/{self._vrs}/experiment", json=delta_max_conf ,headers=self.headers, verify=False)
                req.raise_for_status()
                response = json.loads(req.content.decode("utf-8"))
                #return req.json()['evalId']
                print("-")
                print(response)
                return response
            except Exception as err:
                raise err
# delete
    def delete_eval(self, eval_id):
        """
        Delete a evaluation of the API.

        Parameters
        ----------
        eval_id : dict
            The id of the evaluation

        Returns
        -------
        bool
            True if the evaluation was successfully deleted.
        """
        try:
            req = delete(f"{self._url}/{self._vrs}/evaluations/{eval_id}",headers=self.headers,verify=False)
            req.raise_for_status()
            print(f"Successfully delete evaluation : {eval_id}")
            return req
        except Exception as err:
            raise err

    def delete_all_eval(self):
        """
        Delete all evaluation of the API.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True if all evaluations was successfully deleted.
        """
        try:
            req = delete(f"{self._url}/{self._vrs}/evaluations",headers=self.headers)
            req.raise_for_status()
            print(f"Successfully delete all evaluation")
            return req
        except Exception as err:
            raise err

    def delete_all_model(self):
        """
        Delete all model of the API.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True if all evaluations was successfully deleted.
        """
        try:
            req = delete(f"{self._url}/{self._vrs}/models",headers=self.headers)
            req.raise_for_status()
            print(f"Successfully delete all models")
            return req
        except Exception as err:
            raise err

    def delete_all_inputs(self):
        """
        Delete all inputs of the API.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True if all evaluations was successfully deleted.
        """
        try:
            req = delete(f"{self._url}/{self._vrs}/inputs",headers=self.headers)
            req.raise_for_status()
            print(f"Successfully delete all inputs")
            return req
        except Exception as err:
            raise err

    def clear_workplace(self):
        self.delete_all_inputs()
        self.delete_all_model()
        self.delete_all_eval()
