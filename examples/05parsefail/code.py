from nbreversible import code
import pandas as pd

df = pd.read_csv("./data.csv")


with code():
    abs(df[["impressions"]] - df[["impressions"]]).describe()
    abs(df[["impressions"]] - df[["impressions"]]).describe()