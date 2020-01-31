import sys
import os
import json
import numpy as np
import matplotlib.pylab as plt
from scipy.stats import beta

def normalize(data):
    """
    Normalize a set [min(data[k]), max(data[k])] to [0,1]
    data is a dictionary with key k.
    """
    norm_data = {}
    for k in data.keys():
        norm_data[k] = (np.array(data[k])-min(data[k]))/(max(data[k])-min(data[k]))  
    return norm_data


def fit_beta(norm_data, name, binNo, pBin):
    """
    Fit beta distribution to a set of data normalized betw 0 and 1.
    norm_data is a dictionary.
    Returns a dictionary of alpha and beta saved in json
    """
    beta_dist = {}
    for k in norm_data.keys():
        beta_dist[k] = list(beta.fit(norm_data[k]))#[:2]
    cwd = os.getcwd()
    with open(cwd+'/Bins/'+pBin+'/'+name+'_beta'+pBin+np.str(binNo)+'.json', 'w') as f:
        json.dump(beta_dist, f)

    return beta_dist

def plot_realbeta_distr(realPX, realRB, betaPX, betaRB, name):
    """
    Plots the real posterior distribution together 
    with the beta distribution fitted to it
    """
    survey = name.split('-')[0]
    Id = name.split('-')[1]
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=False, figsize = (14, 6))
    ax1.hist(realPX, alpha = 0.6, color = 'dodgerblue', label='Narrow reflection')
    ax1.hist(realRB, alpha = 0.6, color = 'orangered', label='Broad reflection')

    x = np.linspace(0, 1, 1000)
    distPX = beta(betaPX[0], betaPX[1])
    distRB = beta(betaRB[0], betaRB[1])
    ax2.plot(x, distPX.pdf(x), alpha = 0.6, color = 'dodgerblue', 
        label='Narrow reflection, beta')
    ax2.plot(x, distRB.pdf(x), alpha = 0.6, color = 'orangered',
        label='Broad reflection, beta')

    ax1.set_xlabel('Normaized R value', fontsize=18)
    ax2.set_xlabel('X', fontsize=18)

    ax1.set_ylabel('Posterior distribution', fontsize=18)
    ax2.set_ylabel('Beta distribution', fontsize=18)
    ax1.tick_params(labelsize=16)
    ax2.tick_params(labelsize=16)

    legend = plt.legend(loc='best', scatterpoints=1, numpoints=1, prop={'size':'16'})
    legend.set_frame_on(False)
    cwd = os.getcwd()
    plt.savefig(cwd+'/fit_beta/'+survey+'/'+name+'_nonorm.png')
    plt.close()

def bin_sample(binNo, pBin, data, name):
    """
    Creates a .json file with the posterior distr of the objects
    in the subsample in the bin number binNo for the data binned 
    by pBin. The sources in that bin are described in the header file.
    - binNo in [1, 2, 3, 4, 5, 6], int
    - pBin in ['L', 'NH', 'NHH', 'NHL', 'z', 'zH', 'zL']
    Saves the .json file in the 
    """
    cwd = os.getcwd()
    bin_header = np.load(cwd+'/Headers/header_'+pBin+np.str(binNo)+'.npz')
    inBin = {}
    for k in data.keys():
        if k in bin_header['header']:
            inBin[k] = data[k]

    with open(cwd+'/Bins/'+pBin+'/'+name+'_bin'+pBin+np.str(binNo)+'.json', 'w') as f:
        json.dump(inBin, f)

    return inBin

def read_bin_sample(name, binNo, pBins):
    """

    """
    cwd = os.getcwd()
    data = open(cwd+'/Bins/'+pBins+'/'+name+'_bin'+pBins+np.str(binNo)+'.json')
    pd = json.load(data)

    return pd


if __name__ == "__main__":

    par = sys.argv[1]
    biN = sys.argv[2]

    biN = np.int(biN)
    
    dataPX = open('pxnorm_distrSNR.json')
    dataRB = open('rdblurnorm_distrSNR.json')

    pdPX = json.load(dataPX)
    pdRB = json.load(dataRB)
    
    inBinPX = bin_sample(biN, par, pdPX, 'pxnorm')
    inBinRB = bin_sample(biN, par, pdRB, 'rdblurnorm')

    normPX = read_bin_sample('pxnorm', biN, par) #pdPX #normalize(pdPX)
    normRB = read_bin_sample('rdblurnorm', biN, par) #pdRB #normalize(pdRB)

    betaPX = fit_beta(normPX, 'pxnorm', biN, par)
    betaRB = fit_beta(normRB, 'rdblurnorm', biN, par)
  
    #rbetaPX = open('pxnorm_beta.json')
    #rbetaRB = open('rdblurnorm_beta.json')

    #betaPX = json.load(rbetaPX)
    #betaRB = json.load(rbetaRB)

    #for k in normPX.keys():
    #    plot_realbeta_distr(normPX[k], normRB[k], betaPX[k], betaRB[k], k)

    


