"""
Implements Lucy L Gao's test_clusters_approx function from clusterpval R package
Code for original function found in clusterpval/R/trunc_inf.R
clusterpval website: https://www.lucylgao.com/clusterpval/
Package described in: https://arxiv.org/abs/2012.02936
"""

import numpy as np
import math

def stattest_clusters_approx(X, k1, k2, cluster_labels, cl_fun, positional_arguments, keyword_arguments,
                             iso=True, sig=None, SigInv=None, ndraws=1):
    """
    Monte-Carlo significance test for any clustering method. This function takes matrix X clustered
    into K clusters and tests the null hypothesis of no difference in means between clusters k1 and
    k2. To account for the fact that the clusters were estimated from the data, the p-values are
    computed conditional on the fact that those clusters were estimated. P-values are approximated
    via importance sampling.
    :param X: n by p matrix, containing numeric data
    :param k1: integer, selects a cluster to test
    :param k2: integer, selects a cluster to test
    :param cluster_labels: numpy.ndarray, labels of each point (row) in X
    :param iso: boolean, if True isotropic covariance matrix model, otherwise not
    :param sig: optional scalar specifying sigma,  relevant if iso == True
    :param SigInv: optional matrix specifying Sigma^-1, relevant if iso == False
    :param ndraws: integer, selects the number of importance samples, default of 2000
    :return:
        - stat - float, the test statistic: Euclidean distance between mean of cluster k1 and mean of
                 cluster k2
        - pval - float, the approximate p value
        - stderr - float, the standard error of the p-value estimate
    """

    #check to make sure X is 2D ndarray
    rows, cols = X.shape
    n = rows
    q = cols

    unique, counts = np.unique(cluster_labels, return_counts=True)
    K = len(unique)
    #check to make sure K (number of clusters) is between 2 and n
    #check to make sure k1 and k2 are between 0 and K-1
    #maybe check to make sure iso is true or false, or set default to true (as is done here)
    points_per_cluster = dict(zip(unique, counts))
    n1 = points_per_cluster[k1]
    n2 = points_per_cluster[k2]
    squared_norm_nu = (1/n1) + (1/n2)
    k1colmeans = np.mean(X[cluster_labels == k1,:], axis=0)
    k2colmeans = np.mean(X[cluster_labels == k2,:], axis=0)
    diff_means = k1colmeans - k2colmeans
    prop_k2 = n2/(n1+n2)

    if iso == True:
        if sig == None:
            colmeans = np.mean(X, axis=0)
            scaledX = X - colmeans
            sig = math.sqrt(np.sum(scaledX**2) / (n*q - q))
        else:
            pass
        scale_factor = squared_norm_nu * (sig ** 2)
        #Compute test statistic
        stat = np.linalg.norm(diff_means)
    else:
        if SigInv == None:
            colmeans = np.mean(X, axis=0)
            scaledX = X - colmeans
            #print(scaledX)
            Sig = np.cov(scaledX, rowvar=False)
            SigInv = np.linalg.inv(Sig)
        else:
            pass
        scale_factor = squared_norm_nu
        #Compute test statistic
        tdiff_means = np.transpose(diff_means)
        stat = math.sqrt(np.matmul(np.matmul(tdiff_means, SigInv), diff_means))

    scale_factor = math.sqrt(scale_factor)
    log_survives = [None] * ndraws
    phi = np.random.normal(size=ndraws) * scale_factor + stat
    k1_constant = prop_k2*diff_means/stat
    k2_constant = (prop_k2 - 1)*diff_means/stat
    orig_k1 = np.transpose(X[cluster_labels == k1,:])
    orig_k2 = np.transpose(X[cluster_labels == k2, :])
    Xphi = X

    ndraws_above_0 = []
    for j in range(ndraws):
        if phi[j] < 0:
            continue
        #compute the perturbed data set
        Xphi = X
        Xphi[cluster_labels == k1, :] = np.transpose(orig_k1[:]) + ((phi[j] - stat) * k1_constant)
        Xphi[cluster_labels == k2, :] = np.transpose(orig_k2[:]) + ((phi[j] - stat) * k2_constant)

        #recluster the perturbed data set
        cl_Xphi = cl_fun(*positional_arguments, **keyword_arguments)
        cl_Xphi.fit_predict(Xphi)
        print(cl_Xphi.labels_)