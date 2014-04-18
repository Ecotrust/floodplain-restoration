import itertools

suitability = {
    'Landscape': {
        'Conservation value': {
            'Relationship to protected areas': None,
            'Identified in conservation plan': None,
            'Biotic conditions': {
                'Habitat features': {
                    'Cold water refugia': None,
                    'Intact floodplain forest': None,
                    'Other': None
                },
                'Species of interest': None
            }
        },
        'Abiotic conditions': {
            'Water quality': None,
            'Connectivity barriers': {
                'Upstream': None,
                'Downstream': None,
                'On property': None,
            }
        },
        'Geomorphic Controls': {
            'Channel mobility': None,
            'Material availability': None,
            'Substrate': None,
            'Infrastructure constraints': None,
        },
        'Floodplain characteristics': {
            'Gradient': None,
            'Width': None,
            'Within X-year floodplain': None,
            'Location in floodplain': None,
        }
    },
    'Socio-Economic': {
        'Cost benefit': {
            'Public perception/support': None,
            'Contamination/Hazardous waste': None,
            'Property value': None,
        },
        'Threats to other areas/Permittability': {
            'Surrounding ownership': None,
            'Surrounding land use': None,
            'Water rights': None,
            'Infrastructure': {
                'Levies': None,
                'Dams': None,
                'Structures': None,
                'Bridges': None,
                'Road crossings': None,
            }
        },
    },
    'Site': {
        'Practical property-level restorability': {
            'Continuing property access': None,
            'Fill material availability': None,
            'Site accessibility': None,
        },
        'Pit restorability': {
            'Contamination': None,
            'Substrate': None,
            'Slope distance to river': None,
            'Pit geometry': {
                'Surface area': None,
                'Circumference': None,
                'Bank slope': None,
                'Depth': None,
                'Shoreline complexity': None,
            },
            'Adjacent river depth': None,
            'Pit-adjacent levees': None,
        },

    }
}

LEVELS = ['High', 'Low']

def expand(node, decision):
    """ recursive """
    if not node:
        return
    keys = node.keys()
    print ','.join(keys + [decision])
    aa = itertools.product(*[LEVELS] * len(keys))
    for bb in aa:
        print ','.join([str(x) for x in bb] + ["50"])
        
    print "\n" * 5

    for key in keys:
        res = expand(node[key], key)
        if res:
            print res


expand(suitability, 'Suitability')
#import ipdb; ipdb.set_trace()