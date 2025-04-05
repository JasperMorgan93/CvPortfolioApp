import pandas as pd

class DataframeUtilies:
    def __init__(self):
        pass

    def convert_data_to_pandas_df(self, data_dict:dict={}) -> pd.DataFrame:
        return pd.DataFrame(data_dict)