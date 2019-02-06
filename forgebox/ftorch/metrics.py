import torch

def argmax(x):
    """
    Arg max of a torch tensor (2 dimensional, dim=1)
    :param x:  torch tensor
    :return: index the of the max
    """
    return torch.max(x, dim=1)[1]

def metric4(y_pred,y_true,bm = 0.5):
    """
    4 metrics for binary classification situations
    :param y_pred:
    :param y_true:
    :param bm: benchmark, default 0.5
    :return: acc,rec,prec,f1_score
    """
    acc = accuracy(y_pred,y_true)
    rec = recall(y_pred,y_true,bm)
    prec = precision(y_pred,y_true,bm)
    f1_ = f1(rec,prec)
    return acc,rec,prec,f1_

def accuracy(y_pred, y_true):
    """
    :param y_pred: predition of y (will be argmaxed)
    :param y_true: true label of y (index)
    :return:
    """
    return (argmax(y_pred) == y_true).float().mean()

def recall(y_pred,y_true,bm = 0.5):
    is_right = (((y_pred > bm)*1).long()==y_true)
    is_right_in_targ = is_right[y_true==1]
    if len(is_right_in_targ) == 0:
        is_right_in_targ = torch.zeros(1)
    return is_right_in_targ.float().mean()

def precision(y_pred,y_true, bm = 0.5):
    is_right = (((y_pred > bm)*1).long()==y_true)
    is_right_in_pred = is_right[(y_pred > bm)]
    if len(is_right_in_pred) == 0:
        is_right_in_pred = torch.zeros(1)
    return is_right_in_pred.float().mean()

def f1(recall,precision):
    """
    stantard f1 for binary classification
    recall:
    precision:
    """
    return 2*precision*recall/(precision + recall)