from bayesian.bbn import build_bbn
########################## REMOVE ME ????
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dst')))
#########################################
from bbn.cpt.xls import xls2cptdict

def query_cpt(CPT, user_data=None, output_nodes=('suitability',)):

    def f_suitability(landscape, socio_economic, site, suitability):
        cpt = {
             # Unsuitable, Unsuitable, Suitable
            (False, False, True): CPT['suitability'][('Unsuitable', 'Unsuitable', 'Suitable')],

            # Suitable, Suitable, Unsuitable
            (True, True, False): CPT['suitability'][('Suitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Suitable, Unsuitable
            (False, True, False): CPT['suitability'][('Unsuitable', 'Suitable', 'Unsuitable')],

            # Suitable, Unsuitable, Suitable
            (True, False, True): CPT['suitability'][('Suitable', 'Unsuitable', 'Suitable')],

            # Suitable, Suitable, Suitable
            (True, True, True): CPT['suitability'][('Suitable', 'Suitable', 'Suitable')],

            # Unsuitable, Unsuitable, Unsuitable
            (False, False, False): CPT['suitability'][('Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Unsuitable, Unsuitable
            (True, False, False): CPT['suitability'][('Suitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Suitable, Suitable
            (False, True, True): CPT['suitability'][('Unsuitable', 'Suitable', 'Suitable')],


        }
        p = cpt[(landscape, socio_economic, site)]
        if suitability:
            return p
        else:
            return 1.0 - p
    
    def f_landscape(geomorphic_controls, abiotic_conditions, floodplain_characteristics, conservation_value, landscape):
        cpt = {
             # Unsuitable, Suitable, Unsuitable, Unsuitable
            (False, True, False, False): CPT['Landscape'][('Unsuitable', 'Suitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Unsuitable, Suitable, Unsuitable
            (True, False, True, False): CPT['Landscape'][('Suitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Suitable, Unsuitable, Unsuitable, Unsuitable
            (True, False, False, False): CPT['Landscape'][('Suitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Unsuitable, Suitable
            (False, False, False, True): CPT['Landscape'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable, Suitable
            (False, True, True, True): CPT['Landscape'][('Unsuitable', 'Suitable', 'Suitable', 'Suitable')],

            # Suitable, Suitable, Suitable, Suitable
            (True, True, True, True): CPT['Landscape'][('Suitable', 'Suitable', 'Suitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable, Unsuitable
            (False, True, True, False): CPT['Landscape'][('Unsuitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Suitable, Suitable, Suitable, Unsuitable
            (True, True, True, False): CPT['Landscape'][('Suitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Suitable, Unsuitable, Unsuitable, Suitable
            (True, False, False, True): CPT['Landscape'][('Suitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Unsuitable, Suitable, Unsuitable
            (False, False, True, False): CPT['Landscape'][('Unsuitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Unsuitable, Unsuitable
            (False, False, False, False): CPT['Landscape'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Suitable, Unsuitable, Suitable
            (False, True, False, True): CPT['Landscape'][('Unsuitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Unsuitable, Suitable, Suitable
            (False, False, True, True): CPT['Landscape'][('Unsuitable', 'Unsuitable', 'Suitable', 'Suitable')],

            # Suitable, Unsuitable, Suitable, Suitable
            (True, False, True, True): CPT['Landscape'][('Suitable', 'Unsuitable', 'Suitable', 'Suitable')],

            # Suitable, Suitable, Unsuitable, Suitable
            (True, True, False, True): CPT['Landscape'][('Suitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Suitable, Suitable, Unsuitable, Unsuitable
            (True, True, False, False): CPT['Landscape'][('Suitable', 'Suitable', 'Unsuitable', 'Unsuitable')],


        }
        p = cpt[(geomorphic_controls, abiotic_conditions, floodplain_characteristics, conservation_value)]
        if landscape:
            return p
        else:
            return 1.0 - p
    
    def f_geomorphic_controls(infrastructure_constraints, substrate, material_availability, channel_mobility, geomorphic_controls):
        cpt = {
             # No restrictions, Unsuitable, Unavailable, Mobile
            (True, False, False, True): CPT['Geomorphic Controls'][('No restrictions', 'Unsuitable', 'Unavailable', 'Mobile')],

            # Unsuitable, Suitable, Unavailable, Mobile
            (False, True, False, True): CPT['Geomorphic Controls'][('Unsuitable', 'Suitable', 'Unavailable', 'Mobile')],

            # Unsuitable, Unsuitable, Unavailable, Not mobile
            (False, False, False, False): CPT['Geomorphic Controls'][('Unsuitable', 'Unsuitable', 'Unavailable', 'Not mobile')],

            # Unsuitable, Suitable, Unavailable, Not mobile
            (False, True, False, False): CPT['Geomorphic Controls'][('Unsuitable', 'Suitable', 'Unavailable', 'Not mobile')],

            # Unsuitable, Unsuitable, Available, Not mobile
            (False, False, True, False): CPT['Geomorphic Controls'][('Unsuitable', 'Unsuitable', 'Available', 'Not mobile')],

            # Unsuitable, Unsuitable, Available, Mobile
            (False, False, True, True): CPT['Geomorphic Controls'][('Unsuitable', 'Unsuitable', 'Available', 'Mobile')],

            # No restrictions, Unsuitable, Unavailable, Not mobile
            (True, False, False, False): CPT['Geomorphic Controls'][('No restrictions', 'Unsuitable', 'Unavailable', 'Not mobile')],

            # No restrictions, Unsuitable, Available, Not mobile
            (True, False, True, False): CPT['Geomorphic Controls'][('No restrictions', 'Unsuitable', 'Available', 'Not mobile')],

            # No restrictions, Suitable, Unavailable, Mobile
            (True, True, False, True): CPT['Geomorphic Controls'][('No restrictions', 'Suitable', 'Unavailable', 'Mobile')],

            # No restrictions, Suitable, Available, Not mobile
            (True, True, True, False): CPT['Geomorphic Controls'][('No restrictions', 'Suitable', 'Available', 'Not mobile')],

            # Unsuitable, Suitable, Available, Mobile
            (False, True, True, True): CPT['Geomorphic Controls'][('Unsuitable', 'Suitable', 'Available', 'Mobile')],

            # Unsuitable, Suitable, Available, Not mobile
            (False, True, True, False): CPT['Geomorphic Controls'][('Unsuitable', 'Suitable', 'Available', 'Not mobile')],

            # Unsuitable, Unsuitable, Unavailable, Mobile
            (False, False, False, True): CPT['Geomorphic Controls'][('Unsuitable', 'Unsuitable', 'Unavailable', 'Mobile')],

            # No restrictions, Unsuitable, Available, Mobile
            (True, False, True, True): CPT['Geomorphic Controls'][('No restrictions', 'Unsuitable', 'Available', 'Mobile')],

            # No restrictions, Suitable, Available, Mobile
            (True, True, True, True): CPT['Geomorphic Controls'][('No restrictions', 'Suitable', 'Available', 'Mobile')],

            # No restrictions, Suitable, Unavailable, Not mobile
            (True, True, False, False): CPT['Geomorphic Controls'][('No restrictions', 'Suitable', 'Unavailable', 'Not mobile')],


        }
        p = cpt[(infrastructure_constraints, substrate, material_availability, channel_mobility)]
        if geomorphic_controls:
            return p
        else:
            return 1.0 - p
    
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
    
    def f_abiotic_conditions(connectivity_barriers, water_quality, abiotic_conditions):
        cpt = {
             # Connected, High Quality
            (True, True): CPT['Abiotic conditions'][('Connected', 'High Quality')],

            # Disconnected, Low Quality
            (False, False): CPT['Abiotic conditions'][('Disconnected', 'Low Quality')],

            # Connected, Low Quality
            (True, False): CPT['Abiotic conditions'][('Connected', 'Low Quality')],

            # Disconnected, High Quality
            (False, True): CPT['Abiotic conditions'][('Disconnected', 'High Quality')],


        }
        p = cpt[(connectivity_barriers, water_quality)]
        if abiotic_conditions:
            return p
        else:
            return 1.0 - p
    
    def f_connectivity_barriers(upstream, on_property, downstream, connectivity_barriers):
        cpt = {
             # Connected, Connected, Connected
            (True, True, True): CPT['Connectivity barriers'][('Connected', 'Connected', 'Connected')],

            # Connected, Disconnected, Connected
            (True, False, True): CPT['Connectivity barriers'][('Connected', 'Disconnected', 'Connected')],

            # Disconnected, Connected, Disconnected
            (False, True, False): CPT['Connectivity barriers'][('Disconnected', 'Connected', 'Disconnected')],

            # Connected, Connected, Disconnected
            (True, True, False): CPT['Connectivity barriers'][('Connected', 'Connected', 'Disconnected')],

            # Disconnected, Disconnected, Connected
            (False, False, True): CPT['Connectivity barriers'][('Disconnected', 'Disconnected', 'Connected')],

            # Connected, Disconnected, Disconnected
            (True, False, False): CPT['Connectivity barriers'][('Connected', 'Disconnected', 'Disconnected')],

            # Disconnected, Disconnected, Disconnected
            (False, False, False): CPT['Connectivity barriers'][('Disconnected', 'Disconnected', 'Disconnected')],

            # Disconnected, Connected, Connected
            (False, True, True): CPT['Connectivity barriers'][('Disconnected', 'Connected', 'Connected')],


        }
        p = cpt[(upstream, on_property, downstream)]
        if connectivity_barriers:
            return p
        else:
            return 1.0 - p
    
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
    
    def f_downstream(downstream):
        if downstream:
            return prob['downstream']
        else:
            return 1.0 - prob['downstream']
    
    def f_water_quality(water_quality):
        if water_quality:
            return prob['water_quality']
        else:
            return 1.0 - prob['water_quality']
    
    def f_floodplain_characteristics(gradient, width, location_in_floodplain, within_x_year_floodplain, floodplain_characteristics):
        cpt = {
             # Unsuitable, Suitable, Ineffective, Outside
            (False, True, False, False): CPT['Floodplain characteristic'][('Unsuitable', 'Suitable', 'Ineffective', 'Outside')],

            # Unsuitable, Unsuitable, Ineffective, Outside
            (False, False, False, False): CPT['Floodplain characteristic'][('Unsuitable', 'Unsuitable', 'Ineffective', 'Outside')],

            # Suitable, Unsuitable, Strategic, Outside
            (True, False, True, False): CPT['Floodplain characteristic'][('Suitable', 'Unsuitable', 'Strategic', 'Outside')],

            # Suitable, Suitable, Strategic, Within
            (True, True, True, True): CPT['Floodplain characteristic'][('Suitable', 'Suitable', 'Strategic', 'Within')],

            # Suitable, Suitable, Strategic, Outside
            (True, True, True, False): CPT['Floodplain characteristic'][('Suitable', 'Suitable', 'Strategic', 'Outside')],

            # Suitable, Unsuitable, Strategic, Within
            (True, False, True, True): CPT['Floodplain characteristic'][('Suitable', 'Unsuitable', 'Strategic', 'Within')],

            # Suitable, Unsuitable, Ineffective, Outside
            (True, False, False, False): CPT['Floodplain characteristic'][('Suitable', 'Unsuitable', 'Ineffective', 'Outside')],

            # Suitable, Unsuitable, Ineffective, Within
            (True, False, False, True): CPT['Floodplain characteristic'][('Suitable', 'Unsuitable', 'Ineffective', 'Within')],

            # Unsuitable, Suitable, Strategic, Outside
            (False, True, True, False): CPT['Floodplain characteristic'][('Unsuitable', 'Suitable', 'Strategic', 'Outside')],

            # Unsuitable, Unsuitable, Strategic, Within
            (False, False, True, True): CPT['Floodplain characteristic'][('Unsuitable', 'Unsuitable', 'Strategic', 'Within')],

            # Unsuitable, Unsuitable, Ineffective, Within
            (False, False, False, True): CPT['Floodplain characteristic'][('Unsuitable', 'Unsuitable', 'Ineffective', 'Within')],

            # Unsuitable, Suitable, Ineffective, Within
            (False, True, False, True): CPT['Floodplain characteristic'][('Unsuitable', 'Suitable', 'Ineffective', 'Within')],

            # Suitable, Suitable, Ineffective, Within
            (True, True, False, True): CPT['Floodplain characteristic'][('Suitable', 'Suitable', 'Ineffective', 'Within')],

            # Suitable, Suitable, Ineffective, Outside
            (True, True, False, False): CPT['Floodplain characteristic'][('Suitable', 'Suitable', 'Ineffective', 'Outside')],

            # Unsuitable, Unsuitable, Strategic, Outside
            (False, False, True, False): CPT['Floodplain characteristic'][('Unsuitable', 'Unsuitable', 'Strategic', 'Outside')],

            # Unsuitable, Suitable, Strategic, Within
            (False, True, True, True): CPT['Floodplain characteristic'][('Unsuitable', 'Suitable', 'Strategic', 'Within')],


        }
        p = cpt[(gradient, width, location_in_floodplain, within_x_year_floodplain)]
        if floodplain_characteristics:
            return p
        else:
            return 1.0 - p
    
    def f_gradient(gradient):
        if gradient:
            return prob['gradient']
        else:
            return 1.0 - prob['gradient']
    
    def f_width(width):
        if width:
            return prob['width']
        else:
            return 1.0 - prob['width']
    
    def f_location_in_floodplain(location_in_floodplain):
        if location_in_floodplain:
            return prob['location_in_floodplain']
        else:
            return 1.0 - prob['location_in_floodplain']
    
    def f_within_x_year_floodplain(within_x_year_floodplain):
        if within_x_year_floodplain:
            return prob['within_x_year_floodplain']
        else:
            return 1.0 - prob['within_x_year_floodplain']
    
    def f_conservation_value(biotic_conditions, relationship_to_protected_areas, identified_in_conservation_plan, conservation_value):
        cpt = {
             # Suitable, Disconnected, Not Identified
            (True, False, False): CPT['Conservation value'][('Suitable', 'Disconnected', 'Not Identified')],

            # Suitable, Connected, Identified
            (True, True, True): CPT['Conservation value'][('Suitable', 'Connected', 'Identified')],

            # Unsuitable, Connected, Identified
            (False, True, True): CPT['Conservation value'][('Unsuitable', 'Connected', 'Identified')],

            # Suitable, Disconnected, Identified
            (True, False, True): CPT['Conservation value'][('Suitable', 'Disconnected', 'Identified')],

            # Unsuitable, Disconnected, Not Identified
            (False, False, False): CPT['Conservation value'][('Unsuitable', 'Disconnected', 'Not Identified')],

            # Unsuitable, Connected, Not Identified
            (False, True, False): CPT['Conservation value'][('Unsuitable', 'Connected', 'Not Identified')],

            # Suitable, Connected, Not Identified
            (True, True, False): CPT['Conservation value'][('Suitable', 'Connected', 'Not Identified')],

            # Unsuitable, Disconnected, Identified
            (False, False, True): CPT['Conservation value'][('Unsuitable', 'Disconnected', 'Identified')],


        }
        p = cpt[(biotic_conditions, relationship_to_protected_areas, identified_in_conservation_plan)]
        if conservation_value:
            return p
        else:
            return 1.0 - p
    
    def f_biotic_conditions(habitat_features, intact_floodplain_forest, species_of_interest, biotic_conditions):
        cpt = {
             # Suitable, Intact, Present
            (True, True, True): CPT['Biotic conditions'][('Suitable', 'Intact', 'Present')],

            # Unsuitable, Missing, Not Present
            (False, False, False): CPT['Biotic conditions'][('Unsuitable', 'Missing', 'Not Present')],

            # Suitable, Missing, Not Present
            (True, False, False): CPT['Biotic conditions'][('Suitable', 'Missing', 'Not Present')],

            # Suitable, Intact, Not Present
            (True, True, False): CPT['Biotic conditions'][('Suitable', 'Intact', 'Not Present')],

            # Unsuitable, Intact, Not Present
            (False, True, False): CPT['Biotic conditions'][('Unsuitable', 'Intact', 'Not Present')],

            # Suitable, Missing, Present
            (True, False, True): CPT['Biotic conditions'][('Suitable', 'Missing', 'Present')],

            # Unsuitable, Missing, Present
            (False, False, True): CPT['Biotic conditions'][('Unsuitable', 'Missing', 'Present')],

            # Unsuitable, Intact, Present
            (False, True, True): CPT['Biotic conditions'][('Unsuitable', 'Intact', 'Present')],


        }
        p = cpt[(habitat_features, intact_floodplain_forest, species_of_interest)]
        if biotic_conditions:
            return p
        else:
            return 1.0 - p
    
    def f_habitat_features(habitat_features):
        if habitat_features:
            return prob['habitat_features']
        else:
            return 1.0 - prob['habitat_features']
    
    def f_intact_floodplain_forest(intact_floodplain_forest):
        if intact_floodplain_forest:
            return prob['intact_floodplain_forest']
        else:
            return 1.0 - prob['intact_floodplain_forest']
    
    def f_species_of_interest(species_of_interest):
        if species_of_interest:
            return prob['species_of_interest']
        else:
            return 1.0 - prob['species_of_interest']
    
    def f_relationship_to_protected_areas(relationship_to_protected_areas):
        if relationship_to_protected_areas:
            return prob['relationship_to_protected_areas']
        else:
            return 1.0 - prob['relationship_to_protected_areas']
    
    def f_identified_in_conservation_plan(identified_in_conservation_plan):
        if identified_in_conservation_plan:
            return prob['identified_in_conservation_plan']
        else:
            return 1.0 - prob['identified_in_conservation_plan']
    
    def f_socio_economic(threats_to_other_areas_or_permittability, cost_benefit, socio_economic):
        cpt = {
             # Threatened, Costly
            (False, False): CPT['Socio-Economic'][('Threatened', 'Costly')],

            # Threatened, Beneficial
            (False, True): CPT['Socio-Economic'][('Threatened', 'Beneficial')],

            # No threats, Costly
            (True, False): CPT['Socio-Economic'][('No threats', 'Costly')],

            # No threats, Beneficial
            (True, True): CPT['Socio-Economic'][('No threats', 'Beneficial')],


        }
        p = cpt[(threats_to_other_areas_or_permittability, cost_benefit)]
        if socio_economic:
            return p
        else:
            return 1.0 - p
    
    def f_threats_to_other_areas_or_permittability(water_rights, surrounding_land_use, surrounding_ownership, infrastructure, threats_to_other_areas_or_permittability):
        cpt = {
             # Threatened, Ammenable, Ammenable, Threatened
            (False, True, True, False): CPT['Threats to other areas or'][('Threatened', 'Ammenable', 'Ammenable', 'Threatened')],

            # Threatened, Unfriendly, Ammenable, No threats
            (False, False, True, True): CPT['Threats to other areas or'][('Threatened', 'Unfriendly', 'Ammenable', 'No threats')],

            # No threats, Ammenable, Ammenable, No threats
            (True, True, True, True): CPT['Threats to other areas or'][('No threats', 'Ammenable', 'Ammenable', 'No threats')],

            # Threatened, Unfriendly, Unfriendly, No threats
            (False, False, False, True): CPT['Threats to other areas or'][('Threatened', 'Unfriendly', 'Unfriendly', 'No threats')],

            # No threats, Ammenable, Ammenable, Threatened
            (True, True, True, False): CPT['Threats to other areas or'][('No threats', 'Ammenable', 'Ammenable', 'Threatened')],

            # Threatened, Unfriendly, Ammenable, Threatened
            (False, False, True, False): CPT['Threats to other areas or'][('Threatened', 'Unfriendly', 'Ammenable', 'Threatened')],

            # No threats, Ammenable, Unfriendly, Threatened
            (True, True, False, False): CPT['Threats to other areas or'][('No threats', 'Ammenable', 'Unfriendly', 'Threatened')],

            # No threats, Ammenable, Unfriendly, No threats
            (True, True, False, True): CPT['Threats to other areas or'][('No threats', 'Ammenable', 'Unfriendly', 'No threats')],

            # Threatened, Ammenable, Unfriendly, Threatened
            (False, True, False, False): CPT['Threats to other areas or'][('Threatened', 'Ammenable', 'Unfriendly', 'Threatened')],

            # No threats, Unfriendly, Ammenable, No threats
            (True, False, True, True): CPT['Threats to other areas or'][('No threats', 'Unfriendly', 'Ammenable', 'No threats')],

            # Threatened, Unfriendly, Unfriendly, Threatened
            (False, False, False, False): CPT['Threats to other areas or'][('Threatened', 'Unfriendly', 'Unfriendly', 'Threatened')],

            # No threats, Unfriendly, Unfriendly, No threats
            (True, False, False, True): CPT['Threats to other areas or'][('No threats', 'Unfriendly', 'Unfriendly', 'No threats')],

            # Threatened, Ammenable, Ammenable, No threats
            (False, True, True, True): CPT['Threats to other areas or'][('Threatened', 'Ammenable', 'Ammenable', 'No threats')],

            # No threats, Unfriendly, Ammenable, Threatened
            (True, False, True, False): CPT['Threats to other areas or'][('No threats', 'Unfriendly', 'Ammenable', 'Threatened')],

            # Threatened, Ammenable, Unfriendly, No threats
            (False, True, False, True): CPT['Threats to other areas or'][('Threatened', 'Ammenable', 'Unfriendly', 'No threats')],

            # No threats, Unfriendly, Unfriendly, Threatened
            (True, False, False, False): CPT['Threats to other areas or'][('No threats', 'Unfriendly', 'Unfriendly', 'Threatened')],


        }
        p = cpt[(water_rights, surrounding_land_use, surrounding_ownership, infrastructure)]
        if threats_to_other_areas_or_permittability:
            return p
        else:
            return 1.0 - p
    
    def f_water_rights(water_rights):
        if water_rights:
            return prob['water_rights']
        else:
            return 1.0 - prob['water_rights']
    
    def f_surrounding_land_use(surrounding_land_use):
        if surrounding_land_use:
            return prob['surrounding_land_use']
        else:
            return 1.0 - prob['surrounding_land_use']
    
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
    
    def f_cost_benefit(contamination_or_hazardous_waste, property_value, public_perception, cost_benefit):
        cpt = {
             # Contaminated, Costly, Unfavorable
            (False, False, False): CPT['Cost benefit'][('Contaminated', 'Costly', 'Unfavorable')],

            # Clean, Good Deal, Unfavorable
            (True, True, False): CPT['Cost benefit'][('Clean', 'Good Deal', 'Unfavorable')],

            # Clean, Good Deal, Supportive
            (True, True, True): CPT['Cost benefit'][('Clean', 'Good Deal', 'Supportive')],

            # Contaminated, Good Deal, Unfavorable
            (False, True, False): CPT['Cost benefit'][('Contaminated', 'Good Deal', 'Unfavorable')],

            # Clean, Costly, Unfavorable
            (True, False, False): CPT['Cost benefit'][('Clean', 'Costly', 'Unfavorable')],

            # Clean, Costly, Supportive
            (True, False, True): CPT['Cost benefit'][('Clean', 'Costly', 'Supportive')],

            # Contaminated, Costly, Supportive
            (False, False, True): CPT['Cost benefit'][('Contaminated', 'Costly', 'Supportive')],

            # Contaminated, Good Deal, Supportive
            (False, True, True): CPT['Cost benefit'][('Contaminated', 'Good Deal', 'Supportive')],


        }
        p = cpt[(contamination_or_hazardous_waste, property_value, public_perception)]
        if cost_benefit:
            return p
        else:
            return 1.0 - p
    
    def f_contamination_or_hazardous_waste(contamination_or_hazardous_waste):
        if contamination_or_hazardous_waste:
            return prob['contamination_or_hazardous_waste']
        else:
            return 1.0 - prob['contamination_or_hazardous_waste']
    
    def f_property_value(property_value):
        if property_value:
            return prob['property_value']
        else:
            return 1.0 - prob['property_value']
    
    def f_public_perception(public_perception):
        if public_perception:
            return prob['public_perception']
        else:
            return 1.0 - prob['public_perception']
    
    def f_site(pit_restorability, practical_property_level_restorability, site):
        cpt = {
             # Suitable, Unsuitable
            (True, False): CPT['Site'][('Suitable', 'Unsuitable')],

            # Suitable, Suitable
            (True, True): CPT['Site'][('Suitable', 'Suitable')],

            # Unsuitable, Suitable
            (False, True): CPT['Site'][('Unsuitable', 'Suitable')],

            # Unsuitable, Unsuitable
            (False, False): CPT['Site'][('Unsuitable', 'Unsuitable')],


        }
        p = cpt[(pit_restorability, practical_property_level_restorability)]
        if site:
            return p
        else:
            return 1.0 - p
    
    def f_pit_restorability(practical_restorability, pit_geometry, water_quality_threat, pit_restorability):
        cpt = {
             # Unsuitable, Unsuitable, Suitable
            (False, False, True): CPT['Pit restorability'][('Unsuitable', 'Unsuitable', 'Suitable')],

            # Suitable, Suitable, Unsuitable
            (True, True, False): CPT['Pit restorability'][('Suitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Suitable, Unsuitable
            (False, True, False): CPT['Pit restorability'][('Unsuitable', 'Suitable', 'Unsuitable')],

            # Suitable, Unsuitable, Suitable
            (True, False, True): CPT['Pit restorability'][('Suitable', 'Unsuitable', 'Suitable')],

            # Suitable, Suitable, Suitable
            (True, True, True): CPT['Pit restorability'][('Suitable', 'Suitable', 'Suitable')],

            # Unsuitable, Unsuitable, Unsuitable
            (False, False, False): CPT['Pit restorability'][('Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Unsuitable, Unsuitable
            (True, False, False): CPT['Pit restorability'][('Suitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Suitable, Suitable
            (False, True, True): CPT['Pit restorability'][('Unsuitable', 'Suitable', 'Suitable')],


        }
        p = cpt[(practical_restorability, pit_geometry, water_quality_threat)]
        if pit_restorability:
            return p
        else:
            return 1.0 - p
    
    def f_practical_restorability(pit_adjacent_levees, bedrock_constraints, adjacent_river_depth, slope_distance_to_river, practical_restorability):
        cpt = {
             # Unsuitable, Suitable, Unsuitable, Unsuitable
            (False, True, False, False): CPT['Practical restorability'][('Unsuitable', 'Suitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Unsuitable, Suitable, Unsuitable
            (True, False, True, False): CPT['Practical restorability'][('Suitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Suitable, Unsuitable, Unsuitable, Unsuitable
            (True, False, False, False): CPT['Practical restorability'][('Suitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Unsuitable, Suitable
            (False, False, False, True): CPT['Practical restorability'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable, Suitable
            (False, True, True, True): CPT['Practical restorability'][('Unsuitable', 'Suitable', 'Suitable', 'Suitable')],

            # Suitable, Suitable, Suitable, Suitable
            (True, True, True, True): CPT['Practical restorability'][('Suitable', 'Suitable', 'Suitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable, Unsuitable
            (False, True, True, False): CPT['Practical restorability'][('Unsuitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Suitable, Suitable, Suitable, Unsuitable
            (True, True, True, False): CPT['Practical restorability'][('Suitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Suitable, Unsuitable, Unsuitable, Suitable
            (True, False, False, True): CPT['Practical restorability'][('Suitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Unsuitable, Suitable, Unsuitable
            (False, False, True, False): CPT['Practical restorability'][('Unsuitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Unsuitable, Unsuitable
            (False, False, False, False): CPT['Practical restorability'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Suitable, Unsuitable, Suitable
            (False, True, False, True): CPT['Practical restorability'][('Unsuitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Unsuitable, Suitable, Suitable
            (False, False, True, True): CPT['Practical restorability'][('Unsuitable', 'Unsuitable', 'Suitable', 'Suitable')],

            # Suitable, Unsuitable, Suitable, Suitable
            (True, False, True, True): CPT['Practical restorability'][('Suitable', 'Unsuitable', 'Suitable', 'Suitable')],

            # Suitable, Suitable, Unsuitable, Suitable
            (True, True, False, True): CPT['Practical restorability'][('Suitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Suitable, Suitable, Unsuitable, Unsuitable
            (True, True, False, False): CPT['Practical restorability'][('Suitable', 'Suitable', 'Unsuitable', 'Unsuitable')],


        }
        p = cpt[(pit_adjacent_levees, bedrock_constraints, adjacent_river_depth, slope_distance_to_river)]
        if practical_restorability:
            return p
        else:
            return 1.0 - p
    
    def f_pit_adjacent_levees(pit_adjacent_levees):
        if pit_adjacent_levees:
            return prob['pit_adjacent_levees']
        else:
            return 1.0 - prob['pit_adjacent_levees']
    
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
    
    def f_slope_distance_to_river(slope_distance_to_river):
        if slope_distance_to_river:
            return prob['slope_distance_to_river']
        else:
            return 1.0 - prob['slope_distance_to_river']
    
    def f_pit_geometry(depth, surface_area, complexity, bank_slope, pit_geometry):
        cpt = {
             # Unsuitable, Suitable, Unsuitable, Unsuitable
            (False, True, False, False): CPT['Pit geometry'][('Unsuitable', 'Suitable', 'Unsuitable', 'Unsuitable')],

            # Suitable, Unsuitable, Suitable, Unsuitable
            (True, False, True, False): CPT['Pit geometry'][('Suitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Suitable, Unsuitable, Unsuitable, Unsuitable
            (True, False, False, False): CPT['Pit geometry'][('Suitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Unsuitable, Suitable
            (False, False, False, True): CPT['Pit geometry'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable, Suitable
            (False, True, True, True): CPT['Pit geometry'][('Unsuitable', 'Suitable', 'Suitable', 'Suitable')],

            # Suitable, Suitable, Suitable, Suitable
            (True, True, True, True): CPT['Pit geometry'][('Suitable', 'Suitable', 'Suitable', 'Suitable')],

            # Unsuitable, Suitable, Suitable, Unsuitable
            (False, True, True, False): CPT['Pit geometry'][('Unsuitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Suitable, Suitable, Suitable, Unsuitable
            (True, True, True, False): CPT['Pit geometry'][('Suitable', 'Suitable', 'Suitable', 'Unsuitable')],

            # Suitable, Unsuitable, Unsuitable, Suitable
            (True, False, False, True): CPT['Pit geometry'][('Suitable', 'Unsuitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Unsuitable, Suitable, Unsuitable
            (False, False, True, False): CPT['Pit geometry'][('Unsuitable', 'Unsuitable', 'Suitable', 'Unsuitable')],

            # Unsuitable, Unsuitable, Unsuitable, Unsuitable
            (False, False, False, False): CPT['Pit geometry'][('Unsuitable', 'Unsuitable', 'Unsuitable', 'Unsuitable')],

            # Unsuitable, Suitable, Unsuitable, Suitable
            (False, True, False, True): CPT['Pit geometry'][('Unsuitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Unsuitable, Unsuitable, Suitable, Suitable
            (False, False, True, True): CPT['Pit geometry'][('Unsuitable', 'Unsuitable', 'Suitable', 'Suitable')],

            # Suitable, Unsuitable, Suitable, Suitable
            (True, False, True, True): CPT['Pit geometry'][('Suitable', 'Unsuitable', 'Suitable', 'Suitable')],

            # Suitable, Suitable, Unsuitable, Suitable
            (True, True, False, True): CPT['Pit geometry'][('Suitable', 'Suitable', 'Unsuitable', 'Suitable')],

            # Suitable, Suitable, Unsuitable, Unsuitable
            (True, True, False, False): CPT['Pit geometry'][('Suitable', 'Suitable', 'Unsuitable', 'Unsuitable')],


        }
        p = cpt[(depth, surface_area, complexity, bank_slope)]
        if pit_geometry:
            return p
        else:
            return 1.0 - p
    
    def f_depth(depth):
        if depth:
            return prob['depth']
        else:
            return 1.0 - prob['depth']
    
    def f_surface_area(surface_area):
        if surface_area:
            return prob['surface_area']
        else:
            return 1.0 - prob['surface_area']
    
    def f_complexity(complexity):
        if complexity:
            return prob['complexity']
        else:
            return 1.0 - prob['complexity']
    
    def f_bank_slope(bank_slope):
        if bank_slope:
            return prob['bank_slope']
        else:
            return 1.0 - prob['bank_slope']
    
    def f_water_quality_threat(contamination, restorable_substrate, water_quality_threat):
        cpt = {
             # Suitable, Unsuitable
            (True, False): CPT['Water quality threat'][('Suitable', 'Unsuitable')],

            # Suitable, Suitable
            (True, True): CPT['Water quality threat'][('Suitable', 'Suitable')],

            # Unsuitable, Suitable
            (False, True): CPT['Water quality threat'][('Unsuitable', 'Suitable')],

            # Unsuitable, Unsuitable
            (False, False): CPT['Water quality threat'][('Unsuitable', 'Unsuitable')],


        }
        p = cpt[(contamination, restorable_substrate)]
        if water_quality_threat:
            return p
        else:
            return 1.0 - p
    
    def f_contamination(contamination):
        if contamination:
            return prob['contamination']
        else:
            return 1.0 - prob['contamination']
    
    def f_restorable_substrate(restorable_substrate):
        if restorable_substrate:
            return prob['restorable_substrate']
        else:
            return 1.0 - prob['restorable_substrate']
    
    def f_practical_property_level_restorability(continuing_property_access, site_accessibility, fill_material_availability, practical_property_level_restorability):
        cpt = {
             # Unsuitable, Accessible, Unavailable
            (False, True, False): CPT['Practical property-level '][('Unsuitable', 'Accessible', 'Unavailable')],

            # Unsuitable, Accessible, Available
            (False, True, True): CPT['Practical property-level '][('Unsuitable', 'Accessible', 'Available')],

            # Suitable, Accessible, Available
            (True, True, True): CPT['Practical property-level '][('Suitable', 'Accessible', 'Available')],

            # Suitable, Inaccessible, Available
            (True, False, True): CPT['Practical property-level '][('Suitable', 'Inaccessible', 'Available')],

            # Unsuitable, Inaccessible, Available
            (False, False, True): CPT['Practical property-level '][('Unsuitable', 'Inaccessible', 'Available')],

            # Suitable, Accessible, Unavailable
            (True, True, False): CPT['Practical property-level '][('Suitable', 'Accessible', 'Unavailable')],

            # Suitable, Inaccessible, Unavailable
            (True, False, False): CPT['Practical property-level '][('Suitable', 'Inaccessible', 'Unavailable')],

            # Unsuitable, Inaccessible, Unavailable
            (False, False, False): CPT['Practical property-level '][('Unsuitable', 'Inaccessible', 'Unavailable')],


        }
        p = cpt[(continuing_property_access, site_accessibility, fill_material_availability)]
        if practical_property_level_restorability:
            return p
        else:
            return 1.0 - p
    
    def f_continuing_property_access(continuing_property_access):
        if continuing_property_access:
            return prob['continuing_property_access']
        else:
            return 1.0 - prob['continuing_property_access']
    
    def f_site_accessibility(site_accessibility):
        if site_accessibility:
            return prob['site_accessibility']
        else:
            return 1.0 - prob['site_accessibility']
    
    def f_fill_material_availability(fill_material_availability):
        if fill_material_availability:
            return prob['fill_material_availability']
        else:
            return 1.0 - prob['fill_material_availability']
    
    levels = [True, False]
    net = build_bbn(
        f_suitability,
        f_landscape,
        f_geomorphic_controls,
        f_infrastructure_constraints,
        f_substrate,
        f_material_availability,
        f_channel_mobility,
        f_abiotic_conditions,
        f_connectivity_barriers,
        f_upstream,
        f_on_property,
        f_downstream,
        f_water_quality,
        f_floodplain_characteristics,
        f_gradient,
        f_width,
        f_location_in_floodplain,
        f_within_x_year_floodplain,
        f_conservation_value,
        f_biotic_conditions,
        f_habitat_features,
        f_intact_floodplain_forest,
        f_species_of_interest,
        f_relationship_to_protected_areas,
        f_identified_in_conservation_plan,
        f_socio_economic,
        f_threats_to_other_areas_or_permittability,
        f_water_rights,
        f_surrounding_land_use,
        f_surrounding_ownership,
        f_infrastructure,
        f_cost_benefit,
        f_contamination_or_hazardous_waste,
        f_property_value,
        f_public_perception,
        f_site,
        f_pit_restorability,
        f_practical_restorability,
        f_pit_adjacent_levees,
        f_bedrock_constraints,
        f_adjacent_river_depth,
        f_slope_distance_to_river,
        f_pit_geometry,
        f_depth,
        f_surface_area,
        f_complexity,
        f_bank_slope,
        f_water_quality_threat,
        f_contamination,
        f_restorable_substrate,
        f_practical_property_level_restorability,
        f_continuing_property_access,
        f_site_accessibility,
        f_fill_material_availability,

        # assume simple binary
        domains=dict(
            suitability = levels,
            landscape = levels,
            geomorphic_controls = levels,
            infrastructure_constraints = levels,
            substrate = levels,
            material_availability = levels,
            channel_mobility = levels,
            abiotic_conditions = levels,
            connectivity_barriers = levels,
            upstream = levels,
            on_property = levels,
            downstream = levels,
            water_quality = levels,
            floodplain_characteristics = levels,
            gradient = levels,
            width = levels,
            location_in_floodplain = levels,
            within_x_year_floodplain = levels,
            conservation_value = levels,
            biotic_conditions = levels,
            habitat_features = levels,
            intact_floodplain_forest = levels,
            species_of_interest = levels,
            relationship_to_protected_areas = levels,
            identified_in_conservation_plan = levels,
            socio_economic = levels,
            threats_to_other_areas_or_permittability = levels,
            water_rights = levels,
            surrounding_land_use = levels,
            surrounding_ownership = levels,
            infrastructure = levels,
            cost_benefit = levels,
            contamination_or_hazardous_waste = levels,
            property_value = levels,
            public_perception = levels,
            site = levels,
            pit_restorability = levels,
            practical_restorability = levels,
            pit_adjacent_levees = levels,
            bedrock_constraints = levels,
            adjacent_river_depth = levels,
            slope_distance_to_river = levels,
            pit_geometry = levels,
            depth = levels,
            surface_area = levels,
            complexity = levels,
            bank_slope = levels,
            water_quality_threat = levels,
            contamination = levels,
            restorable_substrate = levels,
            practical_property_level_restorability = levels,
            continuing_property_access = levels,
            site_accessibility = levels,
            fill_material_availability = levels,
        )
    )

    prob = dict(
    infrastructure_constraints = 1.0,
        substrate = 1.0,
        material_availability = 1.0,
        channel_mobility = 1.0,
        upstream = 1.0,
        on_property = 1.0,
        downstream = 1.0,
        water_quality = 1.0,
        gradient = 1.0,
        width = 1.0,
        location_in_floodplain = 1.0,
        within_x_year_floodplain = 1.0,
        habitat_features = 1.0,
        intact_floodplain_forest = 1.0,
        species_of_interest = 1.0,
        relationship_to_protected_areas = 1.0,
        identified_in_conservation_plan = 1.0,
        water_rights = 1.0,
        surrounding_land_use = 1.0,
        surrounding_ownership = 1.0,
        infrastructure = 1.0,
        contamination_or_hazardous_waste = 1.0,
        property_value = 1.0,
        public_perception = 1.0,
        pit_adjacent_levees = 1.0,
        bedrock_constraints = 1.0,
        adjacent_river_depth = 1.0,
        slope_distance_to_river = 1.0,
        depth = 1.0,
        surface_area = 1.0,
        complexity = 1.0,
        bank_slope = 1.0,
        contamination = 1.0,
        restorable_substrate = 1.0,
        continuing_property_access = 1.0,
        site_accessibility = 1.0,
        fill_material_availability = 1.0,)

    if not user_data:
        user_data = {}

    for k,v in user_data.items():
        if k in prob:
            prob[k] = v

    nq = net.query()
    res = []
    for onode in output_nodes:
        res.append(nq[(onode, True)])

    return res


if __name__ == "__main__":
    inputnodes = {
        'water_rights': 0.7,
        'surrounding_ownership': 1.0,
        'identified_in_conservation_plan': 1.0,
        'relationship_to_protected_areas': 1.0,
        'intact_floodplain_forest': 1.0,
        'habitat_features': 1.0,
        'species_of_interest': 1.0,}

    CPT = xls2cptdict('/home/mperry/src/floodplain-restoration/data/cpt_orig.xls')

    import random
    for i in range(10):
        k = random.choice(list(inputnodes.keys()))
        inputnodes[k] = random.random()

        val = query_cpt(CPT, inputnodes, output_nodes=(
            'suitability',
            'socio_economic',
            'site',
            'landscape')
        )
        print(val)

        