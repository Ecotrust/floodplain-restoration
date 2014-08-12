import itertools
import re

class BeliefNetwork:
    def __init__(self, variables, probabilities):
        self.variables = variables
        self.probabilities = probabilities

    def pprint(self):
        """
        {'Cancer': ['True', 'False'],
         'Dyspnoea': ['True', 'False'],
         'Pollution': ['low', 'high'],
         'Smoker': ['True', 'False'],
         'Xray': ['positive', 'negative']}
        {'Cancer': {'cpt': {('high', 'False', 'False'): 0.98,
                            ('high', 'False', 'True'): 0.02,
                            ('high', 'True', 'False'): 0.95,
                            ('high', 'True', 'True'): 0.05,
                            ('low', 'False', 'False'): 0.999,
                            ('low', 'False', 'True'): 0.001,
                            ('low', 'True', 'False'): 0.97,
                            ('low', 'True', 'True'): 0.03},
                    'given': ['Pollution', 'Smoker']},
         'Dyspnoea': {'cpt': {('False', 'False'): 0.7,
                              ('False', 'True'): 0.3,
                              ('True', 'False'): 0.35,
                              ('True', 'True'): 0.65},
                      'given': ['Cancer']},
         'Pollution': {'cpt': "{'high': 0.1, 'low': 0.9}", 'given': None},
         'Smoker': {'cpt': "{'True': 0.3, 'False': 0.7}", 'given': None},
         'Xray': {'cpt': {('False', 'negative'): 0.8,
                          ('False', 'positive'): 0.2,
                          ('True', 'negative'): 0.1,
                          ('True', 'positive'): 0.9},
                  'given': ['Cancer']}}"""

        import pprint
        pprint.pprint(self.variables)  
        pprint.pprint(self.probabilities)

    @staticmethod
    def from_bif(bif):
        variable_pattern = re.compile(
            r"  type discrete \[ \d+ \] \{ (.+) \};\s*")
        prior_probability_pattern_1 = re.compile(
            r"probability \( ([^|]+) \) \{\s*")
        prior_probability_pattern_2 = re.compile(
            r"  table (.+);\s*")
        conditional_probability_pattern_1 = (re.compile(
            r"probability \( (.+) \| (.+) \) \{\s*"))
        conditional_probability_pattern_2 = re.compile(
            r"  \((.+)\) (.+);\s*")


        variables = {}
        dictionary = {}

        with open(bif, 'r') as fh:
            in_var = False
            in_cond = False
            in_prior = False
            in_network = False
            given = False
            for line in fh: 
                if line.startswith("network"):
                    in_network = True
                    continue

                if in_network and line.startswith("}"):
                    in_network = False
                    continue

                if in_var:
                    "  type discrete [ 2 ] { True, False };"
                    match = variable_pattern.match(line)
                    levels = [x.strip() for x in match.group(1).split(",")]
                    variables[in_var] = levels
                    in_var = False
                    continue
        
                if line.startswith('variable'):
                    in_var = line.split(" ")[1]
                    continue

                if in_prior:
                    match = prior_probability_pattern_2.match(line)
                    dd = str(dict(zip(variables[in_prior],
                                  map(float, match.group(1).split(", ")))))
                    dictionary[in_prior] = {'cpt': dd, 'given': None}
                    in_prior = False
                    continue

                match = prior_probability_pattern_1.match(line)
                if match:
                    in_prior = match.group(1)
                    continue


                match = conditional_probability_pattern_1.match(line)
                if match:
                    # Conditional probabilities
                    in_cond = match.group(1)
                    given = [x.strip() for x in match.group(2).split(",")]
                    dictionary[in_cond] = {'given': given,
                                           'cpt': {}}
                    continue

                if in_cond and line.startswith("}"):
                    in_cond = False
                    given = False
                    continue

                if in_cond:
                    match = conditional_probability_pattern_2.match(line)
                    given_values = match.group(1).split(", ")
                    dd = {}
                    for value, prob in zip(
                            variables[in_cond],
                            map(float, match.group(2).split(", "))):
                        dictionary[in_cond]['cpt'][tuple(given_values + [value])] = prob


        bn = BeliefNetwork(variables, dictionary)
        return bn





if __name__ == "__main__":
    bn = BeliefNetwork.from_bif('cancer.bif')
    bn.pprint()

 



