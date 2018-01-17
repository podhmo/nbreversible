# toplevel before
from nbreversible import (
    code,
)
import json
import pandas as pd
# %matplotlib inline

with code():
    # nested before  ##TODO:support
    with open("points.json") as rf:
        # nested nested before  ##TODO:support
        df = pd.DataFrame.from_dict(json.load(rf)).set_index("name")
        # nested nested after  ##TODO:support
    # nested middle
    df

with code():
    # nested before  ## TODO:support
    def f(x):
        # nested nested line  ## TODO:support(indent)
        return x * x

    # nested middle
    f(10)  ## TODO:support(indent)
    # nested after  ## TODO:support

with code():
    ax = df.plot(kind="scatter", x="x", y="y", s=40)
    for _, row in df.iterrows():
        ax.annotate(
            row.name,
            (row.x, row.y),  ## TODO:support(indent)
            color="k",
            weight="semibold",
            size="medium",
            horizontalalignment="left",
            verticalalignment="top"
        )
# toplevel after
