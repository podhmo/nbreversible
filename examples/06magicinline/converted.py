# toplevel before
from nbreversible import (
    code,
)
import pandas as pd
from dictknife import loading
# %matplotlib inline


with code():
    df = pd.DataFrame.from_dict(loading.loadfile("points.json")).set_index("name")
    # nested middle
    df


with code():
    def f(x):
            # nested nested line  ## TODO:support(indent)
        return x * x

    # nested middle
        f(10)  ## TODO:support(indent)


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
