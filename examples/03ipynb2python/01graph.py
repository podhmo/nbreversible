"""


# NumPy and Matplotlib examples


"""


"""


First import NumPy and Matplotlib:


"""


# %matplotlib inline
from nbreversible import (
    code
)



with code():
    import numpy as np



"""


Now we show some very basic examples of how they can be used.


"""






a = np.random.uniform(size=(100,100))



with code():
    a.shape



with code():
    evs = np.linalg.eigvals(a)



with code():
    evs.shape



"""


Here is a cell that has both text and PNG output:


"""




from matplotlib import pyplot as plt
plt.style.use('ggplot')
plt.hist(evs.real)
