import os
import numpy as np

def bins(pBins):

    L = np.array([ 39.1560813 ,  40.22955687,  41.30303244,  42.376508  ,
        43.44998357,  44.52345914,  45.5969347 ])
    NH = np.array([ 20.43562682,  21.08182227,  21.72801771,  
        22.37421315, 23.02040859,  23.66660404,  24.31279948])
    z = np.array([ 0.041  ,  0.67627,  1.31154,  1.94681,  
        2.58208,  3.21735,  3.85262])
    NHL = np.array([ 20.43562682,  21.08182227,  21.72801771,
        22.37421315, 23.02040859,  23.66660404,  24.31279948])
    NHH = np.array([ 20.48059555,  21.06971592,  21.6588363 ,  
        22.24795668,  22.83707706,  23.42619744,  24.01531782])
    zL = np.array([ 0.041     ,  0.65083333,  1.26066667,  1.8705    ,
        2.48033333, 3.09016667,  3.7       ])
    zH = np.array([ 0.345     ,  0.92960333,  1.51420667,  2.09881   ,  
        2.68341333,  3.26801667,  3.85262   ])

    if pBins=='L':
        return np.array([(L[i]+L[i+1])/2. for i in range(len(L)-1)])
    if pBins=='NH':
        return np.array([(NH[i]+NH[i+1])/2. for i in range(len(NH)-1)])
    if pBins=='NHL':
        return np.array([(NHL[i]+NHL[i+1])/2. for i in range(len(NHL)-1)])
    if pBins=='NHH':
        return np.array([(NHH[i]+NHH[i+1])/2. for i in range(len(NHH)-1)])
    if pBins=='z':
        return np.array([(z[i]+z[i+1])/2. for i in range(len(z)-1)])
    if pBins=='zL':
        return np.array([(zL[i]+zL[i+1])/2. for i in range(len(zL)-1)])
    if pBins=='zH':
        return np.array([(zH[i]+zH[i+1])/2. for i in range(len(zH)-1)])



def read_outputBin(name, biN, pBins):
    """
    Read the output of Stan for every bin
    """
    cwd = os.getcwd()
    data = np.load(cwd+'/MuSigma/'+pBins+'/'+name+'_MuSigma'+pBins+np.str(biN)+'.npz')
    return data['mu'], data['sigma']


def read_output(name, pBins):

    mu = np.zeros(6)
    errmu = np.zeros(6)
    sigma = np.zeros(6)
    errsigma = np.zeros(6)

    for j in range(1,7):
        i = j-1
        mu[i] = np.mean(read_outputBin(name, j, pBins)[0])
        errmu[i] = np.std(read_outputBin(name, j, pBins)[0])
        sigma[i] = np.mean(read_outputBin(name, j, pBins)[1])
        errsigma[i] = np.std(read_outputBin(name, j, pBins)[1])

    return mu, errmu, sigma, errsigma
