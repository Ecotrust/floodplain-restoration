from bayesian.bbn import build_bbn
from bayes_xls import read_cpt
from flask import Flask, jsonify, redirect, request, render_template

app = Flask(__name__)

def chunks(lst, n):
    for i in xrange(0, len(lst), n):
        yield lst[i:i+n]

@app.route('/', methods = ['GET'])
def main():
    items = USER_DATA.items()
    items.sort()
    length = len(items)
    n = 11
    b = range(0, length, n)
    return render_template("sliders.html", 
        user_data1=items[b[0]:b[0]+n],
        user_data2=items[b[1]:b[1]+n],
        user_data3=items[b[2]:b[2]+n],
        user_data4=items[b[3]:b[3]+n]
    )

@app.route('/query', methods = ['GET'])
def prob_json():
    print "#" * 80
    user_data = USER_DATA.copy()
    for k, v in request.args.items():
        newval = float(v) / 100.0
        if user_data[k] != newval:
            print k, v
        user_data[k] = newval

    prob = query_cpt(user_data)
    print "!!!!!!", prob
    print "#" * 80
    return jsonify({'restore': round(prob * 100, 2)})

def query_cpt(user_data=None):
    if not user_data:
        user_data = {}

    CPT = read_cpt('cpt.xls')



    def f_suitability(socio_economic, site, landscape, suitability):
        cpt = {
            # Suitable, Suitable, Suitable
            (True, True, True): CPT['suitability'][('Suitable', 'Suitable', 'Suitable')],

            # Unsuitable, Suitable, Unsuitable
            (False, True, False): CPT['suitability'][('Unsuitable', 'Suitable', 'Unsuitable')],

            # Suitable, Suitable, Unsuitable
            (True, True, False): CPT['suitability'][('Suitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Suitable
            (False, False, True): CPT['suitability'][('Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable
            (False, True, True): CPT['suitability'][('Unsuitable', 'Suitable', 'Suitable')],

            # Suitable, Unsuitable, Unsuitable
            (True, False, False): CPT['suitability'][('Suitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Unsuitable
            (False, False, False): CPT['suitability'][('Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Unsuitable, Suitable
            (True, False, True): CPT['suitability'][('Suitable', 'Unsuitable', 'Suitable')],


        }
        p = cpt[(socio_economic, site, landscape)]
        if suitability:
            return p
        else:
            return 1.0 - p
    

    def f_socio_economic(threats_to_other_areas_or_permittability, cost_benefit, socio_economic):
        cpt = {
            # Threatened, Beneficial
            (False, True): CPT['Socio-Economic'][('Threatened', 'Beneficial')],

            # Threatened, Costly
            (False, False): CPT['Socio-Economic'][('Threatened', 'Costly')],

            # No threats, Beneficial
            (True, True): CPT['Socio-Economic'][('No threats', 'Beneficial')],

            # No threats, Costly
            (True, False): CPT['Socio-Economic'][('No threats', 'Costly')],


        }
        p = cpt[(threats_to_other_areas_or_permittability, cost_benefit)]
        if socio_economic:
            return p
        else:
            return 1.0 - p
    

    def f_threats_to_other_areas_or_permittability(water_rights, surrounding_ownership, infrastructure, surrounding_land_use, threats_to_other_areas_or_permittability):
        cpt = {
            # Threatened, Ammenable, No threats, Unfriendly
            (False, True, True, False): CPT['Threats to other areas or'][('Threatened', 'Ammenable', 'No threats', 'Unfriendly')],

            # No threats, Ammenable, Threatened, Ammenable
            (True, True, False, True): CPT['Threats to other areas or'][('No threats', 'Ammenable', 'Threatened', 'Ammenable')],

            # No threats, Unfriendly, Threatened, Ammenable
            (True, False, False, True): CPT['Threats to other areas or'][('No threats', 'Unfriendly', 'Threatened', 'Ammenable')],

            # Threatened, Unfriendly, No threats, Unfriendly
            (False, False, True, False): CPT['Threats to other areas or'][('Threatened', 'Unfriendly', 'No threats', 'Unfriendly')],

            # No threats, Unfriendly, Threatened, Unfriendly
            (True, False, False, False): CPT['Threats to other areas or'][('No threats', 'Unfriendly', 'Threatened', 'Unfriendly')],

            # Threatened, Unfriendly, Threatened, Ammenable
            (False, False, False, True): CPT['Threats to other areas or'][('Threatened', 'Unfriendly', 'Threatened', 'Ammenable')],

            # Threatened, Ammenable, No threats, Ammenable
            (False, True, True, True): CPT['Threats to other areas or'][('Threatened', 'Ammenable', 'No threats', 'Ammenable')],

            # Threatened, Ammenable, Threatened, Unfriendly
            (False, True, False, False): CPT['Threats to other areas or'][('Threatened', 'Ammenable', 'Threatened', 'Unfriendly')],

            # No threats, Unfriendly, No threats, Ammenable
            (True, False, True, True): CPT['Threats to other areas or'][('No threats', 'Unfriendly', 'No threats', 'Ammenable')],

            # Threatened, Unfriendly, Threatened, Unfriendly
            (False, False, False, False): CPT['Threats to other areas or'][('Threatened', 'Unfriendly', 'Threatened', 'Unfriendly')],

            # No threats, Ammenable, No threats, Unfriendly
            (True, True, True, False): CPT['Threats to other areas or'][('No threats', 'Ammenable', 'No threats', 'Unfriendly')],

            # Threatened, Ammenable, Threatened, Ammenable
            (False, True, False, True): CPT['Threats to other areas or'][('Threatened', 'Ammenable', 'Threatened', 'Ammenable')],

            # No threats, Ammenable, Threatened, Unfriendly
            (True, True, False, False): CPT['Threats to other areas or'][('No threats', 'Ammenable', 'Threatened', 'Unfriendly')],

            # No threats, Unfriendly, No threats, Unfriendly
            (True, False, True, False): CPT['Threats to other areas or'][('No threats', 'Unfriendly', 'No threats', 'Unfriendly')],

            # Threatened, Unfriendly, No threats, Ammenable
            (False, False, True, True): CPT['Threats to other areas or'][('Threatened', 'Unfriendly', 'No threats', 'Ammenable')],

            # No threats, Ammenable, No threats, Ammenable
            (True, True, True, True): CPT['Threats to other areas or'][('No threats', 'Ammenable', 'No threats', 'Ammenable')],


        }
        p = cpt[(water_rights, surrounding_ownership, infrastructure, surrounding_land_use)]
        if threats_to_other_areas_or_permittability:
            return p
        else:
            return 1.0 - p
    

    def f_water_rights(water_rights):
        if water_rights:
            return prob['water_rights']
        else:
            return 1.0 - prob['water_rights']
    

    def f_surrounding_ownership(surrounding_ownership):
        if surrounding_ownership:
            return prob['surrounding_ownership']
        else:
            return 1.0 - prob['surrounding_ownership']
    

    def f_infrastructure(structures, dams, road_crossings, levies, bridges, infrastructure):
        cpt = {
            # No threats, Threatened, Threatened, No threats, No threats
            (True, False, False, True, True): CPT['Infrastructure'][('No threats', 'Threatened', 'Threatened', 'No threats', 'No threats')],

            # Threatened, Threatened, No threats, Threatened, No threats
            (False, False, True, False, True): CPT['Infrastructure'][('Threatened', 'Threatened', 'No threats', 'Threatened', 'No threats')],

            # Threatened, No threats, No threats, Threatened, Threatened
            (False, True, True, False, False): CPT['Infrastructure'][('Threatened', 'No threats', 'No threats', 'Threatened', 'Threatened')],

            # No threats, No threats, No threats, Threatened, Threatened
            (True, True, True, False, False): CPT['Infrastructure'][('No threats', 'No threats', 'No threats', 'Threatened', 'Threatened')],

            # Threatened, No threats, No threats, No threats, No threats
            (False, True, True, True, True): CPT['Infrastructure'][('Threatened', 'No threats', 'No threats', 'No threats', 'No threats')],

            # No threats, Threatened, Threatened, Threatened, Threatened
            (True, False, False, False, False): CPT['Infrastructure'][('No threats', 'Threatened', 'Threatened', 'Threatened', 'Threatened')],

            # No threats, Threatened, No threats, No threats, Threatened
            (True, False, True, True, False): CPT['Infrastructure'][('No threats', 'Threatened', 'No threats', 'No threats', 'Threatened')],

            # Threatened, Threatened, Threatened, No threats, Threatened
            (False, False, False, True, False): CPT['Infrastructure'][('Threatened', 'Threatened', 'Threatened', 'No threats', 'Threatened')],

            # Threatened, No threats, No threats, No threats, Threatened
            (False, True, True, True, False): CPT['Infrastructure'][('Threatened', 'No threats', 'No threats', 'No threats', 'Threatened')],

            # Threatened, No threats, No threats, Threatened, No threats
            (False, True, True, False, True): CPT['Infrastructure'][('Threatened', 'No threats', 'No threats', 'Threatened', 'No threats')],

            # No threats, No threats, Threatened, Threatened, Threatened
            (True, True, False, False, False): CPT['Infrastructure'][('No threats', 'No threats', 'Threatened', 'Threatened', 'Threatened')],

            # Threatened, No threats, Threatened, Threatened, No threats
            (False, True, False, False, True): CPT['Infrastructure'][('Threatened', 'No threats', 'Threatened', 'Threatened', 'No threats')],

            # Threatened, Threatened, Threatened, Threatened, Threatened
            (False, False, False, False, False): CPT['Infrastructure'][('Threatened', 'Threatened', 'Threatened', 'Threatened', 'Threatened')],

            # Threatened, No threats, Threatened, No threats, No threats
            (False, True, False, True, True): CPT['Infrastructure'][('Threatened', 'No threats', 'Threatened', 'No threats', 'No threats')],

            # Threatened, Threatened, Threatened, Threatened, No threats
            (False, False, False, False, True): CPT['Infrastructure'][('Threatened', 'Threatened', 'Threatened', 'Threatened', 'No threats')],

            # No threats, No threats, No threats, Threatened, No threats
            (True, True, True, False, True): CPT['Infrastructure'][('No threats', 'No threats', 'No threats', 'Threatened', 'No threats')],

            # No threats, No threats, Threatened, Threatened, No threats
            (True, True, False, False, True): CPT['Infrastructure'][('No threats', 'No threats', 'Threatened', 'Threatened', 'No threats')],

            # No threats, Threatened, Threatened, Threatened, No threats
            (True, False, False, False, True): CPT['Infrastructure'][('No threats', 'Threatened', 'Threatened', 'Threatened', 'No threats')],

            # Threatened, No threats, Threatened, Threatened, Threatened
            (False, True, False, False, False): CPT['Infrastructure'][('Threatened', 'No threats', 'Threatened', 'Threatened', 'Threatened')],

            # Threatened, Threatened, No threats, Threatened, Threatened
            (False, False, True, False, False): CPT['Infrastructure'][('Threatened', 'Threatened', 'No threats', 'Threatened', 'Threatened')],

            # No threats, No threats, No threats, No threats, Threatened
            (True, True, True, True, False): CPT['Infrastructure'][('No threats', 'No threats', 'No threats', 'No threats', 'Threatened')],

            # No threats, No threats, Threatened, No threats, No threats
            (True, True, False, True, True): CPT['Infrastructure'][('No threats', 'No threats', 'Threatened', 'No threats', 'No threats')],

            # No threats, Threatened, Threatened, No threats, Threatened
            (True, False, False, True, False): CPT['Infrastructure'][('No threats', 'Threatened', 'Threatened', 'No threats', 'Threatened')],

            # No threats, No threats, Threatened, No threats, Threatened
            (True, True, False, True, False): CPT['Infrastructure'][('No threats', 'No threats', 'Threatened', 'No threats', 'Threatened')],

            # No threats, No threats, No threats, No threats, No threats
            (True, True, True, True, True): CPT['Infrastructure'][('No threats', 'No threats', 'No threats', 'No threats', 'No threats')],

            # Threatened, Threatened, No threats, No threats, No threats
            (False, False, True, True, True): CPT['Infrastructure'][('Threatened', 'Threatened', 'No threats', 'No threats', 'No threats')],

            # Threatened, Threatened, Threatened, No threats, No threats
            (False, False, False, True, True): CPT['Infrastructure'][('Threatened', 'Threatened', 'Threatened', 'No threats', 'No threats')],

            # No threats, Threatened, No threats, Threatened, No threats
            (True, False, True, False, True): CPT['Infrastructure'][('No threats', 'Threatened', 'No threats', 'Threatened', 'No threats')],

            # No threats, Threatened, No threats, Threatened, Threatened
            (True, False, True, False, False): CPT['Infrastructure'][('No threats', 'Threatened', 'No threats', 'Threatened', 'Threatened')],

            # Threatened, No threats, Threatened, No threats, Threatened
            (False, True, False, True, False): CPT['Infrastructure'][('Threatened', 'No threats', 'Threatened', 'No threats', 'Threatened')],

            # No threats, Threatened, No threats, No threats, No threats
            (True, False, True, True, True): CPT['Infrastructure'][('No threats', 'Threatened', 'No threats', 'No threats', 'No threats')],

            # Threatened, Threatened, No threats, No threats, Threatened
            (False, False, True, True, False): CPT['Infrastructure'][('Threatened', 'Threatened', 'No threats', 'No threats', 'Threatened')],


        }
        p = cpt[(structures, dams, road_crossings, levies, bridges)]
        if infrastructure:
            return p
        else:
            return 1.0 - p
    

    def f_structures(structures):
        if structures:
            return prob['structures']
        else:
            return 1.0 - prob['structures']
    

    def f_dams(dams):
        if dams:
            return prob['dams']
        else:
            return 1.0 - prob['dams']
    

    def f_road_crossings(road_crossings):
        if road_crossings:
            return prob['road_crossings']
        else:
            return 1.0 - prob['road_crossings']
    

    def f_levies(levies):
        if levies:
            return prob['levies']
        else:
            return 1.0 - prob['levies']
    

    def f_bridges(bridges):
        if bridges:
            return prob['bridges']
        else:
            return 1.0 - prob['bridges']
    

    def f_surrounding_land_use(surrounding_land_use):
        if surrounding_land_use:
            return prob['surrounding_land_use']
        else:
            return 1.0 - prob['surrounding_land_use']
    

    def f_cost_benefit(property_value, contamination_or_hazardous_waste, public_perception, cost_benefit):
        cpt = {
            # Costly, Contaminated, Unfavorable
            (False, False, False): CPT['Cost benefit'][('Costly', 'Contaminated', 'Unfavorable')],

            # Good Deal, Clean, Supportive
            (True, True, True): CPT['Cost benefit'][('Good Deal', 'Clean', 'Supportive')],

            # Good Deal, Contaminated, Unfavorable
            (True, False, False): CPT['Cost benefit'][('Good Deal', 'Contaminated', 'Unfavorable')],

            # Costly, Clean, Unfavorable
            (False, True, False): CPT['Cost benefit'][('Costly', 'Clean', 'Unfavorable')],

            # Costly, Clean, Supportive
            (False, True, True): CPT['Cost benefit'][('Costly', 'Clean', 'Supportive')],

            # Costly, Contaminated, Supportive
            (False, False, True): CPT['Cost benefit'][('Costly', 'Contaminated', 'Supportive')],

            # Good Deal, Clean, Unfavorable
            (True, True, False): CPT['Cost benefit'][('Good Deal', 'Clean', 'Unfavorable')],

            # Good Deal, Contaminated, Supportive
            (True, False, True): CPT['Cost benefit'][('Good Deal', 'Contaminated', 'Supportive')],


        }
        p = cpt[(property_value, contamination_or_hazardous_waste, public_perception)]
        if cost_benefit:
            return p
        else:
            return 1.0 - p
    

    def f_property_value(property_value):
        if property_value:
            return prob['property_value']
        else:
            return 1.0 - prob['property_value']
    

    def f_contamination_or_hazardous_waste(contamination_or_hazardous_waste):
        if contamination_or_hazardous_waste:
            return prob['contamination_or_hazardous_waste']
        else:
            return 1.0 - prob['contamination_or_hazardous_waste']
    

    def f_public_perception(public_perception):
        if public_perception:
            return prob['public_perception']
        else:
            return 1.0 - prob['public_perception']
    

    def f_site(pit_restorability, practical_property_level_restorability, site):
        cpt = {
            # Suitable, Unsuitable
            (True, False): CPT['Site'][('Suitable', 'Unsuitable')],

            # Unsuitable, Suitable
            (False, True): CPT['Site'][('Unsuitable', 'Suitable')],

            # Unsuitable, Unsuitable
            (False, False): CPT['Site'][('Unsuitable', 'Unsuitable')],

            # Suitable, Suitable
            (True, True): CPT['Site'][('Suitable', 'Suitable')],


        }
        p = cpt[(pit_restorability, practical_property_level_restorability)]
        if site:
            return p
        else:
            return 1.0 - p
    

    def f_pit_restorability(pit_geometry, water_quality_threat, practical_restorability, pit_restorability):
        cpt = {
            # Suitable, Suitable, Suitable
            (True, True, True): CPT['Pit restorability'][('Suitable', 'Suitable', 'Suitable')],

            # Unsuitable, Suitable, Unsuitable
            (False, True, False): CPT['Pit restorability'][('Unsuitable', 'Suitable', 'Unsuitable')],

            # Suitable, Suitable, Unsuitable
            (True, True, False): CPT['Pit restorability'][('Suitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Suitable
            (False, False, True): CPT['Pit restorability'][('Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable
            (False, True, True): CPT['Pit restorability'][('Unsuitable', 'Suitable', 'Suitable')],

            # Suitable, Unsuitable, Unsuitable
            (True, False, False): CPT['Pit restorability'][('Suitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Unsuitable
            (False, False, False): CPT['Pit restorability'][('Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Unsuitable, Suitable
            (True, False, True): CPT['Pit restorability'][('Suitable', 'Unsuitable', 'Suitable')],


        }
        p = cpt[(pit_geometry, water_quality_threat, practical_restorability)]
        if pit_restorability:
            return p
        else:
            return 1.0 - p
    

    def f_pit_geometry(depth, circumference, surface_area, bank_slope, pit_geometry):
        cpt = {
            # Unsuitable, Unsuitable, Unsuitable, Unsuitable
            (False, False, False, False): CPT['Pit geometry'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Suitable, Suitable, Unsuitable
            (False, True, True, False): CPT['Pit geometry'][('Unsuitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Suitable, Unsuitable, Unsuitable
            (False, True, False, False): CPT['Pit geometry'][('Unsuitable', 'Suitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Unsuitable, Unsuitable, Unsuitable
            (True, False, False, False): CPT['Pit geometry'][('Suitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Suitable, Suitable, Unsuitable
            (True, True, True, False): CPT['Pit geometry'][('Suitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Suitable, Suitable, Unsuitable, Unsuitable
            (True, True, False, False): CPT['Pit geometry'][('Suitable', 'Suitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Suitable, Unsuitable, Suitable
            (True, True, False, True): CPT['Pit geometry'][('Suitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Suitable, Suitable, Suitable, Suitable
            (True, True, True, True): CPT['Pit geometry'][('Suitable', 'Suitable', 'Suitable', 'Suitable')],

            # Suitable, Unsuitable, Unsuitable, Suitable
            (True, False, False, True): CPT['Pit geometry'][('Suitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Suitable, Unsuitable, Suitable, Unsuitable
            (True, False, True, False): CPT['Pit geometry'][('Suitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Suitable, Suitable
            (False, False, True, True): CPT['Pit geometry'][('Unsuitable', 'Unsuitable', 'Suitable', 'Suitable')],

            # Unsuitable, Unsuitable, Unsuitable, Suitable
            (False, False, False, True): CPT['Pit geometry'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable, Suitable
            (False, True, True, True): CPT['Pit geometry'][('Unsuitable', 'Suitable', 'Suitable', 'Suitable')],

            # Unsuitable, Unsuitable, Suitable, Unsuitable
            (False, False, True, False): CPT['Pit geometry'][('Unsuitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Suitable, Unsuitable, Suitable
            (False, True, False, True): CPT['Pit geometry'][('Unsuitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Suitable, Unsuitable, Suitable, Suitable
            (True, False, True, True): CPT['Pit geometry'][('Suitable', 'Unsuitable', 'Suitable', 'Suitable')],


        }
        p = cpt[(depth, circumference, surface_area, bank_slope)]
        if pit_geometry:
            return p
        else:
            return 1.0 - p
    

    def f_depth(depth):
        if depth:
            return prob['depth']
        else:
            return 1.0 - prob['depth']
    

    def f_circumference(circumference):
        if circumference:
            return prob['circumference']
        else:
            return 1.0 - prob['circumference']
    

    def f_surface_area(surface_area):
        if surface_area:
            return prob['surface_area']
        else:
            return 1.0 - prob['surface_area']
    

    def f_bank_slope(bank_slope):
        if bank_slope:
            return prob['bank_slope']
        else:
            return 1.0 - prob['bank_slope']
    

    def f_water_quality_threat(restorable_substrate, contamination, water_quality_threat):
        cpt = {
            # Suitable, Unsuitable
            (True, False): CPT['Water quality threat'][('Suitable', 'Unsuitable')],

            # Unsuitable, Suitable
            (False, True): CPT['Water quality threat'][('Unsuitable', 'Suitable')],

            # Unsuitable, Unsuitable
            (False, False): CPT['Water quality threat'][('Unsuitable', 'Unsuitable')],

            # Suitable, Suitable
            (True, True): CPT['Water quality threat'][('Suitable', 'Suitable')],


        }
        p = cpt[(restorable_substrate, contamination)]
        if water_quality_threat:
            return p
        else:
            return 1.0 - p
    

    def f_restorable_substrate(restorable_substrate):
        if restorable_substrate:
            return prob['restorable_substrate']
        else:
            return 1.0 - prob['restorable_substrate']
    

    def f_contamination(contamination):
        if contamination:
            return prob['contamination']
        else:
            return 1.0 - prob['contamination']
    

    def f_practical_restorability(slope_distance_to_river, adjacent_river_depth, pit_adjacent_levees, practical_restorability):
        cpt = {
            # Suitable, Suitable, Suitable
            (True, True, True): CPT['Practical restorability'][('Suitable', 'Suitable', 'Suitable')],

            # Unsuitable, Suitable, Unsuitable
            (False, True, False): CPT['Practical restorability'][('Unsuitable', 'Suitable', 'Unsuitable')],

            # Suitable, Suitable, Unsuitable
            (True, True, False): CPT['Practical restorability'][('Suitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Suitable
            (False, False, True): CPT['Practical restorability'][('Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable
            (False, True, True): CPT['Practical restorability'][('Unsuitable', 'Suitable', 'Suitable')],

            # Suitable, Unsuitable, Unsuitable
            (True, False, False): CPT['Practical restorability'][('Suitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Unsuitable
            (False, False, False): CPT['Practical restorability'][('Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Unsuitable, Suitable
            (True, False, True): CPT['Practical restorability'][('Suitable', 'Unsuitable', 'Suitable')],


        }
        p = cpt[(slope_distance_to_river, adjacent_river_depth, pit_adjacent_levees)]
        if practical_restorability:
            return p
        else:
            return 1.0 - p
    

    def f_slope_distance_to_river(slope_distance_to_river):
        if slope_distance_to_river:
            return prob['slope_distance_to_river']
        else:
            return 1.0 - prob['slope_distance_to_river']
    

    def f_adjacent_river_depth(adjacent_river_depth):
        if adjacent_river_depth:
            return prob['adjacent_river_depth']
        else:
            return 1.0 - prob['adjacent_river_depth']
    

    def f_pit_adjacent_levees(pit_adjacent_levees):
        if pit_adjacent_levees:
            return prob['pit_adjacent_levees']
        else:
            return 1.0 - prob['pit_adjacent_levees']
    

    def f_practical_property_level_restorability(fill_material_availability, site_accessibility, continuing_property_access, practical_property_level_restorability):
        cpt = {
            # Unavailable, Inaccessible, Suitable
            (False, False, True): CPT['Practical property-level '][('Unavailable', 'Inaccessible', 'Suitable')],

            # Available, Accessible, Suitable
            (True, True, True): CPT['Practical property-level '][('Available', 'Accessible', 'Suitable')],

            # Unavailable, Inaccessible, Unsuitable
            (False, False, False): CPT['Practical property-level '][('Unavailable', 'Inaccessible', 'Unsuitable')],

            # Available, Inaccessible, Unsuitable
            (True, False, False): CPT['Practical property-level '][('Available', 'Inaccessible', 'Unsuitable')],

            # Available, Accessible, Unsuitable
            (True, True, False): CPT['Practical property-level '][('Available', 'Accessible', 'Unsuitable')],

            # Available, Inaccessible, Suitable
            (True, False, True): CPT['Practical property-level '][('Available', 'Inaccessible', 'Suitable')],

            # Unavailable, Accessible, Unsuitable
            (False, True, False): CPT['Practical property-level '][('Unavailable', 'Accessible', 'Unsuitable')],

            # Unavailable, Accessible, Suitable
            (False, True, True): CPT['Practical property-level '][('Unavailable', 'Accessible', 'Suitable')],


        }
        p = cpt[(fill_material_availability, site_accessibility, continuing_property_access)]
        if practical_property_level_restorability:
            return p
        else:
            return 1.0 - p
    

    def f_fill_material_availability(fill_material_availability):
        if fill_material_availability:
            return prob['fill_material_availability']
        else:
            return 1.0 - prob['fill_material_availability']
    

    def f_site_accessibility(site_accessibility):
        if site_accessibility:
            return prob['site_accessibility']
        else:
            return 1.0 - prob['site_accessibility']
    

    def f_continuing_property_access(continuing_property_access):
        if continuing_property_access:
            return prob['continuing_property_access']
        else:
            return 1.0 - prob['continuing_property_access']
    

    def f_landscape(geomorphic_controls, abiotic_conditions, floodplain_characteristics, conservation_value, landscape):
        cpt = {
            # Unsuitable, Unsuitable, Unsuitable, Unsuitable
            (False, False, False, False): CPT['Landscape'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Suitable, Suitable, Unsuitable
            (False, True, True, False): CPT['Landscape'][('Unsuitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Suitable, Unsuitable, Unsuitable
            (False, True, False, False): CPT['Landscape'][('Unsuitable', 'Suitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Unsuitable, Unsuitable, Unsuitable
            (True, False, False, False): CPT['Landscape'][('Suitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Suitable, Suitable, Unsuitable
            (True, True, True, False): CPT['Landscape'][('Suitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Suitable, Suitable, Unsuitable, Unsuitable
            (True, True, False, False): CPT['Landscape'][('Suitable', 'Suitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Suitable, Unsuitable, Suitable
            (True, True, False, True): CPT['Landscape'][('Suitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Suitable, Suitable, Suitable, Suitable
            (True, True, True, True): CPT['Landscape'][('Suitable', 'Suitable', 'Suitable', 'Suitable')],

            # Suitable, Unsuitable, Unsuitable, Suitable
            (True, False, False, True): CPT['Landscape'][('Suitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Suitable, Unsuitable, Suitable, Unsuitable
            (True, False, True, False): CPT['Landscape'][('Suitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Suitable, Suitable
            (False, False, True, True): CPT['Landscape'][('Unsuitable', 'Unsuitable', 'Suitable', 'Suitable')],

            # Unsuitable, Unsuitable, Unsuitable, Suitable
            (False, False, False, True): CPT['Landscape'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable, Suitable
            (False, True, True, True): CPT['Landscape'][('Unsuitable', 'Suitable', 'Suitable', 'Suitable')],

            # Unsuitable, Unsuitable, Suitable, Unsuitable
            (False, False, True, False): CPT['Landscape'][('Unsuitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Suitable, Unsuitable, Suitable
            (False, True, False, True): CPT['Landscape'][('Unsuitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Suitable, Unsuitable, Suitable, Suitable
            (True, False, True, True): CPT['Landscape'][('Suitable', 'Unsuitable', 'Suitable', 'Suitable')],


        }
        p = cpt[(geomorphic_controls, abiotic_conditions, floodplain_characteristics, conservation_value)]
        if landscape:
            return p
        else:
            return 1.0 - p
    

    def f_geomorphic_controls(material_availability, channel_mobility, infrastructure_constraints, substrate, geomorphic_controls):
        cpt = {
            # Unavailable, Mobile, Unsuitable, Unsuitable
            (False, True, False, False): CPT['Geomorphic Controls'][('Unavailable', 'Mobile', 'Unsuitable', 'Unsuitable')],

            # Available, Not mobile, Unsuitable, Unsuitable
            (True, False, False, False): CPT['Geomorphic Controls'][('Available', 'Not mobile', 'Unsuitable', 'Unsuitable')],

            # Unavailable, Mobile, Unsuitable, Suitable
            (False, True, False, True): CPT['Geomorphic Controls'][('Unavailable', 'Mobile', 'Unsuitable', 'Suitable')],

            # Unavailable, Not mobile, No restrictions, Unsuitable
            (False, False, True, False): CPT['Geomorphic Controls'][('Unavailable', 'Not mobile', 'No restrictions', 'Unsuitable')],

            # Unavailable, Mobile, No restrictions, Unsuitable
            (False, True, True, False): CPT['Geomorphic Controls'][('Unavailable', 'Mobile', 'No restrictions', 'Unsuitable')],

            # Available, Not mobile, Unsuitable, Suitable
            (True, False, False, True): CPT['Geomorphic Controls'][('Available', 'Not mobile', 'Unsuitable', 'Suitable')],

            # Available, Not mobile, No restrictions, Suitable
            (True, False, True, True): CPT['Geomorphic Controls'][('Available', 'Not mobile', 'No restrictions', 'Suitable')],

            # Unavailable, Not mobile, Unsuitable, Suitable
            (False, False, False, True): CPT['Geomorphic Controls'][('Unavailable', 'Not mobile', 'Unsuitable', 'Suitable')],

            # Unavailable, Not mobile, Unsuitable, Unsuitable
            (False, False, False, False): CPT['Geomorphic Controls'][('Unavailable', 'Not mobile', 'Unsuitable', 'Unsuitable')],

            # Unavailable, Not mobile, No restrictions, Suitable
            (False, False, True, True): CPT['Geomorphic Controls'][('Unavailable', 'Not mobile', 'No restrictions', 'Suitable')],

            # Available, Mobile, Unsuitable, Suitable
            (True, True, False, True): CPT['Geomorphic Controls'][('Available', 'Mobile', 'Unsuitable', 'Suitable')],

            # Available, Mobile, No restrictions, Unsuitable
            (True, True, True, False): CPT['Geomorphic Controls'][('Available', 'Mobile', 'No restrictions', 'Unsuitable')],

            # Available, Not mobile, No restrictions, Unsuitable
            (True, False, True, False): CPT['Geomorphic Controls'][('Available', 'Not mobile', 'No restrictions', 'Unsuitable')],

            # Available, Mobile, Unsuitable, Unsuitable
            (True, True, False, False): CPT['Geomorphic Controls'][('Available', 'Mobile', 'Unsuitable', 'Unsuitable')],

            # Available, Mobile, No restrictions, Suitable
            (True, True, True, True): CPT['Geomorphic Controls'][('Available', 'Mobile', 'No restrictions', 'Suitable')],

            # Unavailable, Mobile, No restrictions, Suitable
            (False, True, True, True): CPT['Geomorphic Controls'][('Unavailable', 'Mobile', 'No restrictions', 'Suitable')],


        }
        p = cpt[(material_availability, channel_mobility, infrastructure_constraints, substrate)]
        if geomorphic_controls:
            return p
        else:
            return 1.0 - p
    

    def f_material_availability(material_availability):
        if material_availability:
            return prob['material_availability']
        else:
            return 1.0 - prob['material_availability']
    

    def f_channel_mobility(channel_mobility):
        if channel_mobility:
            return prob['channel_mobility']
        else:
            return 1.0 - prob['channel_mobility']
    

    def f_infrastructure_constraints(infrastructure_constraints):
        if infrastructure_constraints:
            return prob['infrastructure_constraints']
        else:
            return 1.0 - prob['infrastructure_constraints']
    

    def f_substrate(substrate):
        if substrate:
            return prob['substrate']
        else:
            return 1.0 - prob['substrate']
    

    def f_abiotic_conditions(water_quality, connectivity_barriers, abiotic_conditions):
        cpt = {
            # Low Quality, Disconnected
            (False, False): CPT['Abiotic conditions'][('Low Quality', 'Disconnected')],

            # High Quality, Connected
            (True, True): CPT['Abiotic conditions'][('High Quality', 'Connected')],

            # Low Quality, Connected
            (False, True): CPT['Abiotic conditions'][('Low Quality', 'Connected')],

            # High Quality, Disconnected
            (True, False): CPT['Abiotic conditions'][('High Quality', 'Disconnected')],


        }
        p = cpt[(water_quality, connectivity_barriers)]
        if abiotic_conditions:
            return p
        else:
            return 1.0 - p
    

    def f_water_quality(water_quality):
        if water_quality:
            return prob['water_quality']
        else:
            return 1.0 - prob['water_quality']
    

    def f_connectivity_barriers(downstream, upstream, on_property, connectivity_barriers):
        cpt = {
            # Connected, Disconnected, Disconnected
            (True, False, False): CPT['Connectivity barriers'][('Connected', 'Disconnected', 'Disconnected')],

            # Connected, Connected, Disconnected
            (True, True, False): CPT['Connectivity barriers'][('Connected', 'Connected', 'Disconnected')],

            # Disconnected, Disconnected, Connected
            (False, False, True): CPT['Connectivity barriers'][('Disconnected', 'Disconnected', 'Connected')],

            # Connected, Disconnected, Connected
            (True, False, True): CPT['Connectivity barriers'][('Connected', 'Disconnected', 'Connected')],

            # Disconnected, Connected, Disconnected
            (False, True, False): CPT['Connectivity barriers'][('Disconnected', 'Connected', 'Disconnected')],

            # Disconnected, Disconnected, Disconnected
            (False, False, False): CPT['Connectivity barriers'][('Disconnected', 'Disconnected', 'Disconnected')],

            # Disconnected, Connected, Connected
            (False, True, True): CPT['Connectivity barriers'][('Disconnected', 'Connected', 'Connected')],

            # Connected, Connected, Connected
            (True, True, True): CPT['Connectivity barriers'][('Connected', 'Connected', 'Connected')],


        }
        p = cpt[(downstream, upstream, on_property)]
        if connectivity_barriers:
            return p
        else:
            return 1.0 - p
    

    def f_downstream(downstream):
        if downstream:
            return prob['downstream']
        else:
            return 1.0 - prob['downstream']
    

    def f_upstream(upstream):
        if upstream:
            return prob['upstream']
        else:
            return 1.0 - prob['upstream']
    

    def f_on_property(on_property):
        if on_property:
            return prob['on_property']
        else:
            return 1.0 - prob['on_property']
    

    def f_floodplain_characteristics(location_in_floodplain, width, gradient, within_x_year_floodplain, floodplain_characteristics):
        cpt = {
            # Strategic, Suitable, Suitable, Outside
            (True, True, True, False): CPT['Floodplain characteristic'][('Strategic', 'Suitable', 'Suitable', 'Outside')],

            # Strategic, Unsuitable, Unsuitable, Outside
            (True, False, False, False): CPT['Floodplain characteristic'][('Strategic', 'Unsuitable', 'Unsuitable', 'Outside')],

            # Ineffective, Suitable, Unsuitable, Outside
            (False, True, False, False): CPT['Floodplain characteristic'][('Ineffective', 'Suitable', 'Unsuitable', 'Outside')],

            # Strategic, Unsuitable, Unsuitable, Within
            (True, False, False, True): CPT['Floodplain characteristic'][('Strategic', 'Unsuitable', 'Unsuitable', 'Within')],

            # Ineffective, Unsuitable, Suitable, Within
            (False, False, True, True): CPT['Floodplain characteristic'][('Ineffective', 'Unsuitable', 'Suitable', 'Within')],

            # Strategic, Unsuitable, Suitable, Outside
            (True, False, True, False): CPT['Floodplain characteristic'][('Strategic', 'Unsuitable', 'Suitable', 'Outside')],

            # Ineffective, Unsuitable, Unsuitable, Within
            (False, False, False, True): CPT['Floodplain characteristic'][('Ineffective', 'Unsuitable', 'Unsuitable', 'Within')],

            # Strategic, Suitable, Suitable, Within
            (True, True, True, True): CPT['Floodplain characteristic'][('Strategic', 'Suitable', 'Suitable', 'Within')],

            # Ineffective, Suitable, Unsuitable, Within
            (False, True, False, True): CPT['Floodplain characteristic'][('Ineffective', 'Suitable', 'Unsuitable', 'Within')],

            # Ineffective, Unsuitable, Suitable, Outside
            (False, False, True, False): CPT['Floodplain characteristic'][('Ineffective', 'Unsuitable', 'Suitable', 'Outside')],

            # Ineffective, Suitable, Suitable, Outside
            (False, True, True, False): CPT['Floodplain characteristic'][('Ineffective', 'Suitable', 'Suitable', 'Outside')],

            # Strategic, Suitable, Unsuitable, Within
            (True, True, False, True): CPT['Floodplain characteristic'][('Strategic', 'Suitable', 'Unsuitable', 'Within')],

            # Ineffective, Unsuitable, Unsuitable, Outside
            (False, False, False, False): CPT['Floodplain characteristic'][('Ineffective', 'Unsuitable', 'Unsuitable', 'Outside')],

            # Strategic, Suitable, Unsuitable, Outside
            (True, True, False, False): CPT['Floodplain characteristic'][('Strategic', 'Suitable', 'Unsuitable', 'Outside')],

            # Strategic, Unsuitable, Suitable, Within
            (True, False, True, True): CPT['Floodplain characteristic'][('Strategic', 'Unsuitable', 'Suitable', 'Within')],

            # Ineffective, Suitable, Suitable, Within
            (False, True, True, True): CPT['Floodplain characteristic'][('Ineffective', 'Suitable', 'Suitable', 'Within')],


        }
        p = cpt[(location_in_floodplain, width, gradient, within_x_year_floodplain)]
        if floodplain_characteristics:
            return p
        else:
            return 1.0 - p
    

    def f_location_in_floodplain(location_in_floodplain):
        if location_in_floodplain:
            return prob['location_in_floodplain']
        else:
            return 1.0 - prob['location_in_floodplain']
    

    def f_width(width):
        if width:
            return prob['width']
        else:
            return 1.0 - prob['width']
    

    def f_gradient(gradient):
        if gradient:
            return prob['gradient']
        else:
            return 1.0 - prob['gradient']
    

    def f_within_x_year_floodplain(within_x_year_floodplain):
        if within_x_year_floodplain:
            return prob['within_x_year_floodplain']
        else:
            return 1.0 - prob['within_x_year_floodplain']
    

    def f_conservation_value(identified_in_conservation_plan, relationship_to_protected_areas, biotic_conditions, conservation_value):
        cpt = {
            # Identified, Disconnected, Suitable
            (True, False, True): CPT['Conservation value'][('Identified', 'Disconnected', 'Suitable')],

            # Not Identified, Connected, Suitable
            (False, True, True): CPT['Conservation value'][('Not Identified', 'Connected', 'Suitable')],

            # Not Identified, Disconnected, Suitable
            (False, False, True): CPT['Conservation value'][('Not Identified', 'Disconnected', 'Suitable')],

            # Not Identified, Connected, Unsuitable
            (False, True, False): CPT['Conservation value'][('Not Identified', 'Connected', 'Unsuitable')],

            # Identified, Connected, Unsuitable
            (True, True, False): CPT['Conservation value'][('Identified', 'Connected', 'Unsuitable')],

            # Identified, Disconnected, Unsuitable
            (True, False, False): CPT['Conservation value'][('Identified', 'Disconnected', 'Unsuitable')],

            # Identified, Connected, Suitable
            (True, True, True): CPT['Conservation value'][('Identified', 'Connected', 'Suitable')],

            # Not Identified, Disconnected, Unsuitable
            (False, False, False): CPT['Conservation value'][('Not Identified', 'Disconnected', 'Unsuitable')],


        }
        p = cpt[(identified_in_conservation_plan, relationship_to_protected_areas, biotic_conditions)]
        if conservation_value:
            return p
        else:
            return 1.0 - p
    

    def f_identified_in_conservation_plan(identified_in_conservation_plan):
        if identified_in_conservation_plan:
            return prob['identified_in_conservation_plan']
        else:
            return 1.0 - prob['identified_in_conservation_plan']
    

    def f_relationship_to_protected_areas(relationship_to_protected_areas):
        if relationship_to_protected_areas:
            return prob['relationship_to_protected_areas']
        else:
            return 1.0 - prob['relationship_to_protected_areas']
    

    def f_biotic_conditions(habitat_features, species_of_interest, biotic_conditions):
        cpt = {
            # Unsuitable, Present
            (False, True): CPT['Biotic conditions'][('Unsuitable', 'Present')],

            # Unsuitable, Not Present
            (False, False): CPT['Biotic conditions'][('Unsuitable', 'Not Present')],

            # Suitable, Present
            (True, True): CPT['Biotic conditions'][('Suitable', 'Present')],

            # Suitable, Not Present
            (True, False): CPT['Biotic conditions'][('Suitable', 'Not Present')],


        }
        p = cpt[(habitat_features, species_of_interest)]
        if biotic_conditions:
            return p
        else:
            return 1.0 - p
    

    def f_habitat_features(intact_floodplain_forest, cold_water_refugia, other, habitat_features):
        cpt = {
            # Intact, Exists, Not Suitable
            (True, True, False): CPT['Habitat features'][('Intact', 'Exists', 'Not Suitable')],

            # Missing, Does not exist, Suitable
            (False, False, True): CPT['Habitat features'][('Missing', 'Does not exist', 'Suitable')],

            # Missing, Exists, Suitable
            (False, True, True): CPT['Habitat features'][('Missing', 'Exists', 'Suitable')],

            # Missing, Exists, Not Suitable
            (False, True, False): CPT['Habitat features'][('Missing', 'Exists', 'Not Suitable')],

            # Intact, Does not exist, Not Suitable
            (True, False, False): CPT['Habitat features'][('Intact', 'Does not exist', 'Not Suitable')],

            # Intact, Does not exist, Suitable
            (True, False, True): CPT['Habitat features'][('Intact', 'Does not exist', 'Suitable')],

            # Intact, Exists, Suitable
            (True, True, True): CPT['Habitat features'][('Intact', 'Exists', 'Suitable')],

            # Missing, Does not exist, Not Suitable
            (False, False, False): CPT['Habitat features'][('Missing', 'Does not exist', 'Not Suitable')],


        }
        p = cpt[(intact_floodplain_forest, cold_water_refugia, other)]
        if habitat_features:
            return p
        else:
            return 1.0 - p
    

    def f_intact_floodplain_forest(intact_floodplain_forest):
        if intact_floodplain_forest:
            return prob['intact_floodplain_forest']
        else:
            return 1.0 - prob['intact_floodplain_forest']
    

    def f_cold_water_refugia(cold_water_refugia):
        if cold_water_refugia:
            return prob['cold_water_refugia']
        else:
            return 1.0 - prob['cold_water_refugia']
    

    def f_other(other):
        if other:
            return prob['other']
        else:
            return 1.0 - prob['other']
    

    def f_species_of_interest(species_of_interest):
        if species_of_interest:
            return prob['species_of_interest']
        else:
            return 1.0 - prob['species_of_interest']
    

    levels = [True, False]
    net = build_bbn(
        f_suitability,
        f_socio_economic,
        f_threats_to_other_areas_or_permittability,
        f_water_rights,
        f_surrounding_ownership,
        f_infrastructure,
        f_structures,
        f_dams,
        f_road_crossings,
        f_levies,
        f_bridges,
        f_surrounding_land_use,
        f_cost_benefit,
        f_property_value,
        f_contamination_or_hazardous_waste,
        f_public_perception,
        f_site,
        f_pit_restorability,
        f_pit_geometry,
        f_depth,
        f_circumference,
        f_surface_area,
        f_bank_slope,
        f_water_quality_threat,
        f_restorable_substrate,
        f_contamination,
        f_practical_restorability,
        f_slope_distance_to_river,
        f_adjacent_river_depth,
        f_pit_adjacent_levees,
        f_practical_property_level_restorability,
        f_fill_material_availability,
        f_site_accessibility,
        f_continuing_property_access,
        f_landscape,
        f_geomorphic_controls,
        f_material_availability,
        f_channel_mobility,
        f_infrastructure_constraints,
        f_substrate,
        f_abiotic_conditions,
        f_water_quality,
        f_connectivity_barriers,
        f_downstream,
        f_upstream,
        f_on_property,
        f_floodplain_characteristics,
        f_location_in_floodplain,
        f_width,
        f_gradient,
        f_within_x_year_floodplain,
        f_conservation_value,
        f_identified_in_conservation_plan,
        f_relationship_to_protected_areas,
        f_biotic_conditions,
        f_habitat_features,
        f_intact_floodplain_forest,
        f_cold_water_refugia,
        f_other,
        f_species_of_interest,

        # assume simple binary
        domains=dict(
            suitability = levels,
            socio_economic = levels,
            threats_to_other_areas_or_permittability = levels,
            water_rights = levels,
            surrounding_ownership = levels,
            infrastructure = levels,
            structures = levels,
            dams = levels,
            road_crossings = levels,
            levies = levels,
            bridges = levels,
            surrounding_land_use = levels,
            cost_benefit = levels,
            property_value = levels,
            contamination_or_hazardous_waste = levels,
            public_perception = levels,
            site = levels,
            pit_restorability = levels,
            pit_geometry = levels,
            depth = levels,
            circumference = levels,
            surface_area = levels,
            bank_slope = levels,
            water_quality_threat = levels,
            restorable_substrate = levels,
            contamination = levels,
            practical_restorability = levels,
            slope_distance_to_river = levels,
            adjacent_river_depth = levels,
            pit_adjacent_levees = levels,
            practical_property_level_restorability = levels,
            fill_material_availability = levels,
            site_accessibility = levels,
            continuing_property_access = levels,
            landscape = levels,
            geomorphic_controls = levels,
            material_availability = levels,
            channel_mobility = levels,
            infrastructure_constraints = levels,
            substrate = levels,
            abiotic_conditions = levels,
            water_quality = levels,
            connectivity_barriers = levels,
            downstream = levels,
            upstream = levels,
            on_property = levels,
            floodplain_characteristics = levels,
            location_in_floodplain = levels,
            width = levels,
            gradient = levels,
            within_x_year_floodplain = levels,
            conservation_value = levels,
            identified_in_conservation_plan = levels,
            relationship_to_protected_areas = levels,
            biotic_conditions = levels,
            habitat_features = levels,
            intact_floodplain_forest = levels,
            cold_water_refugia = levels,
            other = levels,
            species_of_interest = levels,
        )
    )

    prob = dict(
    water_rights = 1.0,
        surrounding_ownership = 1.0,
        structures = 1.0,
        dams = 1.0,
        road_crossings = 1.0,
        levies = 1.0,
        bridges = 1.0,
        surrounding_land_use = 1.0,
        property_value = 1.0,
        contamination_or_hazardous_waste = 1.0,
        public_perception = 1.0,
        depth = 1.0,
        circumference = 1.0,
        surface_area = 1.0,
        bank_slope = 1.0,
        restorable_substrate = 1.0,
        contamination = 1.0,
        slope_distance_to_river = 1.0,
        adjacent_river_depth = 1.0,
        pit_adjacent_levees = 1.0,
        fill_material_availability = 1.0,
        site_accessibility = 1.0,
        continuing_property_access = 1.0,
        material_availability = 1.0,
        channel_mobility = 1.0,
        infrastructure_constraints = 1.0,
        substrate = 1.0,
        water_quality = 1.0,
        downstream = 1.0,
        upstream = 1.0,
        on_property = 1.0,
        location_in_floodplain = 1.0,
        width = 1.0,
        gradient = 1.0,
        within_x_year_floodplain = 1.0,
        identified_in_conservation_plan = 1.0,
        relationship_to_protected_areas = 1.0,
        intact_floodplain_forest = 1.0,
        cold_water_refugia = 1.0,
        other = 1.0,
        species_of_interest = 1.0,)

    for k,v in user_data.items():
        if prob.has_key(k):
            prob[k] = v

    return net.query()[('suitability', True)]

USER_DATA = {
    'water_rights': 1.0,
     'surrounding_ownership': 1.0,
     'structures': 1.0,
     'dams': 1.0,
     'road_crossings': 1.0,
     'levies': 1.0,
     'bridges': 1.0,
     'surrounding_land_use': 1.0,
     'property_value': 1.0,
     'contamination_or_hazardous_waste': 1.0,
     'public_perception': 1.0,
     'depth': 1.0,
     'circumference': 1.0,
     'surface_area': 1.0,
     'bank_slope': 1.0,
     'restorable_substrate': 1.0,
     'contamination': 1.0,
     'slope_distance_to_river': 1.0,
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
     'cold_water_refugia': 1.0,
     'other': 1.0,
     'species_of_interest': 1.0,}

import signal

class GracefulInterruptHandler(object):
    def __init__(self, sig=signal.SIGINT):
        self.sig = sig

    def __enter__(self):
        self.interrupted = False
        self.released = False
        self.original_handler = signal.getsignal(self.sig)

        def handler(signum, frame):
            self.release()
            self.interrupted = True

        signal.signal(self.sig, handler)
        return self

    def __exit__(self, type, value, tb):
        self.release()

    def release(self):
        if self.released:
            return False
        signal.signal(self.sig, self.original_handler)
        self.released = True
        return True


if __name__ == "__main__":
    import random
    import json
    import matplotlib.pyplot as plt
    import numpy as np

    user_data = USER_DATA.copy()

    try:
        fh = open('vals.json', 'r')
        vals = json.loads(fh.read())
        fh.close()
    except IOError:
        vals = []

    with GracefulInterruptHandler() as h:
        for i in xrange(9000000000):
            for k, v in user_data.items():
                user_data[k] = random.choice([0.25, 0.95, 0.99, 1.0])

            vals.append(query_cpt(user_data))
            #print "%.3f" % vals[-1], "(%.3f" % min(vals), "to", "%.3f)" % max(vals)
            if float(i) % 50 == 0:
                print len(vals)
            if h.interrupted:
                break

    with open('vals.json', 'w') as fh:
        fh.write(json.dumps(vals))

    mu, sigma = 100, 15
    hist, bins = np.histogram(vals, bins=20)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()

