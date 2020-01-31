import os
import sys
import json
import numpy as np
import matplotlib.pylab as plt
from scipy.stats import beta


def CStan_input_file(betaD, name):

    alpha = 'alpha <- c('
    beta = 'beta <- c('
    loc = 'loc <- c('
    scale = 'scale <- c('

    for k in betaD.keys():
        alpha += np.str(betaD[k][0]) + ', '
        beta += np.str(betaD[k][1]) + ', '
        loc += np.str(betaD[k][2]) + ', '
        scale += np.str(betaD[k][3]) + ', '

    alpha += ')\n'
    beta += ')\n'
    loc += ')\n'
    scale += ')\n'

    textf = open(name+'_StanSNR.txt', 'w')
    textf.write(alpha)
    textf.write(beta)
    textf.write(loc)
    textf.write(scale)
    textf.close()

    return

def pyStan_input_file(betaD, name, binNo, pBins):
    cwd = os.getcwd()
    alpha = np.zeros(len(betaD))
    beta = np.zeros(len(betaD))
    loc = np.zeros(len(betaD))
    scale = np.zeros(len(betaD))

    for i,k in enumerate(betaD.keys()):
        alpha[i], beta[i], loc[i], scale[i] = betaD[k]

    np.savez(cwd+'/Bins/'+pBins+'/'+name+'_pyStanSNR'+pBins+np.str(binNo)+'.npz', 
        a=alpha, b=beta, loc=loc, scale=scale, N=len(betaD))

    return


def read_bin_beta(name, binNo, pBins):
    cwd = os.getcwd()
    data = open(cwd+'/Bins/'+pBins+'/'+name+'_beta'+pBins+np.str(binNo)+'.json')
    pd = json.load(data)

    return pd



if __name__ == "__main__":

    #rbetaPX = open('pxnorm_betaSNR.json')
    #rbetaRB = open('rdblurnorm_betaSNR.json')

    pBins = sys.argv[1]

    for i in range(1,7):
        betaPX = read_bin_beta('pxnorm', i, pBins) #json.load(rbetaPX)
        betaRB = read_bin_beta('rdblurnorm', i, pBins)   #json.load(rbetaRB)
    
        pyStan_input_file(betaPX, 'pxnorm', i, pBins)
        pyStan_input_file(betaRB, 'rdblurnorm', i, pBins)


