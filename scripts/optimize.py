from bayesian.bbn import build_bbn
import os

print("Note... using cpt.py and cpt.xls in /data!")

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dst')))
from bbn.cpt.xls import xls2cptdict, cptdict2xls

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
from cpt import query_cpt
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'optimization_files')))
from anneal import Annealer

CPT_XLS = os.path.abspath(os.path.join(os.path.dirname(__file__),
    '..', 'data', 'cpt.xls'))

OUTPUT_CPT_XLS = os.path.abspath(os.path.join(os.path.dirname(__file__),
    '..', 'data', 'cpt_OPTIMIZED.xls'))


USER_DATA = {
    'water_rights': 1.0,
     'surrounding_ownership': 1.0,
     'infrastructure': 1.0,
     'surrounding_land_use': 1.0,
     'property_value': 1.0,
     'contamination_or_hazardous_waste': 1.0,
     'public_perception': 1.0,
     'depth': 1.0,
     'complexity': 1.0,
     'surface_area': 1.0,
     'bank_slope': 1.0,
     'restorable_substrate': 1.0,
     'contamination': 1.0,
     'slope_distance_to_river': 1.0,
     'bedrock_constraints': 1.0,
     'adjacent_river_depth': 1.0,
     'pit_adjacent_levees': 1.0,
     'fill_material_availability': 1.0,
     'site_accessibility': 1.0,
     'continuing_property_access': 1.0,
     'material_availability': 1.0,
     'channel_mobility': 1.0,
     'infrastructure_constraints': 1.0,
     'substrate': 1.0,
     'water_quality': 1.0,
     'downstream': 1.0,
     'upstream': 1.0,
     'on_property': 1.0,
     'location_in_floodplain': 1.0,
     'width': 1.0,
     'gradient': 1.0,
     'within_x_year_floodplain': 1.0,
     'identified_in_conservation_plan': 1.0,
     'relationship_to_protected_areas': 1.0,
     'intact_floodplain_forest': 1.0,
     'habitat_features': 1.0,
     'species_of_interest': 1.0,}

if __name__ == "__main__":
    import glob
    import random
    import copy

    training_sites = {}
    user_datas = {}
    sites_glob = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 
            'optimization_files', 'training_sites', "*.txt"))
    for training_site in glob.glob(sites_glob):
        user_data = USER_DATA.copy()
        socio_economic = site = landscape = None
        with open(training_site, 'r') as fh:
            for line in fh.readlines():
                key, val = line.split(',')
                val = float(val)
                if key == 'socio_economic':
                    socio_economic = val
                elif key == 'site':
                    site = val
                elif key == 'landscape':
                    landscape = val
                # elif key == 'suitability':
                #     suitability = val
                else:
                    user_data[key] = val

        if None not in [socio_economic, site, landscape]:
            suitability = np.array([socio_economic, site, landscape])
        else:
            import ipdb; ipdb.set_trace()
            raise Exception("Need socio_economic, site, landscape for each training site")
        training_sites[training_site] = suitability
        user_datas[training_site] = user_data

    CPT = xls2cptdict(CPT_XLS)  # , add_tilde=True)

    state = copy.deepcopy(CPT)
    
    def energy(state):
        """
        Calculate RMSE
        $$
        \textrm{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}
        $$
        """
        errors = []
        for training_site, suitability in training_sites.items():
            #import ipdb; ipdb.set_trace()
            #print(training_site)
            res = query_cpt(
                state, 
                user_datas[training_site],
                output_nodes=(
                    #'suitability',
                    'socio_economic',
                    'site',
                    'landscape'
                )
            )
            prob = np.array(res)
            diff = prob - suitability
            errors.extend(list(diff))

        error = (np.array(errors) ** 2).mean() ** 0.5
        return error * 100

    def move(state):
        valid_move = False
        while not valid_move:
            var = random.choice(list(state.keys()))
            cond = random.choice(list(state[var].keys()))
            val = state[var][cond]
            newval = val + random.choice([0.05, -0.05])
            if newval >= 0.0 and newval <= 1.0:
                valid_move = True
        #print var, cond, newval

        state[var][cond] = newval


    annealer = Annealer(energy, move)
    # schedule = annealer.auto(state, minutes=60.0, steps=20)
    # print schedule
    
    schedule = {'steps': 800.0, 'tmax': 0.33, 'tmin': 6.7e-14}
    #schedule = {'steps': 16000.0, 'tmax': 0.004, 'tmin': 0.000001}
    state, e = annealer.anneal(state, schedule['tmax'], schedule['tmin'], 
                                schedule['steps'], updates=schedule['steps']/5)


    cptdict2xls(state, OUTPUT_CPT_XLS)
    print()
    print(OUTPUT_CPT_XLS)
