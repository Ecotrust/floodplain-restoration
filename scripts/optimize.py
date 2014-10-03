import sys
import os
from os.path import abspath, join, dirname
import numpy as np
import glob
import random
import copy
from simanneal import Annealer

sys.path.append(abspath(join(dirname(__file__), '..', 'dst')))
from bbn import BeliefNetwork

INPUT_BIF = abspath(join(dirname(__file__), '..', 'dst', 'dst', 'data',
                         'bbn.bif'))

OUTPUT_BIF = abspath(join(dirname(__file__), '..', 'dst', 'dst', 'data',
                          'bbn_OPTIMIZED.bif'))


class CPTOptimizer(Annealer):

    """ Optimize the conditional probability table of a bayesian belief network
    """

    def energy(self):
        """
        Calculate RMSE
        $$
        \textrm{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}
        $$
        """
        errors = []
        for training_site, suitability in training_sites.items():

            # TODO transform to proper dict as expected by the query method
            inputnodes = user_datas[training_site]

            res = self.state.query(
                inputnodes=inputnodes,
                outputnodes=(
                    ('socio_economic', 'suitable'),
                    ('site', 'suitable'),
                    ('landscape', 'suitable')
                )
            )

            prob = np.array(res)
            diff = prob - suitability
            errors.extend(list(diff))

        error = (np.array(errors) ** 2).mean() ** 0.5
        return error * 100

    def move(self):
        valid_move = False
        while not valid_move:
            # randomly choose one conditional decision variable
            var = random.choice(cond_vars)

            # randomly choose a set of given conditions
            clist = [random.choice(self.state.variables[x])
                     for x in self.state.probabilities[var]['given']]

            # randomly alter the probability table
            #  (first the True cond the false at 1.0 - val)
            first = self.state.variables[var][0]
            last = self.state.variables[var][1]
            key = tuple(clist + [first])
            lastkey = tuple(clist + [last])
            val = self.state.probabilities[var]['cpt'][key]
            newval = val + random.choice([0.05, -0.05])
            if newval >= 0.0 and newval <= 1.0:
                valid_move = True
                self.state.probabilities[var]['cpt'][key] = newval
                self.state.probabilities[var]['cpt'][lastkey] = 1.0 - newval

if __name__ == "__main__":

    bn = BeliefNetwork.from_bif(INPUT_BIF)

    training_sites = {}
    sites_glob = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     'optimization_files', 'training_sites', "*.txt"))
    user_datas = {}
    for training_site in glob.glob(sites_glob):
        socio_economic = site = landscape = None
        user_data = {}
        with open(training_site, 'r') as fh:
            for line in fh.readlines():
                key, val = line.split(',')
                val = float(val)
                try:
                    cond = bn.variables[key][0]  # assume first
                except KeyError:
                    print("    {} not found in BBN".format(key))
                if key == 'socio_economic':
                    socio_economic = val
                elif key == 'site':
                    site = val
                elif key == 'landscape':
                    landscape = val
                else:
                    user_data[key] = (cond, val)
                """
                user_data = {
                    'infrastructure': ('suitable', 0.5),
                    ...
                }
                """

        if None not in [socio_economic, site, landscape]:
            suitability = np.array([socio_economic, site, landscape])
        else:
            import ipdb
            ipdb.set_trace()
            raise Exception(
                "Need socio_economic, site, landscape for each training site")
        training_sites[training_site] = suitability
        user_datas[training_site] = user_data

    cond_vars = [n for n, p in bn.probabilities.items()
                 if p['given']]  # given is not None ~ conditional

    annealer = CPTOptimizer(bn)
    annealer.steps = 8000.0
    annealer.Tmax = 0.33
    annealer.Tmin = 6.7e-14 
    annealer.updates = annealer.steps / 5
    annealer.copy_strategy = 'deepcopy'
    state, e = annealer.anneal()

    state.to_bif(OUTPUT_BIF, round=True)
    print()
    print(OUTPUT_BIF)
    print()
