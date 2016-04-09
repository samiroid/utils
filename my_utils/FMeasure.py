import numpy as np

def get_confusionMatrix(pred, gold):
    # Confusion Matrix
    # This assumes the order (neut-sent, pos-sent, neg-sent)
    # mapp     = np.array([ 1, 2, 0])
    conf_mat = np.zeros((3, 3))
    for y, hat_y in zip(gold, pred):        
        conf_mat[y, hat_y] += 1

    return conf_mat

def FmesSemEval(pred, gold, pos_ind, neg_ind):
    # This assumes the order (neut-sent, pos-sent, neg-sent)    
    confusionMatrix = get_confusionMatrix(pred, gold)
    
    # POS-SENT 
    # True positives pos-sent
    tp = confusionMatrix[pos_ind, pos_ind]
    # False postives pos-sent
    fp = confusionMatrix[:, pos_ind].sum() - tp
    # False engatives pos-sent
    fn = confusionMatrix[pos_ind, :].sum() - tp
    # Fmeasure binary
    FmesPosSent = Fmeasure(tp, fp, fn)

    # NEG-SENT 
    # True positives pos-sent
    tp = confusionMatrix[neg_ind, neg_ind]
    # False postives pos-sent
    fp = confusionMatrix[:, neg_ind].sum() - tp
    # False engatives pos-sent
    fn = confusionMatrix[neg_ind, :].sum() - tp
    # Fmeasure binary
    FmesNegSent = Fmeasure(tp, fp, fn)
 
    return (FmesPosSent + FmesNegSent)/2

def Fmeasure(tp, fp, fn):
    # Precision
    if tp+fp:
        precision = tp/(tp+fp)
    else:
        precision = 0 
    # Recall
    if tp+fn:
        recall    = tp/(tp+fn)
    else:
        recall    = 0
    # F-measure
    if precision + recall:
        return 2 * (precision * recall)/(precision + recall)
    else:
        return 0 

