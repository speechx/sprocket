# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import numpy as np


class GV (object):
    """A global variance (GV) statistics class
    Estimate statistics and perform postfilter based on
    the GV statistics

    """

    def __init__(self):
        pass

    def estimate(self, datalist):
        """Estimate GV statistics from list of data

        Parameters
        ---------
        datalist : list, shape ('num_data')
            List of several data ([T, dim]) sequence

        Returns
        ---------
        gvstats : array, shape (`2`, `dim`)
            Array of mean and standard deviation fo GV
        """

        n_files = len(datalist)

        var = []
        for i in range(n_files):
            data = datalist[i]
            var.append(np.var(data, axis=0))

        # calculate vm and vv
        vm = np.mean(np.array(var), axis=0)
        vv = np.var(np.array(var), axis=0)
        gvstats = np.r_[vm, vv]
        gvstats = gvstats.reshape(2, len(vm))

        return gvstats

    def postfilter(self, data, gvstats, startdim=1):
        """Perform postfilter based on GV statistics into data

        Parameters
        ---------
        data : array, shape (`T`, `dim`)
            Array of data sequence
        startdim : int, optional
            Start dimension to perform GV postfilter

        Returns
        ---------
        filtered_data : array, shape (`T`, `data`)
            Array of GV postfiltered data sequence

        """

        # get length and dimension
        T, dim = data.shape
        assert gvstats is not None
        assert dim == gvstats.shape[1]

        # calculate statics of input data
        datamean = np.mean(data, axis=0)
        datavar = np.var(data, axis=0)

        # perform GV postfilter
        filtered = np.sqrt(gvstats[0, startdim:] / datavar[startdim:]) * \
            (data[:, startdim:] - datamean[startdim:]) + datamean[startdim:]

        filtered_data = np.c_[data[:, :startdim], filtered]

        return filtered_data
