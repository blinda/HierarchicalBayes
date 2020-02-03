import sys
import os
import pystan
import numpy as np

def compile_Stan():
    spec= """
        data {
            int<lower=0> N;

            vector[N] a;
            vector[N] b;
            vector[N] loc;
            vector[N] scale;
        }
        parameters {
            real<lower=-3, upper=2> mu;
            real<lower=-2, upper=2> logsigma;
            vector<lower=0, upper=1>[N] u;
        }
        transformed parameters {
            vector[N] x;
            real<lower=0> sigma;
            x = u .* scale + loc;
            sigma = pow(10, logsigma);
        }

        model {
            u ~ beta(a, b);
            x ~ normal(mu, sigma);
        }

        """


    sm = pystan.StanModel(model_code=spec)
    return sm


def fit_totSample_Stan(name, sm):
    cwd = os.getcwd()
    dat = np.load(cwd+'/totSample/'+name+'_pyStanSNR.npz')
    data = dict(a=dat['a'], b=dat['b'], loc=dat['loc'], scale=dat['scale'], N=dat['N'])

    fit = sm.sampling(data=data, iter=1000, chains=4)


    la = fit.extract(permuted=True)  # return a dictionary of arrays
    mu = la['mu']
    sigma = la['sigma']

    np.savez(cwd+'/MuSigma/'+name+'_MuSigma.npz', mu=mu, sigma=sigma)
    return mu, sigma



def fit_Stan(name, pBins, biN, sm):

    cwd = os.getcwd()
    #dat = np.load('pxnorm_pyStanSNR.npz')
    dat = np.load(cwd+'/Bins/'+pBins+'/'+name+'_pyStanSNR'+pBins+np.str(biN)+'.npz')

    data = dict(a=dat['a'], b=dat['b'], loc=dat['loc'], scale=dat['scale'], N=dat['N'])

    fit = sm.sampling(data=data, iter=1000, chains=4)


    la = fit.extract(permuted=True)  # return a dictionary of arrays
    mu = la['mu']
    sigma = la['sigma']

    np.savez(cwd+'/MuSigma/'+pBins+'/'+name+'_MuSigma'+pBins+np.str(biN)+'.npz', mu=mu, sigma=sigma)
    return mu, sigma


if __name__=="__main__":

    pBins = ['L', 'NH', 'NHL', 'NHH', 'z', 'zL', 'zH']
    biN = np.arange(1,7)
    
    sm = compile_Stan()

    # m, s = fit_totSample_Stan('rdblurnorm', sm)

    for pb in pBins:
        for bn in biN:
            m, s = fit_Stan('pxnorm', pb, bn, sm)
            m, s = fit_Stan('rdblurnorm', pb, bn, sm)

    #datRB = np.load('rdblurnorm_pyStanSNR.npz')



