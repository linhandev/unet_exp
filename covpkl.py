import sys
import os
import os.path as osp
import pickle
import json

import numpy as np


if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = "/home/lin/Desktop/data/nnunet/"
print(path)


class NumpyEncoder(json.JSONEncoder):
    """Special json encoder for numpy types"""

    def default(self, obj):
        if isinstance(
            obj,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        return json.JSONEncoder.default(self, obj)


for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".pkl"):
            print("converting file: ", file)
            with open(osp.join(root, file), "rb") as f:
                data = pickle.load(f)
            # print(type(data))
            # print(json.dumps(data, cls=NumpyEncoder))
            with open(osp.join(root, file + ".json"), "w") as f:
                print(json.dumps(data, cls=NumpyEncoder, indent=4), file=f)
