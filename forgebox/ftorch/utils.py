from .train import JUPYTER
if JUPYTER: from IPython.display import display

def mars(printstuff):
    """
    A print function works between jupyter and console print
    :param printstuff:
    """
    if JUPYTER:display(printstuff)
    else:print(printstuff)