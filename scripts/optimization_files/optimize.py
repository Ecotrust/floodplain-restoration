from bayesian.bbn import build_bbn
from bayes_xls import read_cpt
import numpy as np

CPT = read_cpt('TNC_CPT_master.xls')

def query_cpt(user_data=None):
    if not user_data:
        user_data = {}

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
    

    def f_infrastructure(infrastructure):
        if infrastructure:
            return prob['infrastructure']
        else:
            return 1.0 - prob['infrastructure']
    

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
    

    def f_pit_geometry(depth, complexity, surface_area, bank_slope, pit_geometry):
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
        p = cpt[(depth, complexity, surface_area, bank_slope)]
        if pit_geometry:
            return p
        else:
            return 1.0 - p
    

    def f_depth(depth):
        if depth:
            return prob['depth']
        else:
            return 1.0 - prob['depth']
    

    def f_complexity(complexity):
        if complexity:
            return prob['complexity']
        else:
            return 1.0 - prob['complexity']
    

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
    

    def f_practical_restorability(slope_distance_to_river, bedrock_constraints, adjacent_river_depth, pit_adjacent_levees, practical_restorability):
        cpt = {
            # Unsuitable, Unsuitable, Unsuitable, Unsuitable
            (False, False, False, False): CPT['Practical restorability'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Suitable, Suitable, Unsuitable
            (False, True, True, False): CPT['Practical restorability'][('Unsuitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Suitable, Unsuitable, Unsuitable
            (False, True, False, False): CPT['Practical restorability'][('Unsuitable', 'Suitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Unsuitable, Unsuitable, Unsuitable
            (True, False, False, False): CPT['Practical restorability'][('Suitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Suitable, Suitable, Unsuitable
            (True, True, True, False): CPT['Practical restorability'][('Suitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Suitable, Suitable, Unsuitable, Unsuitable
            (True, True, False, False): CPT['Practical restorability'][('Suitable', 'Suitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Suitable, Unsuitable, Suitable
            (True, True, False, True): CPT['Practical restorability'][('Suitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Suitable, Suitable, Suitable, Suitable
            (True, True, True, True): CPT['Practical restorability'][('Suitable', 'Suitable', 'Suitable', 'Suitable')],

            # Suitable, Unsuitable, Unsuitable, Suitable
            (True, False, False, True): CPT['Practical restorability'][('Suitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Suitable, Unsuitable, Suitable, Unsuitable
            (True, False, True, False): CPT['Practical restorability'][('Suitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Suitable, Suitable
            (False, False, True, True): CPT['Practical restorability'][('Unsuitable', 'Unsuitable', 'Suitable', 'Suitable')],

            # Unsuitable, Unsuitable, Unsuitable, Suitable
            (False, False, False, True): CPT['Practical restorability'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable, Suitable
            (False, True, True, True): CPT['Practical restorability'][('Unsuitable', 'Suitable', 'Suitable', 'Suitable')],

            # Unsuitable, Unsuitable, Suitable, Unsuitable
            (False, False, True, False): CPT['Practical restorability'][('Unsuitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Suitable, Unsuitable, Suitable
            (False, True, False, True): CPT['Practical restorability'][('Unsuitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Suitable, Unsuitable, Suitable, Suitable
            (True, False, True, True): CPT['Practical restorability'][('Suitable', 'Unsuitable', 'Suitable', 'Suitable')],


        }
        p = cpt[(slope_distance_to_river, bedrock_constraints, adjacent_river_depth, pit_adjacent_levees)]
        if practical_restorability:
            return p
        else:
            return 1.0 - p
    

    def f_slope_distance_to_river(slope_distance_to_river):
        if slope_distance_to_river:
            return prob['slope_distance_to_river']
        else:
            return 1.0 - prob['slope_distance_to_river']
    

    def f_bedrock_constraints(bedrock_constraints):
        if bedrock_constraints:
            return prob['bedrock_constraints']
        else:
            return 1.0 - prob['bedrock_constraints']
    

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
    

    def f_biotic_conditions(intact_floodplain_forest, habitat_features, species_of_interest, biotic_conditions):
        cpt = {
            # Missing, Unsuitable, Not Present
            (False, False, False): CPT['Biotic conditions'][('Missing', 'Unsuitable', 'Not Present')],

            # Missing, Unsuitable, Present
            (False, False, True): CPT['Biotic conditions'][('Missing', 'Unsuitable', 'Present')],

            # Missing, Suitable, Not Present
            (False, True, False): CPT['Biotic conditions'][('Missing', 'Suitable', 'Not Present')],

            # Intact, Suitable, Present
            (True, True, True): CPT['Biotic conditions'][('Intact', 'Suitable', 'Present')],

            # Intact, Unsuitable, Not Present
            (True, False, False): CPT['Biotic conditions'][('Intact', 'Unsuitable', 'Not Present')],

            # Intact, Unsuitable, Present
            (True, False, True): CPT['Biotic conditions'][('Intact', 'Unsuitable', 'Present')],

            # Intact, Suitable, Not Present
            (True, True, False): CPT['Biotic conditions'][('Intact', 'Suitable', 'Not Present')],

            # Missing, Suitable, Present
            (False, True, True): CPT['Biotic conditions'][('Missing', 'Suitable', 'Present')],


        }
        p = cpt[(intact_floodplain_forest, habitat_features, species_of_interest)]
        if biotic_conditions:
            return p
        else:
            return 1.0 - p
    

    def f_intact_floodplain_forest(intact_floodplain_forest):
        if intact_floodplain_forest:
            return prob['intact_floodplain_forest']
        else:
            return 1.0 - prob['intact_floodplain_forest']
    

    def f_habitat_features(habitat_features):
        if habitat_features:
            return prob['habitat_features']
        else:
            return 1.0 - prob['habitat_features']
    

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
        f_surrounding_land_use,
        f_cost_benefit,
        f_property_value,
        f_contamination_or_hazardous_waste,
        f_public_perception,
        f_site,
        f_pit_restorability,
        f_pit_geometry,
        f_depth,
        f_complexity,
        f_surface_area,
        f_bank_slope,
        f_water_quality_threat,
        f_restorable_substrate,
        f_contamination,
        f_practical_restorability,
        f_slope_distance_to_river,
        f_bedrock_constraints,
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
        f_intact_floodplain_forest,
        f_habitat_features,
        f_species_of_interest,

        # assume simple binary
        domains=dict(
            suitability = levels,
            socio_economic = levels,
            threats_to_other_areas_or_permittability = levels,
            water_rights = levels,
            surrounding_ownership = levels,
            infrastructure = levels,
            surrounding_land_use = levels,
            cost_benefit = levels,
            property_value = levels,
            contamination_or_hazardous_waste = levels,
            public_perception = levels,
            site = levels,
            pit_restorability = levels,
            pit_geometry = levels,
            depth = levels,
            complexity = levels,
            surface_area = levels,
            bank_slope = levels,
            water_quality_threat = levels,
            restorable_substrate = levels,
            contamination = levels,
            practical_restorability = levels,
            slope_distance_to_river = levels,
            bedrock_constraints = levels,
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
            intact_floodplain_forest = levels,
            habitat_features = levels,
            species_of_interest = levels,
        )
    )

    prob = dict(
        water_rights = 1.0,
        surrounding_ownership = 1.0,
        infrastructure = 1.0,
        surrounding_land_use = 1.0,
        property_value = 1.0,
        contamination_or_hazardous_waste = 1.0,
        public_perception = 1.0,
        depth = 1.0,
        complexity = 1.0,
        surface_area = 1.0,
        bank_slope = 1.0,
        restorable_substrate = 1.0,
        contamination = 1.0,
        slope_distance_to_river = 1.0,
        bedrock_constraints = 1.0,
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
        habitat_features = 1.0,
        species_of_interest = 1.0,)

    for k,v in user_data.items():
        if prob.has_key(k):
            prob[k] = v

    #return net.query()[('suitability', True)]
    nq = net.query()
    return ( 
        nq[('socio_economic', True)],
        nq[('site', True)],
        nq[('landscape', True)],
    )

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

    orig_cpt = copy.deepcopy(CPT)
    best_error = float('inf')
    prev_cpt = copy.deepcopy(CPT)
    best_cpt = copy.deepcopy(CPT)
    stuck = 0

    training_sites = {}
    for training_site in glob.glob("training_sites/*.txt"):
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

    while stuck < 200:
        error = 0
        errors = []

        # move
        valid_move = False
        while not valid_move:
            var = random.choice(CPT.keys())
            cond = random.choice(CPT[var].keys())
            val = CPT[var][cond]
            newval = val + random.choice([0.05, -0.05])
            if newval >= 0.0 and newval <= 1.0:
                valid_move = True

        CPT[var][cond] = newval

        for training_site in glob.glob("training_sites/*.txt"):
            suitability = training_sites[training_site]

            prob = np.array(query_cpt(user_data))
            diff = prob - suitability
            errors.append(np.absolute(diff).sum())
            #print trainging_site, "Got", round(prob, 2), "Expected", suitability


        error = sum(errors)
        if error < best_error:
            best_error = error
            print "\naccept new lowest error:", best_error, # "stuck=", stuck
            best_cpt = copy.deepcopy(CPT)
            prev_cpt = copy.deepcopy(CPT)
            stuck = 0
        else:
            #print error, "reject it...", "best", best_error, hash(str(best_cpt))
            print ".", 
            CPT = copy.deepcopy(prev_cpt)
            stuck += 1

    import cPickle
    with open('optimal_cpt.pickle', 'w') as fh:
        fh.write(cPickle.dumps(best_cpt))

    import pprint
    pprint.pprint(best_cpt)
