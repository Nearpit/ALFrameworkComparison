import numpy as np
from datasets.base import SVMDataset
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder

class Dna(SVMDataset):
    
    dataset_name = "dna"
    feature_encoder =  FunctionTransformer(lambda x: x)
    target_encoder = OneHotEncoder(sparse_output=False)

    urls_dict = {"train":"https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/dna.scale.tr",
                "val":"https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/dna.scale.val",
                "test":"https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/dna.scale.t"}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def split(self, data):
        data["train"]["x"] = np.concatenate((data["train"]["x"], data["val"]["x"].copy()))
        data["train"]["y"] = np.concatenate((data["train"]["y"], data["val"]["y"].copy()))

        data.pop("val", None)
        return data