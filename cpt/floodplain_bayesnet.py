from bayesian.bbn import build_bbn

def main(user_data=None):
    if not user_data:
        user_data = {}


    def f_suitability(socio_economic, site, landscape, suitability):  # needs review
        cpt = {
            # Suitable, Suitable, Suitable
            (True, True, True): 1.0,

            # Suitable, Suitable, Unsuitable
            (True, True, False): 0.8,

            # Suitable, Unsuitable, Suitable
            (True, False, True): 0.6,

            # Suitable, Unsuitable, Unsuitable
            (True, False, False): 0.7,

            # Unsuitable, Suitable, Suitable
            (False, True, True): 0.5,

            # Unsuitable, Suitable, Unsuitable
            (False, True, False): 0.4,

            # Unsuitable, Unsuitable, Suitable
            (False, False, True): 0.2,

            # Unsuitable, Unsuitable, Unsuitable
            (False, False, False): 0.0,


        }
        p = cpt[(socio_economic, site, landscape)]
        if suitability:
            return p
        else:
            return 1.0 - p
    

    def f_socio_economic(cost_benefit, threats_to_other_areas_or_permittability, socio_economic):
        cpt = {
            # Costly, Threatened
            (True, True): 0.0,

            # Costly, Not Threatened
            (True, False): 0.75,

            # Inexpensive, Threatened
            (False, True): 0.0,

            # Inexpensive, Not Threatened
            (False, False): 1.0,


        }
        p = cpt[(cost_benefit, threats_to_other_areas_or_permittability)]
        if socio_economic:
            return p
        else:
            return 1.0 - p
    

    def f_cost_benefit(property_value, contamination_or_hazardous_waste, public_perception, cost_benefit):
        cpt = {
            # Costly, Clean, Supportive
            (True, True, True): 0.5,

            # Costly, Clean, Unfavorable
            (True, True, False): 0.2,

            # Costly, Contaminated, Supportive
            (True, False, True): 0.4,

            # Costly, Contaminated, Unfavorable
            (True, False, False): 0.0,

            # Inexpensive, Clean, Supportive
            (False, True, True): 1.0,

            # Inexpensive, Clean, Unfavorable
            (False, True, False): 0.4,

            # Inexpensive, Contaminated, Supportive
            (False, False, True): 0.6,

            # Inexpensive, Contaminated, Unfavorable
            (False, False, False): 0.1,


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
    

    def f_threats_to_other_areas_or_permittability(water_rights, surrounding_ownership, infrastructure, surrounding_land_use, threats_to_other_areas_or_permittability):
        cpt = {
            # Threatened, Ammenable, Threatened, Ammenable
            (True, True, True, True): 0.0,

            # Threatened, Ammenable, Threatened, Unfriendly
            (True, True, True, False): 0.0,

            # Threatened, Ammenable, No threats, Ammenable
            (True, True, False, True): 0.6,

            # Threatened, Ammenable, No threats, Unfriendly
            (True, True, False, False): 0.5,

            # Threatened, Unfriendly, Threatened, Ammenable
            (True, False, True, True): 0.0,

            # Threatened, Unfriendly, Threatened, Unfriendly
            (True, False, True, False): 0.0,

            # Threatened, Unfriendly, No threats, Ammenable
            (True, False, False, True): 0.3,

            # Threatened, Unfriendly, No threats, Unfriendly
            (True, False, False, False): 0.2,

            # No threats, Ammenable, Threatened, Ammenable
            (False, True, True, True): 0.0,

            # No threats, Ammenable, Threatened, Unfriendly
            (False, True, True, False): 0.0,

            # No threats, Ammenable, No threats, Ammenable
            (False, True, False, True): 1.0,

            # No threats, Ammenable, No threats, Unfriendly
            (False, True, False, False): 0.9,

            # No threats, Unfriendly, Threatened, Ammenable
            (False, False, True, True): 0.0,

            # No threats, Unfriendly, Threatened, Unfriendly
            (False, False, True, False): 0.0,

            # No threats, Unfriendly, No threats, Ammenable
            (False, False, False, True): 0.5,

            # No threats, Unfriendly, No threats, Unfriendly
            (False, False, False, False): 0.4,


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
            # Threatened, Threatened, Threatened, Threatened, Threatened
            (True, True, True, True, True): 0.0,

            # Threatened, Threatened, Threatened, Threatened, No threats
            (True, True, True, True, False): 0.0,

            # Threatened, Threatened, Threatened, No threats, Threatened
            (True, True, True, False, True): 0.0,

            # Threatened, Threatened, Threatened, No threats, No threats
            (True, True, True, False, False): 0.0,

            # Threatened, Threatened, No threats, Threatened, Threatened
            (True, True, False, True, True): 0.0,

            # Threatened, Threatened, No threats, Threatened, No threats
            (True, True, False, True, False): 0.0,

            # Threatened, Threatened, No threats, No threats, Threatened
            (True, True, False, False, True): 0.0,

            # Threatened, Threatened, No threats, No threats, No threats
            (True, True, False, False, False): 0.0,

            # Threatened, No threats, Threatened, Threatened, Threatened
            (True, False, True, True, True): 0.0,

            # Threatened, No threats, Threatened, Threatened, No threats
            (True, False, True, True, False): 0.0,

            # Threatened, No threats, Threatened, No threats, Threatened
            (True, False, True, False, True): 0.0,

            # Threatened, No threats, Threatened, No threats, No threats
            (True, False, True, False, False): 0.0,

            # Threatened, No threats, No threats, Threatened, Threatened
            (True, False, False, True, True): 0.0,

            # Threatened, No threats, No threats, Threatened, No threats
            (True, False, False, True, False): 0.0,

            # Threatened, No threats, No threats, No threats, Threatened
            (True, False, False, False, True): 0.0,

            # Threatened, No threats, No threats, No threats, No threats
            (True, False, False, False, False): 0.0,

            # No threats, Threatened, Threatened, Threatened, Threatened
            (False, True, True, True, True): 0.0,

            # No threats, Threatened, Threatened, Threatened, No threats
            (False, True, True, True, False): 0.0,

            # No threats, Threatened, Threatened, No threats, Threatened
            (False, True, True, False, True): 0.0,

            # No threats, Threatened, Threatened, No threats, No threats
            (False, True, True, False, False): 0.0,

            # No threats, Threatened, No threats, Threatened, Threatened
            (False, True, False, True, True): 0.0,

            # No threats, Threatened, No threats, Threatened, No threats
            (False, True, False, True, False): 0.0,

            # No threats, Threatened, No threats, No threats, Threatened
            (False, True, False, False, True): 0.0,

            # No threats, Threatened, No threats, No threats, No threats
            (False, True, False, False, False): 0.0,

            # No threats, No threats, Threatened, Threatened, Threatened
            (False, False, True, True, True): 0.0,

            # No threats, No threats, Threatened, Threatened, No threats
            (False, False, True, True, False): 0.0,

            # No threats, No threats, Threatened, No threats, Threatened
            (False, False, True, False, True): 0.0,

            # No threats, No threats, Threatened, No threats, No threats
            (False, False, True, False, False): 0.0,

            # No threats, No threats, No threats, Threatened, Threatened
            (False, False, False, True, True): 0.0,

            # No threats, No threats, No threats, Threatened, No threats
            (False, False, False, True, False): 0.0,

            # No threats, No threats, No threats, No threats, Threatened
            (False, False, False, False, True): 0.0,

            # No threats, No threats, No threats, No threats, No threats
            (False, False, False, False, False): 1.0,


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
    

    def f_site(pit_restorability, practical_property_level_restorability, site):
        cpt = {
            # Suitable, Suitable
            (True, True): 1.0,

            # Suitable, Unsuitable
            (True, False): 0.8,

            # Unsuitable, Suitable
            (False, True): 0.2,

            # Unsuitable, Unsuitable
            (False, False): 0.0,


        }
        p = cpt[(pit_restorability, practical_property_level_restorability)]
        if site:
            return p
        else:
            return 1.0 - p
    

    def f_pit_restorability(pit_geometry, water_quality_threat, practical_restorability, pit_restorability):
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        #
        #
        #
        # TODO
        #
        #
        #
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        cpt = {
            # Suitable, Suitable, Suitable
            (True, True, True): 1.0,

            # Suitable, Suitable, Unsuitable
            (True, True, False): 0.,

            # Suitable, Unsuitable, Suitable
            (True, False, True): 0.5,

            # Suitable, Unsuitable, Unsuitable
            (True, False, False): 0.5,

            # Unsuitable, Suitable, Suitable
            (False, True, True): 0.5,

            # Unsuitable, Suitable, Unsuitable
            (False, True, False): 0.5,

            # Unsuitable, Unsuitable, Suitable
            (False, False, True): 0.5,

            # Unsuitable, Unsuitable, Unsuitable
            (False, False, False): 0.5,


        }
        p = cpt[(pit_geometry, water_quality_threat, practical_restorability)]
        if pit_restorability:
            return p
        else:
            return 1.0 - p
    

    def f_pit_geometry(depth, circumference, surface_area, bank_slope, pit_geometry):
        cpt = {
            # Suitable, Suitable, Suitable, Suitable
            (True, True, True, True): 0.5,

            # Suitable, Suitable, Suitable, Unsuitable
            (True, True, True, False): 0.5,

            # Suitable, Suitable, Unsuitable, Suitable
            (True, True, False, True): 0.5,

            # Suitable, Suitable, Unsuitable, Unsuitable
            (True, True, False, False): 0.5,

            # Suitable, Unsuitable, Suitable, Suitable
            (True, False, True, True): 0.5,

            # Suitable, Unsuitable, Suitable, Unsuitable
            (True, False, True, False): 0.5,

            # Suitable, Unsuitable, Unsuitable, Suitable
            (True, False, False, True): 0.5,

            # Suitable, Unsuitable, Unsuitable, Unsuitable
            (True, False, False, False): 0.5,

            # Unsuitable, Suitable, Suitable, Suitable
            (False, True, True, True): 0.5,

            # Unsuitable, Suitable, Suitable, Unsuitable
            (False, True, True, False): 0.5,

            # Unsuitable, Suitable, Unsuitable, Suitable
            (False, True, False, True): 0.5,

            # Unsuitable, Suitable, Unsuitable, Unsuitable
            (False, True, False, False): 0.5,

            # Unsuitable, Unsuitable, Suitable, Suitable
            (False, False, True, True): 0.5,

            # Unsuitable, Unsuitable, Suitable, Unsuitable
            (False, False, True, False): 0.5,

            # Unsuitable, Unsuitable, Unsuitable, Suitable
            (False, False, False, True): 0.5,

            # Unsuitable, Unsuitable, Unsuitable, Unsuitable
            (False, False, False, False): 0.5,


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
            # Suitable, Suitable
            (True, True): 1.0,

            # Suitable, Unsuitable
            (True, False): 0.5,

            # Unsuitable, Suitable
            (False, True): 0.5,

            # Unsuitable, Unsuitable
            (False, False): 0.0,


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
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        #
        #
        #
        # TODO
        #
        #
        #
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        cpt = {
            # Suitable, Suitable, Suitable
            (True, True, True): 0.5,

            # Suitable, Suitable, Unsuitable
            (True, True, False): 0.5,

            # Suitable, Unsuitable, Suitable
            (True, False, True): 0.5,

            # Suitable, Unsuitable, Unsuitable
            (True, False, False): 0.5,

            # Unsuitable, Suitable, Suitable
            (False, True, True): 0.5,

            # Unsuitable, Suitable, Unsuitable
            (False, True, False): 0.5,

            # Unsuitable, Unsuitable, Suitable
            (False, False, True): 0.5,

            # Unsuitable, Unsuitable, Unsuitable
            (False, False, False): 0.5,


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
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        #
        #
        #
        # TODO
        #
        #
        #
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        cpt = {
            # Available, Accessible, Suitable
            (True, True, True): 0.5,

            # Available, Accessible, Unsuitable
            (True, True, False): 0.5,

            # Available, Inaccessible, Suitable
            (True, False, True): 0.5,

            # Available, Inaccessible, Unsuitable
            (True, False, False): 0.5,

            # Unavailable, Accessible, Suitable
            (False, True, True): 0.5,

            # Unavailable, Accessible, Unsuitable
            (False, True, False): 0.5,

            # Unavailable, Inaccessible, Suitable
            (False, False, True): 0.5,

            # Unavailable, Inaccessible, Unsuitable
            (False, False, False): 0.5,


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
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        #
        #
        #
        # TODO
        #
        #
        #
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        cpt = {
            # Suitable, Suitable, Suitable, Suitable
            (True, True, True, True): 0.5,

            # Suitable, Suitable, Suitable, Unsuitable
            (True, True, True, False): 0.5,

            # Suitable, Suitable, Unsuitable, Suitable
            (True, True, False, True): 0.5,

            # Suitable, Suitable, Unsuitable, Unsuitable
            (True, True, False, False): 0.5,

            # Suitable, Unsuitable, Suitable, Suitable
            (True, False, True, True): 0.5,

            # Suitable, Unsuitable, Suitable, Unsuitable
            (True, False, True, False): 0.5,

            # Suitable, Unsuitable, Unsuitable, Suitable
            (True, False, False, True): 0.5,

            # Suitable, Unsuitable, Unsuitable, Unsuitable
            (True, False, False, False): 0.5,

            # Unsuitable, Suitable, Suitable, Suitable
            (False, True, True, True): 0.5,

            # Unsuitable, Suitable, Suitable, Unsuitable
            (False, True, True, False): 0.5,

            # Unsuitable, Suitable, Unsuitable, Suitable
            (False, True, False, True): 0.5,

            # Unsuitable, Suitable, Unsuitable, Unsuitable
            (False, True, False, False): 0.5,

            # Unsuitable, Unsuitable, Suitable, Suitable
            (False, False, True, True): 0.5,

            # Unsuitable, Unsuitable, Suitable, Unsuitable
            (False, False, True, False): 0.5,

            # Unsuitable, Unsuitable, Unsuitable, Suitable
            (False, False, False, True): 0.5,

            # Unsuitable, Unsuitable, Unsuitable, Unsuitable
            (False, False, False, False): 0.5,


        }
        p = cpt[(geomorphic_controls, abiotic_conditions, floodplain_characteristics, conservation_value)]
        if landscape:
            return p
        else:
            return 1.0 - p
    

    def f_geomorphic_controls(material_availability, channel_mobility, infrastructure_constraints, substrate, geomorphic_controls):
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        #
        #
        #
        # TODO
        #
        #
        #
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        cpt = {
            # Available, Mobile, No restrictions, Suitable
            (True, True, True, True): 0.5,

            # Available, Mobile, No restrictions, Unsuitable
            (True, True, True, False): 0.5,

            # Available, Mobile, Unsuitable, Suitable
            (True, True, False, True): 0.5,

            # Available, Mobile, Unsuitable, Unsuitable
            (True, True, False, False): 0.5,

            # Available, Not mobile, No restrictions, Suitable
            (True, False, True, True): 0.5,

            # Available, Not mobile, No restrictions, Unsuitable
            (True, False, True, False): 0.5,

            # Available, Not mobile, Unsuitable, Suitable
            (True, False, False, True): 0.5,

            # Available, Not mobile, Unsuitable, Unsuitable
            (True, False, False, False): 0.5,

            # Unavailable, Mobile, No restrictions, Suitable
            (False, True, True, True): 0.5,

            # Unavailable, Mobile, No restrictions, Unsuitable
            (False, True, True, False): 0.5,

            # Unavailable, Mobile, Unsuitable, Suitable
            (False, True, False, True): 0.5,

            # Unavailable, Mobile, Unsuitable, Unsuitable
            (False, True, False, False): 0.5,

            # Unavailable, Not mobile, No restrictions, Suitable
            (False, False, True, True): 0.5,

            # Unavailable, Not mobile, No restrictions, Unsuitable
            (False, False, True, False): 0.5,

            # Unavailable, Not mobile, Unsuitable, Suitable
            (False, False, False, True): 0.5,

            # Unavailable, Not mobile, Unsuitable, Unsuitable
            (False, False, False, False): 0.5,


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
            # High Quality, Connected
            (True, True): 0.9,

            # High Quality, Disconnected
            (True, False): 0.2,

            # Low Quality, Connected
            (False, True): 1.0,

            # Low Quality, Disconnected
            (False, False): 0.3,


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
            # Connected, Connected, Connected
            (True, True, True): 0.9,

            # Connected, Connected, Disconnected
            (True, True, False): 1.0,

            # Connected, Disconnected, Connected
            (True, False, True): 0.7,

            # Connected, Disconnected, Disconnected
            (True, False, False): 0.8,

            # Disconnected, Connected, Connected
            (False, True, True): 0.2,

            # Disconnected, Connected, Disconnected
            (False, True, False): 0.2,

            # Disconnected, Disconnected, Connected
            (False, False, True): 0.0,

            # Disconnected, Disconnected, Disconnected
            (False, False, False): 0.0,


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
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        #
        #
        #
        # TODO
        #
        #
        #
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################
        ####################################################################

        cpt = {
            # Strategic, Suitable, Suitable, Within
            (True, True, True, True): 0.5,

            # Strategic, Suitable, Suitable, Outside
            (True, True, True, False): 0.0,

            # Strategic, Suitable, Unsuitable, Within
            (True, True, False, True): 0.5,

            # Strategic, Suitable, Unsuitable, Outside
            (True, True, False, False): 0.0,

            # Strategic, Unsuitable, Suitable, Within
            (True, False, True, True): 0.5,

            # Strategic, Unsuitable, Suitable, Outside
            (True, False, True, False): 0.0,

            # Strategic, Unsuitable, Unsuitable, Within
            (True, False, False, True): 0.5,

            # Strategic, Unsuitable, Unsuitable, Outside
            (True, False, False, False): 0.0,

            # Ineffective, Suitable, Suitable, Within
            (False, True, True, True): 0.5,

            # Ineffective, Suitable, Suitable, Outside
            (False, True, True, False): 0.0,

            # Ineffective, Suitable, Unsuitable, Within
            (False, True, False, True): 0.5,

            # Ineffective, Suitable, Unsuitable, Outside
            (False, True, False, False): 0.0,

            # Ineffective, Unsuitable, Suitable, Within
            (False, False, True, True): 0.5,

            # Ineffective, Unsuitable, Suitable, Outside
            (False, False, True, False): 0.0,

            # Ineffective, Unsuitable, Unsuitable, Within
            (False, False, False, True): 0.5,

            # Ineffective, Unsuitable, Unsuitable, Outside
            (False, False, False, False): 0.0,


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
            # Identified, Connected, Suitable
            (True, True, True): 1.0,

            # Identified, Connected, Unsuitable
            (True, True, False): 0.8,

            # Identified, Disconnected, Suitable
            (True, False, True): 0.9,

            # Identified, Disconnected, Unsuitable
            (True, False, False): 0.7,

            # Not Identified, Connected, Suitable
            (False, True, True): 0.6,

            # Not Identified, Connected, Unsuitable
            (False, True, False): 0.0,

            # Not Identified, Disconnected, Suitable
            (False, False, True): 0.5,

            # Not Identified, Disconnected, Unsuitable
            (False, False, False): 0.0,


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
            # Suitable, Present
            (True, True): 0.9,

            # Suitable, Not Present
            (True, False): 1.0,

            # Unsuitable, Present
            (False, True): 1.0,

            # Unsuitable, Not Present
            (False, False): 0.3,


        }
        p = cpt[(habitat_features, species_of_interest)]
        if biotic_conditions:
            return p
        else:
            return 1.0 - p
    

    def f_habitat_features(intact_floodplain_forest, cold_water_refugia, other, habitat_features):
        cpt = {
            # Intact, Exists, Suitable
            (True, True, True): 1.0,

            # Intact, Exists, Not Suitable
            (True, True, False): 0.9,

            # Intact, Does not exist, Suitable
            (True, False, True): 0.9,

            # Intact, Does not exist, Not Suitable
            (True, False, False): 0.6,

            # Missing, Exists, Suitable
            (False, True, True): 0.9,

            # Missing, Exists, Not Suitable
            (False, True, False): 0.6,

            # Missing, Does not exist, Suitable
            (False, False, True): 0.6,

            # Missing, Does not exist, Not Suitable
            (False, False, False): 0.4,


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
        f_cost_benefit,
        f_property_value,
        f_contamination_or_hazardous_waste,
        f_public_perception,
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
            cost_benefit = levels,
            property_value = levels,
            contamination_or_hazardous_waste = levels,
            public_perception = levels,
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
    property_value = 0.5,
        contamination_or_hazardous_waste = 0.5,
        public_perception = 0.5,
        water_rights = 0.5,
        surrounding_ownership = 0.5,
        structures = 0.5,
        dams = 0.5,
        road_crossings = 0.5,
        levies = 0.5,
        bridges = 0.5,
        surrounding_land_use = 0.5,
        depth = 0.5,
        circumference = 0.5,
        surface_area = 0.5,
        bank_slope = 0.5,
        restorable_substrate = 0.5,
        contamination = 0.5,
        slope_distance_to_river = 0.5,
        adjacent_river_depth = 0.5,
        pit_adjacent_levees = 0.5,
        fill_material_availability = 0.5,
        site_accessibility = 0.5,
        continuing_property_access = 0.5,
        material_availability = 0.5,
        channel_mobility = 0.5,
        infrastructure_constraints = 0.5,
        substrate = 0.5,
        water_quality = 0.5,
        downstream = 0.5,
        upstream = 0.5,
        on_property = 0.5,
        location_in_floodplain = 0.5,
        width = 0.5,
        gradient = 0.5,
        within_x_year_floodplain = 0.5,
        identified_in_conservation_plan = 0.5,
        relationship_to_protected_areas = 0.5,
        intact_floodplain_forest = 0.5,
        cold_water_refugia = 0.5,
        other = 0.5,
        species_of_interest = 0.5,)

    for k,v in user_data.items():
        if prob.has_key(k):
            prob[k] = v

    return net.query()[('suitability', True)]

if __name__ == "__main__":
    user_data = {
        'property_value': 0.5,
        'contamination_or_hazardous_waste': 0.5,
        'public_perception': 0.5,
        'water_rights': 0.5,
        'surrounding_ownership': 0.5,
        'structures': 0.5,
        'dams': 0.5,
        'road_crossings': 0.5,
        'levies': 0.5,
        'bridges': 0.5,
        'surrounding_land_use': 0.5,
        'depth': 0.5,
        'circumference': 0.5,
        'surface_area': 0.5,
        'bank_slope': 0.5,
        'restorable_substrate': 0.5,
        'contamination': 0.5,
        'slope_distance_to_river': 0.5,
        'adjacent_river_depth': 0.5,
        'pit_adjacent_levees': 0.5,
        'fill_material_availability': 0.5,
        'site_accessibility': 0.5,
        'continuing_property_access': 0.5,
        'material_availability': 0.5,
        'channel_mobility': 0.5,
        'infrastructure_constraints': 0.5,
        'substrate': 0.5,
        'water_quality': 0.5,
        'downstream': 0.5,
        'upstream': 0.5,
        'on_property': 0.5,
        'location_in_floodplain': 0.5,
        'width': 0.5,
        'gradient': 0.5,
        'within_x_year_floodplain': 0.5,
        'identified_in_conservation_plan': 0.5,
        'relationship_to_protected_areas': 0.5,
        'intact_floodplain_forest': 0.5,
        'cold_water_refugia': 0.5,
        'other': 0.5,
        'species_of_interest': 0.5,}

    print main(user_data)

