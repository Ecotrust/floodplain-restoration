from bayesian.bbn import build_bbn
########################## REMOVE ME ????
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dst')))
#########################################
from bbn.cpt.xls import xls2cptdict

def query_cpt(CPT, user_data=None, output_nodes=('suitability',)):

    def f_suitability(socio_economic, site, landscape, suitability):
        cpt = {
             # Socio-Economic~Unsuitable, Site~Unsuitable, Landscape~Suitable
            (False, False, True): CPT['suitability'][('Socio-Economic~Unsuitable', 'Site~Unsuitable', 'Landscape~Suitable')],

            # Socio-Economic~Suitable, Site~Suitable, Landscape~Suitable
            (True, True, True): CPT['suitability'][('Socio-Economic~Suitable', 'Site~Suitable', 'Landscape~Suitable')],

            # Socio-Economic~Suitable, Site~Unsuitable, Landscape~Unsuitable
            (True, False, False): CPT['suitability'][('Socio-Economic~Suitable', 'Site~Unsuitable', 'Landscape~Unsuitable')],

            # Socio-Economic~Unsuitable, Site~Suitable, Landscape~Unsuitable
            (False, True, False): CPT['suitability'][('Socio-Economic~Unsuitable', 'Site~Suitable', 'Landscape~Unsuitable')],

            # Socio-Economic~Unsuitable, Site~Unsuitable, Landscape~Unsuitable
            (False, False, False): CPT['suitability'][('Socio-Economic~Unsuitable', 'Site~Unsuitable', 'Landscape~Unsuitable')],

            # Socio-Economic~Suitable, Site~Suitable, Landscape~Unsuitable
            (True, True, False): CPT['suitability'][('Socio-Economic~Suitable', 'Site~Suitable', 'Landscape~Unsuitable')],

            # Socio-Economic~Suitable, Site~Unsuitable, Landscape~Suitable
            (True, False, True): CPT['suitability'][('Socio-Economic~Suitable', 'Site~Unsuitable', 'Landscape~Suitable')],

            # Socio-Economic~Unsuitable, Site~Suitable, Landscape~Suitable
            (False, True, True): CPT['suitability'][('Socio-Economic~Unsuitable', 'Site~Suitable', 'Landscape~Suitable')],


        }
        p = cpt[(socio_economic, site, landscape)]
        if suitability:
            return p
        else:
            return 1.0 - p
    
    def f_socio_economic(cost_benefit, threats_to_other_areas_or_permittability, socio_economic):
        cpt = {
             # Cost benefit~Beneficial, Threats to other areas or Permittability~Threatened
            (True, False): CPT['Socio-Economic'][('Cost benefit~Beneficial', 'Threats to other areas or Permittability~Threatened')],

            # Cost benefit~Beneficial, Threats to other areas or Permittability~No threats
            (True, True): CPT['Socio-Economic'][('Cost benefit~Beneficial', 'Threats to other areas or Permittability~No threats')],

            # Cost benefit~Costly, Threats to other areas or Permittability~Threatened
            (False, False): CPT['Socio-Economic'][('Cost benefit~Costly', 'Threats to other areas or Permittability~Threatened')],

            # Cost benefit~Costly, Threats to other areas or Permittability~No threats
            (False, True): CPT['Socio-Economic'][('Cost benefit~Costly', 'Threats to other areas or Permittability~No threats')],


        }
        p = cpt[(cost_benefit, threats_to_other_areas_or_permittability)]
        if socio_economic:
            return p
        else:
            return 1.0 - p
    
    def f_cost_benefit(public_perception, property_value, contamination_or_hazardous_waste, cost_benefit):
        cpt = {
             # Public perception~Supportive, Property value~Costly, Contamination or Hazardous waste~Clean
            (True, False, True): CPT['Cost benefit'][('Public perception~Supportive', 'Property value~Costly', 'Contamination or Hazardous waste~Clean')],

            # Public perception~Supportive, Property value~Costly, Contamination or Hazardous waste~Contaminated
            (True, False, False): CPT['Cost benefit'][('Public perception~Supportive', 'Property value~Costly', 'Contamination or Hazardous waste~Contaminated')],

            # Public perception~Supportive, Property value~Good Deal, Contamination or Hazardous waste~Contaminated
            (True, True, False): CPT['Cost benefit'][('Public perception~Supportive', 'Property value~Good Deal', 'Contamination or Hazardous waste~Contaminated')],

            # Public perception~Unfavorable, Property value~Costly, Contamination or Hazardous waste~Clean
            (False, False, True): CPT['Cost benefit'][('Public perception~Unfavorable', 'Property value~Costly', 'Contamination or Hazardous waste~Clean')],

            # Public perception~Unfavorable, Property value~Good Deal, Contamination or Hazardous waste~Clean
            (False, True, True): CPT['Cost benefit'][('Public perception~Unfavorable', 'Property value~Good Deal', 'Contamination or Hazardous waste~Clean')],

            # Public perception~Unfavorable, Property value~Good Deal, Contamination or Hazardous waste~Contaminated
            (False, True, False): CPT['Cost benefit'][('Public perception~Unfavorable', 'Property value~Good Deal', 'Contamination or Hazardous waste~Contaminated')],

            # Public perception~Unfavorable, Property value~Costly, Contamination or Hazardous waste~Contaminated
            (False, False, False): CPT['Cost benefit'][('Public perception~Unfavorable', 'Property value~Costly', 'Contamination or Hazardous waste~Contaminated')],

            # Public perception~Supportive, Property value~Good Deal, Contamination or Hazardous waste~Clean
            (True, True, True): CPT['Cost benefit'][('Public perception~Supportive', 'Property value~Good Deal', 'Contamination or Hazardous waste~Clean')],


        }
        p = cpt[(public_perception, property_value, contamination_or_hazardous_waste)]
        if cost_benefit:
            return p
        else:
            return 1.0 - p
    
    def f_public_perception(public_perception):
        if public_perception:
            return prob['public_perception']
        else:
            return 1.0 - prob['public_perception']
    
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
    
    def f_threats_to_other_areas_or_permittability(surrounding_land_use, water_rights, surrounding_ownership, infrastructure, threats_to_other_areas_or_permittability):
        cpt = {
             # Surrounding land use~Ammenable, Water rights~Threatened, Surrounding ownership~Unfriendly, Infrastructure~Threatened
            (True, False, False, False): CPT['Threats to other areas or'][('Surrounding land use~Ammenable', 'Water rights~Threatened', 'Surrounding ownership~Unfriendly', 'Infrastructure~Threatened')],

            # Surrounding land use~Unfriendly, Water rights~No threats, Surrounding ownership~Ammenable, Infrastructure~No threats
            (False, True, True, True): CPT['Threats to other areas or'][('Surrounding land use~Unfriendly', 'Water rights~No threats', 'Surrounding ownership~Ammenable', 'Infrastructure~No threats')],

            # Surrounding land use~Ammenable, Water rights~No threats, Surrounding ownership~Unfriendly, Infrastructure~No threats
            (True, True, False, True): CPT['Threats to other areas or'][('Surrounding land use~Ammenable', 'Water rights~No threats', 'Surrounding ownership~Unfriendly', 'Infrastructure~No threats')],

            # Surrounding land use~Unfriendly, Water rights~Threatened, Surrounding ownership~Ammenable, Infrastructure~Threatened
            (False, False, True, False): CPT['Threats to other areas or'][('Surrounding land use~Unfriendly', 'Water rights~Threatened', 'Surrounding ownership~Ammenable', 'Infrastructure~Threatened')],

            # Surrounding land use~Ammenable, Water rights~Threatened, Surrounding ownership~Ammenable, Infrastructure~Threatened
            (True, False, True, False): CPT['Threats to other areas or'][('Surrounding land use~Ammenable', 'Water rights~Threatened', 'Surrounding ownership~Ammenable', 'Infrastructure~Threatened')],

            # Surrounding land use~Unfriendly, Water rights~Threatened, Surrounding ownership~Unfriendly, Infrastructure~Threatened
            (False, False, False, False): CPT['Threats to other areas or'][('Surrounding land use~Unfriendly', 'Water rights~Threatened', 'Surrounding ownership~Unfriendly', 'Infrastructure~Threatened')],

            # Surrounding land use~Unfriendly, Water rights~No threats, Surrounding ownership~Ammenable, Infrastructure~Threatened
            (False, True, True, False): CPT['Threats to other areas or'][('Surrounding land use~Unfriendly', 'Water rights~No threats', 'Surrounding ownership~Ammenable', 'Infrastructure~Threatened')],

            # Surrounding land use~Unfriendly, Water rights~Threatened, Surrounding ownership~Ammenable, Infrastructure~No threats
            (False, False, True, True): CPT['Threats to other areas or'][('Surrounding land use~Unfriendly', 'Water rights~Threatened', 'Surrounding ownership~Ammenable', 'Infrastructure~No threats')],

            # Surrounding land use~Unfriendly, Water rights~Threatened, Surrounding ownership~Unfriendly, Infrastructure~No threats
            (False, False, False, True): CPT['Threats to other areas or'][('Surrounding land use~Unfriendly', 'Water rights~Threatened', 'Surrounding ownership~Unfriendly', 'Infrastructure~No threats')],

            # Surrounding land use~Ammenable, Water rights~No threats, Surrounding ownership~Ammenable, Infrastructure~Threatened
            (True, True, True, False): CPT['Threats to other areas or'][('Surrounding land use~Ammenable', 'Water rights~No threats', 'Surrounding ownership~Ammenable', 'Infrastructure~Threatened')],

            # Surrounding land use~Unfriendly, Water rights~No threats, Surrounding ownership~Unfriendly, Infrastructure~No threats
            (False, True, False, True): CPT['Threats to other areas or'][('Surrounding land use~Unfriendly', 'Water rights~No threats', 'Surrounding ownership~Unfriendly', 'Infrastructure~No threats')],

            # Surrounding land use~Ammenable, Water rights~Threatened, Surrounding ownership~Unfriendly, Infrastructure~No threats
            (True, False, False, True): CPT['Threats to other areas or'][('Surrounding land use~Ammenable', 'Water rights~Threatened', 'Surrounding ownership~Unfriendly', 'Infrastructure~No threats')],

            # Surrounding land use~Ammenable, Water rights~No threats, Surrounding ownership~Ammenable, Infrastructure~No threats
            (True, True, True, True): CPT['Threats to other areas or'][('Surrounding land use~Ammenable', 'Water rights~No threats', 'Surrounding ownership~Ammenable', 'Infrastructure~No threats')],

            # Surrounding land use~Ammenable, Water rights~No threats, Surrounding ownership~Unfriendly, Infrastructure~Threatened
            (True, True, False, False): CPT['Threats to other areas or'][('Surrounding land use~Ammenable', 'Water rights~No threats', 'Surrounding ownership~Unfriendly', 'Infrastructure~Threatened')],

            # Surrounding land use~Unfriendly, Water rights~No threats, Surrounding ownership~Unfriendly, Infrastructure~Threatened
            (False, True, False, False): CPT['Threats to other areas or'][('Surrounding land use~Unfriendly', 'Water rights~No threats', 'Surrounding ownership~Unfriendly', 'Infrastructure~Threatened')],

            # Surrounding land use~Ammenable, Water rights~Threatened, Surrounding ownership~Ammenable, Infrastructure~No threats
            (True, False, True, True): CPT['Threats to other areas or'][('Surrounding land use~Ammenable', 'Water rights~Threatened', 'Surrounding ownership~Ammenable', 'Infrastructure~No threats')],


        }
        p = cpt[(surrounding_land_use, water_rights, surrounding_ownership, infrastructure)]
        if threats_to_other_areas_or_permittability:
            return p
        else:
            return 1.0 - p
    
    def f_surrounding_land_use(surrounding_land_use):
        if surrounding_land_use:
            return prob['surrounding_land_use']
        else:
            return 1.0 - prob['surrounding_land_use']
    
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
    
    def f_site(practical_property_level_restorability, pit_restorability, site):
        cpt = {
             # Practical property-level restorability~Suitable, Pit restorability~Suitable
            (True, True): CPT['Site'][('Practical property-level restorability~Suitable', 'Pit restorability~Suitable')],

            # Practical property-level restorability~Suitable, Pit restorability~Unsuitable
            (True, False): CPT['Site'][('Practical property-level restorability~Suitable', 'Pit restorability~Unsuitable')],

            # Practical property-level restorability~Unsuitable, Pit restorability~Unsuitable
            (False, False): CPT['Site'][('Practical property-level restorability~Unsuitable', 'Pit restorability~Unsuitable')],

            # Practical property-level restorability~Unsuitable, Pit restorability~Suitable
            (False, True): CPT['Site'][('Practical property-level restorability~Unsuitable', 'Pit restorability~Suitable')],


        }
        p = cpt[(practical_property_level_restorability, pit_restorability)]
        if site:
            return p
        else:
            return 1.0 - p
    
    def f_practical_property_level_restorability(continuing_property_access, site_accessibility, fill_material_availability, practical_property_level_restorability):
        cpt = {
             # Continuing property access~Unsuitable, Site accessibility~Inaccessible, Fill material availability~Available
            (False, False, True): CPT['Practical property-level '][('Continuing property access~Unsuitable', 'Site accessibility~Inaccessible', 'Fill material availability~Available')],

            # Continuing property access~Suitable, Site accessibility~Inaccessible, Fill material availability~Unavailable
            (True, False, False): CPT['Practical property-level '][('Continuing property access~Suitable', 'Site accessibility~Inaccessible', 'Fill material availability~Unavailable')],

            # Continuing property access~Unsuitable, Site accessibility~Inaccessible, Fill material availability~Unavailable
            (False, False, False): CPT['Practical property-level '][('Continuing property access~Unsuitable', 'Site accessibility~Inaccessible', 'Fill material availability~Unavailable')],

            # Continuing property access~Suitable, Site accessibility~Accessible, Fill material availability~Available
            (True, True, True): CPT['Practical property-level '][('Continuing property access~Suitable', 'Site accessibility~Accessible', 'Fill material availability~Available')],

            # Continuing property access~Unsuitable, Site accessibility~Accessible, Fill material availability~Available
            (False, True, True): CPT['Practical property-level '][('Continuing property access~Unsuitable', 'Site accessibility~Accessible', 'Fill material availability~Available')],

            # Continuing property access~Unsuitable, Site accessibility~Accessible, Fill material availability~Unavailable
            (False, True, False): CPT['Practical property-level '][('Continuing property access~Unsuitable', 'Site accessibility~Accessible', 'Fill material availability~Unavailable')],

            # Continuing property access~Suitable, Site accessibility~Accessible, Fill material availability~Unavailable
            (True, True, False): CPT['Practical property-level '][('Continuing property access~Suitable', 'Site accessibility~Accessible', 'Fill material availability~Unavailable')],

            # Continuing property access~Suitable, Site accessibility~Inaccessible, Fill material availability~Available
            (True, False, True): CPT['Practical property-level '][('Continuing property access~Suitable', 'Site accessibility~Inaccessible', 'Fill material availability~Available')],


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
    
    def f_pit_restorability(practical_restorability, water_quality_threat, pit_geometry, pit_restorability):
        cpt = {
             # Practical restorability~Unsuitable, Water quality threat~Suitable, Pit geometry~Suitable
            (False, True, True): CPT['Pit restorability'][('Practical restorability~Unsuitable', 'Water quality threat~Suitable', 'Pit geometry~Suitable')],

            # Practical restorability~Suitable, Water quality threat~Suitable, Pit geometry~Unsuitable
            (True, True, False): CPT['Pit restorability'][('Practical restorability~Suitable', 'Water quality threat~Suitable', 'Pit geometry~Unsuitable')],

            # Practical restorability~Unsuitable, Water quality threat~Unsuitable, Pit geometry~Unsuitable
            (False, False, False): CPT['Pit restorability'][('Practical restorability~Unsuitable', 'Water quality threat~Unsuitable', 'Pit geometry~Unsuitable')],

            # Practical restorability~Unsuitable, Water quality threat~Suitable, Pit geometry~Unsuitable
            (False, True, False): CPT['Pit restorability'][('Practical restorability~Unsuitable', 'Water quality threat~Suitable', 'Pit geometry~Unsuitable')],

            # Practical restorability~Suitable, Water quality threat~Suitable, Pit geometry~Suitable
            (True, True, True): CPT['Pit restorability'][('Practical restorability~Suitable', 'Water quality threat~Suitable', 'Pit geometry~Suitable')],

            # Practical restorability~Unsuitable, Water quality threat~Unsuitable, Pit geometry~Suitable
            (False, False, True): CPT['Pit restorability'][('Practical restorability~Unsuitable', 'Water quality threat~Unsuitable', 'Pit geometry~Suitable')],

            # Practical restorability~Suitable, Water quality threat~Unsuitable, Pit geometry~Unsuitable
            (True, False, False): CPT['Pit restorability'][('Practical restorability~Suitable', 'Water quality threat~Unsuitable', 'Pit geometry~Unsuitable')],

            # Practical restorability~Suitable, Water quality threat~Unsuitable, Pit geometry~Suitable
            (True, False, True): CPT['Pit restorability'][('Practical restorability~Suitable', 'Water quality threat~Unsuitable', 'Pit geometry~Suitable')],


        }
        p = cpt[(practical_restorability, water_quality_threat, pit_geometry)]
        if pit_restorability:
            return p
        else:
            return 1.0 - p
    
    def f_practical_restorability(pit_adjacent_levees, bedrock_constraints, adjacent_river_depth, slope_distance_to_river, practical_restorability):
        cpt = {
             # Pit-adjacent levees~Suitable, Bedrock Constraints~Unsuitable, Adjacent river depth~Suitable, Slope distance to river~Suitable
            (True, False, True, True): CPT['Practical restorability'][('Pit-adjacent levees~Suitable', 'Bedrock Constraints~Unsuitable', 'Adjacent river depth~Suitable', 'Slope distance to river~Suitable')],

            # Pit-adjacent levees~Unsuitable, Bedrock Constraints~Suitable, Adjacent river depth~Suitable, Slope distance to river~Unsuitable
            (False, True, True, False): CPT['Practical restorability'][('Pit-adjacent levees~Unsuitable', 'Bedrock Constraints~Suitable', 'Adjacent river depth~Suitable', 'Slope distance to river~Unsuitable')],

            # Pit-adjacent levees~Suitable, Bedrock Constraints~Suitable, Adjacent river depth~Unsuitable, Slope distance to river~Unsuitable
            (True, True, False, False): CPT['Practical restorability'][('Pit-adjacent levees~Suitable', 'Bedrock Constraints~Suitable', 'Adjacent river depth~Unsuitable', 'Slope distance to river~Unsuitable')],

            # Pit-adjacent levees~Unsuitable, Bedrock Constraints~Suitable, Adjacent river depth~Suitable, Slope distance to river~Suitable
            (False, True, True, True): CPT['Practical restorability'][('Pit-adjacent levees~Unsuitable', 'Bedrock Constraints~Suitable', 'Adjacent river depth~Suitable', 'Slope distance to river~Suitable')],

            # Pit-adjacent levees~Suitable, Bedrock Constraints~Unsuitable, Adjacent river depth~Suitable, Slope distance to river~Unsuitable
            (True, False, True, False): CPT['Practical restorability'][('Pit-adjacent levees~Suitable', 'Bedrock Constraints~Unsuitable', 'Adjacent river depth~Suitable', 'Slope distance to river~Unsuitable')],

            # Pit-adjacent levees~Unsuitable, Bedrock Constraints~Unsuitable, Adjacent river depth~Unsuitable, Slope distance to river~Suitable
            (False, False, False, True): CPT['Practical restorability'][('Pit-adjacent levees~Unsuitable', 'Bedrock Constraints~Unsuitable', 'Adjacent river depth~Unsuitable', 'Slope distance to river~Suitable')],

            # Pit-adjacent levees~Unsuitable, Bedrock Constraints~Unsuitable, Adjacent river depth~Suitable, Slope distance to river~Unsuitable
            (False, False, True, False): CPT['Practical restorability'][('Pit-adjacent levees~Unsuitable', 'Bedrock Constraints~Unsuitable', 'Adjacent river depth~Suitable', 'Slope distance to river~Unsuitable')],

            # Pit-adjacent levees~Unsuitable, Bedrock Constraints~Unsuitable, Adjacent river depth~Unsuitable, Slope distance to river~Unsuitable
            (False, False, False, False): CPT['Practical restorability'][('Pit-adjacent levees~Unsuitable', 'Bedrock Constraints~Unsuitable', 'Adjacent river depth~Unsuitable', 'Slope distance to river~Unsuitable')],

            # Pit-adjacent levees~Suitable, Bedrock Constraints~Suitable, Adjacent river depth~Suitable, Slope distance to river~Unsuitable
            (True, True, True, False): CPT['Practical restorability'][('Pit-adjacent levees~Suitable', 'Bedrock Constraints~Suitable', 'Adjacent river depth~Suitable', 'Slope distance to river~Unsuitable')],

            # Pit-adjacent levees~Unsuitable, Bedrock Constraints~Suitable, Adjacent river depth~Unsuitable, Slope distance to river~Unsuitable
            (False, True, False, False): CPT['Practical restorability'][('Pit-adjacent levees~Unsuitable', 'Bedrock Constraints~Suitable', 'Adjacent river depth~Unsuitable', 'Slope distance to river~Unsuitable')],

            # Pit-adjacent levees~Unsuitable, Bedrock Constraints~Unsuitable, Adjacent river depth~Suitable, Slope distance to river~Suitable
            (False, False, True, True): CPT['Practical restorability'][('Pit-adjacent levees~Unsuitable', 'Bedrock Constraints~Unsuitable', 'Adjacent river depth~Suitable', 'Slope distance to river~Suitable')],

            # Pit-adjacent levees~Suitable, Bedrock Constraints~Suitable, Adjacent river depth~Unsuitable, Slope distance to river~Suitable
            (True, True, False, True): CPT['Practical restorability'][('Pit-adjacent levees~Suitable', 'Bedrock Constraints~Suitable', 'Adjacent river depth~Unsuitable', 'Slope distance to river~Suitable')],

            # Pit-adjacent levees~Suitable, Bedrock Constraints~Suitable, Adjacent river depth~Suitable, Slope distance to river~Suitable
            (True, True, True, True): CPT['Practical restorability'][('Pit-adjacent levees~Suitable', 'Bedrock Constraints~Suitable', 'Adjacent river depth~Suitable', 'Slope distance to river~Suitable')],

            # Pit-adjacent levees~Suitable, Bedrock Constraints~Unsuitable, Adjacent river depth~Unsuitable, Slope distance to river~Suitable
            (True, False, False, True): CPT['Practical restorability'][('Pit-adjacent levees~Suitable', 'Bedrock Constraints~Unsuitable', 'Adjacent river depth~Unsuitable', 'Slope distance to river~Suitable')],

            # Pit-adjacent levees~Suitable, Bedrock Constraints~Unsuitable, Adjacent river depth~Unsuitable, Slope distance to river~Unsuitable
            (True, False, False, False): CPT['Practical restorability'][('Pit-adjacent levees~Suitable', 'Bedrock Constraints~Unsuitable', 'Adjacent river depth~Unsuitable', 'Slope distance to river~Unsuitable')],

            # Pit-adjacent levees~Unsuitable, Bedrock Constraints~Suitable, Adjacent river depth~Unsuitable, Slope distance to river~Suitable
            (False, True, False, True): CPT['Practical restorability'][('Pit-adjacent levees~Unsuitable', 'Bedrock Constraints~Suitable', 'Adjacent river depth~Unsuitable', 'Slope distance to river~Suitable')],


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
    
    def f_water_quality_threat(contamination, restorable_substrate, water_quality_threat):
        cpt = {
             # Contamination~Unsuitable, Restorable Substrate~Unsuitable
            (False, False): CPT['Water quality threat'][('Contamination~Unsuitable', 'Restorable Substrate~Unsuitable')],

            # Contamination~Suitable, Restorable Substrate~Suitable
            (True, True): CPT['Water quality threat'][('Contamination~Suitable', 'Restorable Substrate~Suitable')],

            # Contamination~Unsuitable, Restorable Substrate~Suitable
            (False, True): CPT['Water quality threat'][('Contamination~Unsuitable', 'Restorable Substrate~Suitable')],

            # Contamination~Suitable, Restorable Substrate~Unsuitable
            (True, False): CPT['Water quality threat'][('Contamination~Suitable', 'Restorable Substrate~Unsuitable')],


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
    
    def f_pit_geometry(complexity, bank_slope, surface_area, depth, pit_geometry):
        cpt = {
             # Complexity~Suitable, Bank slope~Suitable, Surface area~Unsuitable, Depth~Suitable
            (True, True, False, True): CPT['Pit geometry'][('Complexity~Suitable', 'Bank slope~Suitable', 'Surface area~Unsuitable', 'Depth~Suitable')],

            # Complexity~Unsuitable, Bank slope~Unsuitable, Surface area~Unsuitable, Depth~Unsuitable
            (False, False, False, False): CPT['Pit geometry'][('Complexity~Unsuitable', 'Bank slope~Unsuitable', 'Surface area~Unsuitable', 'Depth~Unsuitable')],

            # Complexity~Suitable, Bank slope~Unsuitable, Surface area~Suitable, Depth~Suitable
            (True, False, True, True): CPT['Pit geometry'][('Complexity~Suitable', 'Bank slope~Unsuitable', 'Surface area~Suitable', 'Depth~Suitable')],

            # Complexity~Unsuitable, Bank slope~Unsuitable, Surface area~Suitable, Depth~Suitable
            (False, False, True, True): CPT['Pit geometry'][('Complexity~Unsuitable', 'Bank slope~Unsuitable', 'Surface area~Suitable', 'Depth~Suitable')],

            # Complexity~Suitable, Bank slope~Unsuitable, Surface area~Unsuitable, Depth~Unsuitable
            (True, False, False, False): CPT['Pit geometry'][('Complexity~Suitable', 'Bank slope~Unsuitable', 'Surface area~Unsuitable', 'Depth~Unsuitable')],

            # Complexity~Suitable, Bank slope~Unsuitable, Surface area~Unsuitable, Depth~Suitable
            (True, False, False, True): CPT['Pit geometry'][('Complexity~Suitable', 'Bank slope~Unsuitable', 'Surface area~Unsuitable', 'Depth~Suitable')],

            # Complexity~Unsuitable, Bank slope~Unsuitable, Surface area~Unsuitable, Depth~Suitable
            (False, False, False, True): CPT['Pit geometry'][('Complexity~Unsuitable', 'Bank slope~Unsuitable', 'Surface area~Unsuitable', 'Depth~Suitable')],

            # Complexity~Suitable, Bank slope~Suitable, Surface area~Suitable, Depth~Unsuitable
            (True, True, True, False): CPT['Pit geometry'][('Complexity~Suitable', 'Bank slope~Suitable', 'Surface area~Suitable', 'Depth~Unsuitable')],

            # Complexity~Suitable, Bank slope~Suitable, Surface area~Unsuitable, Depth~Unsuitable
            (True, True, False, False): CPT['Pit geometry'][('Complexity~Suitable', 'Bank slope~Suitable', 'Surface area~Unsuitable', 'Depth~Unsuitable')],

            # Complexity~Unsuitable, Bank slope~Suitable, Surface area~Suitable, Depth~Suitable
            (False, True, True, True): CPT['Pit geometry'][('Complexity~Unsuitable', 'Bank slope~Suitable', 'Surface area~Suitable', 'Depth~Suitable')],

            # Complexity~Unsuitable, Bank slope~Suitable, Surface area~Unsuitable, Depth~Suitable
            (False, True, False, True): CPT['Pit geometry'][('Complexity~Unsuitable', 'Bank slope~Suitable', 'Surface area~Unsuitable', 'Depth~Suitable')],

            # Complexity~Unsuitable, Bank slope~Unsuitable, Surface area~Suitable, Depth~Unsuitable
            (False, False, True, False): CPT['Pit geometry'][('Complexity~Unsuitable', 'Bank slope~Unsuitable', 'Surface area~Suitable', 'Depth~Unsuitable')],

            # Complexity~Unsuitable, Bank slope~Suitable, Surface area~Suitable, Depth~Unsuitable
            (False, True, True, False): CPT['Pit geometry'][('Complexity~Unsuitable', 'Bank slope~Suitable', 'Surface area~Suitable', 'Depth~Unsuitable')],

            # Complexity~Suitable, Bank slope~Unsuitable, Surface area~Suitable, Depth~Unsuitable
            (True, False, True, False): CPT['Pit geometry'][('Complexity~Suitable', 'Bank slope~Unsuitable', 'Surface area~Suitable', 'Depth~Unsuitable')],

            # Complexity~Suitable, Bank slope~Suitable, Surface area~Suitable, Depth~Suitable
            (True, True, True, True): CPT['Pit geometry'][('Complexity~Suitable', 'Bank slope~Suitable', 'Surface area~Suitable', 'Depth~Suitable')],

            # Complexity~Unsuitable, Bank slope~Suitable, Surface area~Unsuitable, Depth~Unsuitable
            (False, True, False, False): CPT['Pit geometry'][('Complexity~Unsuitable', 'Bank slope~Suitable', 'Surface area~Unsuitable', 'Depth~Unsuitable')],


        }
        p = cpt[(complexity, bank_slope, surface_area, depth)]
        if pit_geometry:
            return p
        else:
            return 1.0 - p
    
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
    
    def f_surface_area(surface_area):
        if surface_area:
            return prob['surface_area']
        else:
            return 1.0 - prob['surface_area']
    
    def f_depth(depth):
        if depth:
            return prob['depth']
        else:
            return 1.0 - prob['depth']
    
    def f_landscape(conservation_value, geomorphic_controls, abiotic_conditions, floodplain_characteristics, landscape):
        cpt = {
             # Conservation value~Unsuitable, Geomorphic Controls~Unsuitable, Abiotic conditions~Unsuitable, Floodplain characteristics~Suitable
            (False, False, False, True): CPT['Landscape'][('Conservation value~Unsuitable', 'Geomorphic Controls~Unsuitable', 'Abiotic conditions~Unsuitable', 'Floodplain characteristics~Suitable')],

            # Conservation value~Suitable, Geomorphic Controls~Suitable, Abiotic conditions~Unsuitable, Floodplain characteristics~Unsuitable
            (True, True, False, False): CPT['Landscape'][('Conservation value~Suitable', 'Geomorphic Controls~Suitable', 'Abiotic conditions~Unsuitable', 'Floodplain characteristics~Unsuitable')],

            # Conservation value~Suitable, Geomorphic Controls~Unsuitable, Abiotic conditions~Unsuitable, Floodplain characteristics~Unsuitable
            (True, False, False, False): CPT['Landscape'][('Conservation value~Suitable', 'Geomorphic Controls~Unsuitable', 'Abiotic conditions~Unsuitable', 'Floodplain characteristics~Unsuitable')],

            # Conservation value~Suitable, Geomorphic Controls~Unsuitable, Abiotic conditions~Suitable, Floodplain characteristics~Suitable
            (True, False, True, True): CPT['Landscape'][('Conservation value~Suitable', 'Geomorphic Controls~Unsuitable', 'Abiotic conditions~Suitable', 'Floodplain characteristics~Suitable')],

            # Conservation value~Unsuitable, Geomorphic Controls~Unsuitable, Abiotic conditions~Suitable, Floodplain characteristics~Suitable
            (False, False, True, True): CPT['Landscape'][('Conservation value~Unsuitable', 'Geomorphic Controls~Unsuitable', 'Abiotic conditions~Suitable', 'Floodplain characteristics~Suitable')],

            # Conservation value~Suitable, Geomorphic Controls~Suitable, Abiotic conditions~Unsuitable, Floodplain characteristics~Suitable
            (True, True, False, True): CPT['Landscape'][('Conservation value~Suitable', 'Geomorphic Controls~Suitable', 'Abiotic conditions~Unsuitable', 'Floodplain characteristics~Suitable')],

            # Conservation value~Suitable, Geomorphic Controls~Suitable, Abiotic conditions~Suitable, Floodplain characteristics~Suitable
            (True, True, True, True): CPT['Landscape'][('Conservation value~Suitable', 'Geomorphic Controls~Suitable', 'Abiotic conditions~Suitable', 'Floodplain characteristics~Suitable')],

            # Conservation value~Unsuitable, Geomorphic Controls~Unsuitable, Abiotic conditions~Unsuitable, Floodplain characteristics~Unsuitable
            (False, False, False, False): CPT['Landscape'][('Conservation value~Unsuitable', 'Geomorphic Controls~Unsuitable', 'Abiotic conditions~Unsuitable', 'Floodplain characteristics~Unsuitable')],

            # Conservation value~Unsuitable, Geomorphic Controls~Suitable, Abiotic conditions~Unsuitable, Floodplain characteristics~Unsuitable
            (False, True, False, False): CPT['Landscape'][('Conservation value~Unsuitable', 'Geomorphic Controls~Suitable', 'Abiotic conditions~Unsuitable', 'Floodplain characteristics~Unsuitable')],

            # Conservation value~Suitable, Geomorphic Controls~Unsuitable, Abiotic conditions~Suitable, Floodplain characteristics~Unsuitable
            (True, False, True, False): CPT['Landscape'][('Conservation value~Suitable', 'Geomorphic Controls~Unsuitable', 'Abiotic conditions~Suitable', 'Floodplain characteristics~Unsuitable')],

            # Conservation value~Unsuitable, Geomorphic Controls~Suitable, Abiotic conditions~Suitable, Floodplain characteristics~Unsuitable
            (False, True, True, False): CPT['Landscape'][('Conservation value~Unsuitable', 'Geomorphic Controls~Suitable', 'Abiotic conditions~Suitable', 'Floodplain characteristics~Unsuitable')],

            # Conservation value~Suitable, Geomorphic Controls~Suitable, Abiotic conditions~Suitable, Floodplain characteristics~Unsuitable
            (True, True, True, False): CPT['Landscape'][('Conservation value~Suitable', 'Geomorphic Controls~Suitable', 'Abiotic conditions~Suitable', 'Floodplain characteristics~Unsuitable')],

            # Conservation value~Unsuitable, Geomorphic Controls~Unsuitable, Abiotic conditions~Suitable, Floodplain characteristics~Unsuitable
            (False, False, True, False): CPT['Landscape'][('Conservation value~Unsuitable', 'Geomorphic Controls~Unsuitable', 'Abiotic conditions~Suitable', 'Floodplain characteristics~Unsuitable')],

            # Conservation value~Unsuitable, Geomorphic Controls~Suitable, Abiotic conditions~Suitable, Floodplain characteristics~Suitable
            (False, True, True, True): CPT['Landscape'][('Conservation value~Unsuitable', 'Geomorphic Controls~Suitable', 'Abiotic conditions~Suitable', 'Floodplain characteristics~Suitable')],

            # Conservation value~Unsuitable, Geomorphic Controls~Suitable, Abiotic conditions~Unsuitable, Floodplain characteristics~Suitable
            (False, True, False, True): CPT['Landscape'][('Conservation value~Unsuitable', 'Geomorphic Controls~Suitable', 'Abiotic conditions~Unsuitable', 'Floodplain characteristics~Suitable')],

            # Conservation value~Suitable, Geomorphic Controls~Unsuitable, Abiotic conditions~Unsuitable, Floodplain characteristics~Suitable
            (True, False, False, True): CPT['Landscape'][('Conservation value~Suitable', 'Geomorphic Controls~Unsuitable', 'Abiotic conditions~Unsuitable', 'Floodplain characteristics~Suitable')],


        }
        p = cpt[(conservation_value, geomorphic_controls, abiotic_conditions, floodplain_characteristics)]
        if landscape:
            return p
        else:
            return 1.0 - p
    
    def f_conservation_value(relationship_to_protected_areas, biotic_conditions, identified_in_conservation_plan, conservation_value):
        cpt = {
             # Relationship to protected areas~Connected, Biotic conditions~Suitable, Identified in conservation plan~Not Identified
            (True, True, False): CPT['Conservation value'][('Relationship to protected areas~Connected', 'Biotic conditions~Suitable', 'Identified in conservation plan~Not Identified')],

            # Relationship to protected areas~Disconnected, Biotic conditions~Unsuitable, Identified in conservation plan~Not Identified
            (False, False, False): CPT['Conservation value'][('Relationship to protected areas~Disconnected', 'Biotic conditions~Unsuitable', 'Identified in conservation plan~Not Identified')],

            # Relationship to protected areas~Connected, Biotic conditions~Unsuitable, Identified in conservation plan~Not Identified
            (True, False, False): CPT['Conservation value'][('Relationship to protected areas~Connected', 'Biotic conditions~Unsuitable', 'Identified in conservation plan~Not Identified')],

            # Relationship to protected areas~Connected, Biotic conditions~Suitable, Identified in conservation plan~Identified
            (True, True, True): CPT['Conservation value'][('Relationship to protected areas~Connected', 'Biotic conditions~Suitable', 'Identified in conservation plan~Identified')],

            # Relationship to protected areas~Disconnected, Biotic conditions~Unsuitable, Identified in conservation plan~Identified
            (False, False, True): CPT['Conservation value'][('Relationship to protected areas~Disconnected', 'Biotic conditions~Unsuitable', 'Identified in conservation plan~Identified')],

            # Relationship to protected areas~Disconnected, Biotic conditions~Suitable, Identified in conservation plan~Not Identified
            (False, True, False): CPT['Conservation value'][('Relationship to protected areas~Disconnected', 'Biotic conditions~Suitable', 'Identified in conservation plan~Not Identified')],

            # Relationship to protected areas~Disconnected, Biotic conditions~Suitable, Identified in conservation plan~Identified
            (False, True, True): CPT['Conservation value'][('Relationship to protected areas~Disconnected', 'Biotic conditions~Suitable', 'Identified in conservation plan~Identified')],

            # Relationship to protected areas~Connected, Biotic conditions~Unsuitable, Identified in conservation plan~Identified
            (True, False, True): CPT['Conservation value'][('Relationship to protected areas~Connected', 'Biotic conditions~Unsuitable', 'Identified in conservation plan~Identified')],


        }
        p = cpt[(relationship_to_protected_areas, biotic_conditions, identified_in_conservation_plan)]
        if conservation_value:
            return p
        else:
            return 1.0 - p
    
    def f_relationship_to_protected_areas(relationship_to_protected_areas):
        if relationship_to_protected_areas:
            return prob['relationship_to_protected_areas']
        else:
            return 1.0 - prob['relationship_to_protected_areas']
    
    def f_biotic_conditions(intact_floodplain_forest, habitat_features, species_of_interest, biotic_conditions):
        cpt = {
             # Intact floodplain forest~Intact, Habitat features~Suitable, Species of interest~Present
            (True, True, True): CPT['Biotic conditions'][('Intact floodplain forest~Intact', 'Habitat features~Suitable', 'Species of interest~Present')],

            # Intact floodplain forest~Intact, Habitat features~Suitable, Species of interest~Not Present
            (True, True, False): CPT['Biotic conditions'][('Intact floodplain forest~Intact', 'Habitat features~Suitable', 'Species of interest~Not Present')],

            # Intact floodplain forest~Intact, Habitat features~Unsuitable, Species of interest~Not Present
            (True, False, False): CPT['Biotic conditions'][('Intact floodplain forest~Intact', 'Habitat features~Unsuitable', 'Species of interest~Not Present')],

            # Intact floodplain forest~Missing, Habitat features~Unsuitable, Species of interest~Not Present
            (False, False, False): CPT['Biotic conditions'][('Intact floodplain forest~Missing', 'Habitat features~Unsuitable', 'Species of interest~Not Present')],

            # Intact floodplain forest~Missing, Habitat features~Suitable, Species of interest~Not Present
            (False, True, False): CPT['Biotic conditions'][('Intact floodplain forest~Missing', 'Habitat features~Suitable', 'Species of interest~Not Present')],

            # Intact floodplain forest~Missing, Habitat features~Unsuitable, Species of interest~Present
            (False, False, True): CPT['Biotic conditions'][('Intact floodplain forest~Missing', 'Habitat features~Unsuitable', 'Species of interest~Present')],

            # Intact floodplain forest~Intact, Habitat features~Unsuitable, Species of interest~Present
            (True, False, True): CPT['Biotic conditions'][('Intact floodplain forest~Intact', 'Habitat features~Unsuitable', 'Species of interest~Present')],

            # Intact floodplain forest~Missing, Habitat features~Suitable, Species of interest~Present
            (False, True, True): CPT['Biotic conditions'][('Intact floodplain forest~Missing', 'Habitat features~Suitable', 'Species of interest~Present')],


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
    
    def f_identified_in_conservation_plan(identified_in_conservation_plan):
        if identified_in_conservation_plan:
            return prob['identified_in_conservation_plan']
        else:
            return 1.0 - prob['identified_in_conservation_plan']
    
    def f_geomorphic_controls(channel_mobility, substrate, infrastructure_constraints, material_availability, geomorphic_controls):
        cpt = {
             # Channel mobility~Mobile, Substrate~Suitable, Infrastructure constraints~Unsuitable, Material availability~Available
            (True, True, False, True): CPT['Geomorphic Controls'][('Channel mobility~Mobile', 'Substrate~Suitable', 'Infrastructure constraints~Unsuitable', 'Material availability~Available')],

            # Channel mobility~Not mobile, Substrate~Suitable, Infrastructure constraints~No restrictions, Material availability~Available
            (False, True, True, True): CPT['Geomorphic Controls'][('Channel mobility~Not mobile', 'Substrate~Suitable', 'Infrastructure constraints~No restrictions', 'Material availability~Available')],

            # Channel mobility~Mobile, Substrate~Unsuitable, Infrastructure constraints~Unsuitable, Material availability~Unavailable
            (True, False, False, False): CPT['Geomorphic Controls'][('Channel mobility~Mobile', 'Substrate~Unsuitable', 'Infrastructure constraints~Unsuitable', 'Material availability~Unavailable')],

            # Channel mobility~Not mobile, Substrate~Unsuitable, Infrastructure constraints~Unsuitable, Material availability~Unavailable
            (False, False, False, False): CPT['Geomorphic Controls'][('Channel mobility~Not mobile', 'Substrate~Unsuitable', 'Infrastructure constraints~Unsuitable', 'Material availability~Unavailable')],

            # Channel mobility~Mobile, Substrate~Suitable, Infrastructure constraints~Unsuitable, Material availability~Unavailable
            (True, True, False, False): CPT['Geomorphic Controls'][('Channel mobility~Mobile', 'Substrate~Suitable', 'Infrastructure constraints~Unsuitable', 'Material availability~Unavailable')],

            # Channel mobility~Mobile, Substrate~Unsuitable, Infrastructure constraints~No restrictions, Material availability~Available
            (True, False, True, True): CPT['Geomorphic Controls'][('Channel mobility~Mobile', 'Substrate~Unsuitable', 'Infrastructure constraints~No restrictions', 'Material availability~Available')],

            # Channel mobility~Not mobile, Substrate~Suitable, Infrastructure constraints~Unsuitable, Material availability~Unavailable
            (False, True, False, False): CPT['Geomorphic Controls'][('Channel mobility~Not mobile', 'Substrate~Suitable', 'Infrastructure constraints~Unsuitable', 'Material availability~Unavailable')],

            # Channel mobility~Mobile, Substrate~Suitable, Infrastructure constraints~No restrictions, Material availability~Available
            (True, True, True, True): CPT['Geomorphic Controls'][('Channel mobility~Mobile', 'Substrate~Suitable', 'Infrastructure constraints~No restrictions', 'Material availability~Available')],

            # Channel mobility~Not mobile, Substrate~Suitable, Infrastructure constraints~No restrictions, Material availability~Unavailable
            (False, True, True, False): CPT['Geomorphic Controls'][('Channel mobility~Not mobile', 'Substrate~Suitable', 'Infrastructure constraints~No restrictions', 'Material availability~Unavailable')],

            # Channel mobility~Mobile, Substrate~Unsuitable, Infrastructure constraints~Unsuitable, Material availability~Available
            (True, False, False, True): CPT['Geomorphic Controls'][('Channel mobility~Mobile', 'Substrate~Unsuitable', 'Infrastructure constraints~Unsuitable', 'Material availability~Available')],

            # Channel mobility~Not mobile, Substrate~Unsuitable, Infrastructure constraints~No restrictions, Material availability~Available
            (False, False, True, True): CPT['Geomorphic Controls'][('Channel mobility~Not mobile', 'Substrate~Unsuitable', 'Infrastructure constraints~No restrictions', 'Material availability~Available')],

            # Channel mobility~Not mobile, Substrate~Unsuitable, Infrastructure constraints~Unsuitable, Material availability~Available
            (False, False, False, True): CPT['Geomorphic Controls'][('Channel mobility~Not mobile', 'Substrate~Unsuitable', 'Infrastructure constraints~Unsuitable', 'Material availability~Available')],

            # Channel mobility~Not mobile, Substrate~Unsuitable, Infrastructure constraints~No restrictions, Material availability~Unavailable
            (False, False, True, False): CPT['Geomorphic Controls'][('Channel mobility~Not mobile', 'Substrate~Unsuitable', 'Infrastructure constraints~No restrictions', 'Material availability~Unavailable')],

            # Channel mobility~Mobile, Substrate~Suitable, Infrastructure constraints~No restrictions, Material availability~Unavailable
            (True, True, True, False): CPT['Geomorphic Controls'][('Channel mobility~Mobile', 'Substrate~Suitable', 'Infrastructure constraints~No restrictions', 'Material availability~Unavailable')],

            # Channel mobility~Not mobile, Substrate~Suitable, Infrastructure constraints~Unsuitable, Material availability~Available
            (False, True, False, True): CPT['Geomorphic Controls'][('Channel mobility~Not mobile', 'Substrate~Suitable', 'Infrastructure constraints~Unsuitable', 'Material availability~Available')],

            # Channel mobility~Mobile, Substrate~Unsuitable, Infrastructure constraints~No restrictions, Material availability~Unavailable
            (True, False, True, False): CPT['Geomorphic Controls'][('Channel mobility~Mobile', 'Substrate~Unsuitable', 'Infrastructure constraints~No restrictions', 'Material availability~Unavailable')],


        }
        p = cpt[(channel_mobility, substrate, infrastructure_constraints, material_availability)]
        if geomorphic_controls:
            return p
        else:
            return 1.0 - p
    
    def f_channel_mobility(channel_mobility):
        if channel_mobility:
            return prob['channel_mobility']
        else:
            return 1.0 - prob['channel_mobility']
    
    def f_substrate(substrate):
        if substrate:
            return prob['substrate']
        else:
            return 1.0 - prob['substrate']
    
    def f_infrastructure_constraints(infrastructure_constraints):
        if infrastructure_constraints:
            return prob['infrastructure_constraints']
        else:
            return 1.0 - prob['infrastructure_constraints']
    
    def f_material_availability(material_availability):
        if material_availability:
            return prob['material_availability']
        else:
            return 1.0 - prob['material_availability']
    
    def f_abiotic_conditions(water_quality, connectivity_barriers, abiotic_conditions):
        cpt = {
             # Water quality~High Quality, Connectivity barriers~Disconnected
            (True, False): CPT['Abiotic conditions'][('Water quality~High Quality', 'Connectivity barriers~Disconnected')],

            # Water quality~High Quality, Connectivity barriers~Connected
            (True, True): CPT['Abiotic conditions'][('Water quality~High Quality', 'Connectivity barriers~Connected')],

            # Water quality~Low Quality, Connectivity barriers~Connected
            (False, True): CPT['Abiotic conditions'][('Water quality~Low Quality', 'Connectivity barriers~Connected')],

            # Water quality~Low Quality, Connectivity barriers~Disconnected
            (False, False): CPT['Abiotic conditions'][('Water quality~Low Quality', 'Connectivity barriers~Disconnected')],


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
    
    def f_connectivity_barriers(on_property, downstream, upstream, connectivity_barriers):
        cpt = {
             # On property~Disconnected, Downstream~Disconnected, Upstream~Connected
            (False, False, True): CPT['Connectivity barriers'][('On property~Disconnected', 'Downstream~Disconnected', 'Upstream~Connected')],

            # On property~Connected, Downstream~Connected, Upstream~Connected
            (True, True, True): CPT['Connectivity barriers'][('On property~Connected', 'Downstream~Connected', 'Upstream~Connected')],

            # On property~Connected, Downstream~Disconnected, Upstream~Disconnected
            (True, False, False): CPT['Connectivity barriers'][('On property~Connected', 'Downstream~Disconnected', 'Upstream~Disconnected')],

            # On property~Disconnected, Downstream~Connected, Upstream~Disconnected
            (False, True, False): CPT['Connectivity barriers'][('On property~Disconnected', 'Downstream~Connected', 'Upstream~Disconnected')],

            # On property~Disconnected, Downstream~Disconnected, Upstream~Disconnected
            (False, False, False): CPT['Connectivity barriers'][('On property~Disconnected', 'Downstream~Disconnected', 'Upstream~Disconnected')],

            # On property~Connected, Downstream~Connected, Upstream~Disconnected
            (True, True, False): CPT['Connectivity barriers'][('On property~Connected', 'Downstream~Connected', 'Upstream~Disconnected')],

            # On property~Connected, Downstream~Disconnected, Upstream~Connected
            (True, False, True): CPT['Connectivity barriers'][('On property~Connected', 'Downstream~Disconnected', 'Upstream~Connected')],

            # On property~Disconnected, Downstream~Connected, Upstream~Connected
            (False, True, True): CPT['Connectivity barriers'][('On property~Disconnected', 'Downstream~Connected', 'Upstream~Connected')],


        }
        p = cpt[(on_property, downstream, upstream)]
        if connectivity_barriers:
            return p
        else:
            return 1.0 - p
    
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
    
    def f_upstream(upstream):
        if upstream:
            return prob['upstream']
        else:
            return 1.0 - prob['upstream']
    
    def f_floodplain_characteristics(within_x_year_floodplain, gradient, width, location_in_floodplain, floodplain_characteristics):
        cpt = {
             # Within X-year floodplain~Within, Gradient~Suitable, Width~Unsuitable, Location in floodplain~Ineffective
            (True, True, False, False): CPT['Floodplain characteristic'][('Within X-year floodplain~Within', 'Gradient~Suitable', 'Width~Unsuitable', 'Location in floodplain~Ineffective')],

            # Within X-year floodplain~Outside, Gradient~Suitable, Width~Unsuitable, Location in floodplain~Ineffective
            (False, True, False, False): CPT['Floodplain characteristic'][('Within X-year floodplain~Outside', 'Gradient~Suitable', 'Width~Unsuitable', 'Location in floodplain~Ineffective')],

            # Within X-year floodplain~Within, Gradient~Unsuitable, Width~Suitable, Location in floodplain~Ineffective
            (True, False, True, False): CPT['Floodplain characteristic'][('Within X-year floodplain~Within', 'Gradient~Unsuitable', 'Width~Suitable', 'Location in floodplain~Ineffective')],

            # Within X-year floodplain~Within, Gradient~Suitable, Width~Suitable, Location in floodplain~Strategic
            (True, True, True, True): CPT['Floodplain characteristic'][('Within X-year floodplain~Within', 'Gradient~Suitable', 'Width~Suitable', 'Location in floodplain~Strategic')],

            # Within X-year floodplain~Outside, Gradient~Unsuitable, Width~Suitable, Location in floodplain~Ineffective
            (False, False, True, False): CPT['Floodplain characteristic'][('Within X-year floodplain~Outside', 'Gradient~Unsuitable', 'Width~Suitable', 'Location in floodplain~Ineffective')],

            # Within X-year floodplain~Outside, Gradient~Suitable, Width~Suitable, Location in floodplain~Strategic
            (False, True, True, True): CPT['Floodplain characteristic'][('Within X-year floodplain~Outside', 'Gradient~Suitable', 'Width~Suitable', 'Location in floodplain~Strategic')],

            # Within X-year floodplain~Outside, Gradient~Unsuitable, Width~Unsuitable, Location in floodplain~Ineffective
            (False, False, False, False): CPT['Floodplain characteristic'][('Within X-year floodplain~Outside', 'Gradient~Unsuitable', 'Width~Unsuitable', 'Location in floodplain~Ineffective')],

            # Within X-year floodplain~Within, Gradient~Unsuitable, Width~Unsuitable, Location in floodplain~Ineffective
            (True, False, False, False): CPT['Floodplain characteristic'][('Within X-year floodplain~Within', 'Gradient~Unsuitable', 'Width~Unsuitable', 'Location in floodplain~Ineffective')],

            # Within X-year floodplain~Outside, Gradient~Suitable, Width~Unsuitable, Location in floodplain~Strategic
            (False, True, False, True): CPT['Floodplain characteristic'][('Within X-year floodplain~Outside', 'Gradient~Suitable', 'Width~Unsuitable', 'Location in floodplain~Strategic')],

            # Within X-year floodplain~Within, Gradient~Suitable, Width~Unsuitable, Location in floodplain~Strategic
            (True, True, False, True): CPT['Floodplain characteristic'][('Within X-year floodplain~Within', 'Gradient~Suitable', 'Width~Unsuitable', 'Location in floodplain~Strategic')],

            # Within X-year floodplain~Outside, Gradient~Unsuitable, Width~Suitable, Location in floodplain~Strategic
            (False, False, True, True): CPT['Floodplain characteristic'][('Within X-year floodplain~Outside', 'Gradient~Unsuitable', 'Width~Suitable', 'Location in floodplain~Strategic')],

            # Within X-year floodplain~Outside, Gradient~Suitable, Width~Suitable, Location in floodplain~Ineffective
            (False, True, True, False): CPT['Floodplain characteristic'][('Within X-year floodplain~Outside', 'Gradient~Suitable', 'Width~Suitable', 'Location in floodplain~Ineffective')],

            # Within X-year floodplain~Within, Gradient~Unsuitable, Width~Suitable, Location in floodplain~Strategic
            (True, False, True, True): CPT['Floodplain characteristic'][('Within X-year floodplain~Within', 'Gradient~Unsuitable', 'Width~Suitable', 'Location in floodplain~Strategic')],

            # Within X-year floodplain~Within, Gradient~Suitable, Width~Suitable, Location in floodplain~Ineffective
            (True, True, True, False): CPT['Floodplain characteristic'][('Within X-year floodplain~Within', 'Gradient~Suitable', 'Width~Suitable', 'Location in floodplain~Ineffective')],

            # Within X-year floodplain~Within, Gradient~Unsuitable, Width~Unsuitable, Location in floodplain~Strategic
            (True, False, False, True): CPT['Floodplain characteristic'][('Within X-year floodplain~Within', 'Gradient~Unsuitable', 'Width~Unsuitable', 'Location in floodplain~Strategic')],

            # Within X-year floodplain~Outside, Gradient~Unsuitable, Width~Unsuitable, Location in floodplain~Strategic
            (False, False, False, True): CPT['Floodplain characteristic'][('Within X-year floodplain~Outside', 'Gradient~Unsuitable', 'Width~Unsuitable', 'Location in floodplain~Strategic')],


        }
        p = cpt[(within_x_year_floodplain, gradient, width, location_in_floodplain)]
        if floodplain_characteristics:
            return p
        else:
            return 1.0 - p
    
    def f_within_x_year_floodplain(within_x_year_floodplain):
        if within_x_year_floodplain:
            return prob['within_x_year_floodplain']
        else:
            return 1.0 - prob['within_x_year_floodplain']
    
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
    
    levels = [True, False]
    net = build_bbn(
        f_suitability,
        f_socio_economic,
        f_cost_benefit,
        f_public_perception,
        f_property_value,
        f_contamination_or_hazardous_waste,
        f_threats_to_other_areas_or_permittability,
        f_surrounding_land_use,
        f_water_rights,
        f_surrounding_ownership,
        f_infrastructure,
        f_site,
        f_practical_property_level_restorability,
        f_continuing_property_access,
        f_site_accessibility,
        f_fill_material_availability,
        f_pit_restorability,
        f_practical_restorability,
        f_pit_adjacent_levees,
        f_bedrock_constraints,
        f_adjacent_river_depth,
        f_slope_distance_to_river,
        f_water_quality_threat,
        f_contamination,
        f_restorable_substrate,
        f_pit_geometry,
        f_complexity,
        f_bank_slope,
        f_surface_area,
        f_depth,
        f_landscape,
        f_conservation_value,
        f_relationship_to_protected_areas,
        f_biotic_conditions,
        f_intact_floodplain_forest,
        f_habitat_features,
        f_species_of_interest,
        f_identified_in_conservation_plan,
        f_geomorphic_controls,
        f_channel_mobility,
        f_substrate,
        f_infrastructure_constraints,
        f_material_availability,
        f_abiotic_conditions,
        f_water_quality,
        f_connectivity_barriers,
        f_on_property,
        f_downstream,
        f_upstream,
        f_floodplain_characteristics,
        f_within_x_year_floodplain,
        f_gradient,
        f_width,
        f_location_in_floodplain,

        # assume simple binary
        domains=dict(
            suitability = levels,
            socio_economic = levels,
            cost_benefit = levels,
            public_perception = levels,
            property_value = levels,
            contamination_or_hazardous_waste = levels,
            threats_to_other_areas_or_permittability = levels,
            surrounding_land_use = levels,
            water_rights = levels,
            surrounding_ownership = levels,
            infrastructure = levels,
            site = levels,
            practical_property_level_restorability = levels,
            continuing_property_access = levels,
            site_accessibility = levels,
            fill_material_availability = levels,
            pit_restorability = levels,
            practical_restorability = levels,
            pit_adjacent_levees = levels,
            bedrock_constraints = levels,
            adjacent_river_depth = levels,
            slope_distance_to_river = levels,
            water_quality_threat = levels,
            contamination = levels,
            restorable_substrate = levels,
            pit_geometry = levels,
            complexity = levels,
            bank_slope = levels,
            surface_area = levels,
            depth = levels,
            landscape = levels,
            conservation_value = levels,
            relationship_to_protected_areas = levels,
            biotic_conditions = levels,
            intact_floodplain_forest = levels,
            habitat_features = levels,
            species_of_interest = levels,
            identified_in_conservation_plan = levels,
            geomorphic_controls = levels,
            channel_mobility = levels,
            substrate = levels,
            infrastructure_constraints = levels,
            material_availability = levels,
            abiotic_conditions = levels,
            water_quality = levels,
            connectivity_barriers = levels,
            on_property = levels,
            downstream = levels,
            upstream = levels,
            floodplain_characteristics = levels,
            within_x_year_floodplain = levels,
            gradient = levels,
            width = levels,
            location_in_floodplain = levels,
        )
    )

    prob = dict(
    public_perception = 1.0,
        property_value = 1.0,
        contamination_or_hazardous_waste = 1.0,
        surrounding_land_use = 1.0,
        water_rights = 1.0,
        surrounding_ownership = 1.0,
        infrastructure = 1.0,
        continuing_property_access = 1.0,
        site_accessibility = 1.0,
        fill_material_availability = 1.0,
        pit_adjacent_levees = 1.0,
        bedrock_constraints = 1.0,
        adjacent_river_depth = 1.0,
        slope_distance_to_river = 1.0,
        contamination = 1.0,
        restorable_substrate = 1.0,
        complexity = 1.0,
        bank_slope = 1.0,
        surface_area = 1.0,
        depth = 1.0,
        relationship_to_protected_areas = 1.0,
        intact_floodplain_forest = 1.0,
        habitat_features = 1.0,
        species_of_interest = 1.0,
        identified_in_conservation_plan = 1.0,
        channel_mobility = 1.0,
        substrate = 1.0,
        infrastructure_constraints = 1.0,
        material_availability = 1.0,
        water_quality = 1.0,
        on_property = 1.0,
        downstream = 1.0,
        upstream = 1.0,
        within_x_year_floodplain = 1.0,
        gradient = 1.0,
        width = 1.0,
        location_in_floodplain = 1.0,)

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

    CPT = xls2cptdict('/home/mperry/src/floodplain-restoration/data/cpt.xls')

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

        