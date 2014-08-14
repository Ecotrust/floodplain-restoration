from __future__ import print_function
import itertools
import re
from bayesian.bbn import build_bbn


def format_p(x, round=False):
    if round:
        return "%0.2f" % x
    else:
        return str(x)


class BeliefNetwork:
    """
    Example usage

    bn = BeliefNetwork.from_bif('cancer.bif')
    res = bn.query(
        inputnodes={
            'Smoker': ('smoker', 1.0),
            'Pollution': ('polluted', 1.0)
        }, 
        outputnodes=(
            ('Cancer', 'True')
        )
    )
    """

    def __init__(self, variables, probabilities):
        self.variables = variables
        self.probabilities = probabilities

    def __eq__(self, other): 
        return (
            self.variables == other.variables and
            self.probabilities == other.probabilities
        )

    @property 
    def is_valid(self):
        if sorted(self.variables.keys()) != sorted(self.probabilities.keys()):
            return (False, 'variables and probabilities must have same keys')
        return (True, 'valid')

    def query(self,  inputnodes=None, outputnodes=None):
        net = self.net(inputnodes)
        qr = net.query()
        if outputnodes:
            res = []
            for onode in outputnodes:
                res.append(qr[onode])
        else:
            res = qr

        return res

    def net(self, inputnodes=None):
        function_list = list(self.functions(inputnodes=inputnodes))
        net = build_bbn(
            function_list,
            domains=self.variables
        )
        return net

    def functions(self, inputnodes=None):
        if inputnodes is None:
            inputnodes = []

        for name, prob in self.probabilities.items():

            cpt = prob['cpt'].copy()

            # Set inputnodes 
            # (only applies to variables without conditional tables)
            for varname, inv in inputnodes.items():
                if varname != name:
                    continue
                if prob['given']:
                    raise Exception(
                     "Can't specify nodes with conditionals; {}".format(varname))
                state = inv[0]
                assert state in self.variables[varname]
                value = inv[1]
                assert value <= 1.0
                cpt[(state,)] = value

                # aportion the rest to remaining states
                totalleft = 1.0 - value
                remaining = [v for v in self.variables[varname] if v != state]
                for rv in remaining:
                    cpt[(rv,)] = totalleft/len(remaining)
            
            if prob['given']:
                given = prob['given']
            else:
                given = []
            argspec = given + [name]

            # evaling a function string? yep I'm going there
            # alternatively, i could make cpt a closure ...
            # but didn't have much luck with this method
            # def func(*args):
            #     print(cpt)
            #     print(args)
            #     return cpt[args]
            funcstr = """def f_{name}(*args):
    data = {cpt}
    return data[args]
            """.format(
                name=name,
                # args=", ".join(argspec),
                cpt=cpt
            )
            exec(funcstr)

            func = locals()["f_{}".format(name)]
            func.argspec = argspec
            yield func
  
    def to_bif(self, path, round=False):
        with open(path, 'w') as fh:
            fh.write("network unknown {\n}\n")

            for vname, vlevels in self.variables.items():
                fh.write("""variable %s {
  type discrete [ %d ] { %s };
})
""" % (vname, len(vlevels), ', '.join(vlevels)))

            for pname, prob in self.probabilities.items():
                if not prob['given']:
                    # prior
                    priors = []
                    for level in self.variables[pname]:
                        priors.append(prob['cpt'][(level,)])

                    prob_str = """probability ( %s ) {
  table %s;
}
""" % (pname, ", ".join([format_p(x, round=round) for x in priors]))

                else:
                    # conditional
                    prob_str = "probability ( %s | %s ) {\n" % (
                        pname,
                        ", ".join(prob['given'])
                    )

                    given_levels = list(itertools.product(*[
                        self.variables[x] for x in prob['given']
                    ]))

                    for given in given_levels:
                        prob_str += "  (%s) " % (', '.join(given), )
                        vals = []
                        for dlevel in self.variables[pname]:
                            k = tuple(list(given) + [dlevel])
                            vals.append(prob['cpt'][k])
                        prob_str += "%s;\n" % (', '.join([format_p(x, round=round)
                                                          for x in vals]))

                    prob_str += "}\n"
                fh.write(prob_str)
        return path



    @classmethod
    def from_bif(cls, bif):
        """ Parts of this method derived from 
        https://raw.githubusercontent.com/eBay/bayesian-belief-networks/master/bayesian/examples/bif/bif_parser.py

        Copyright 2013 eBay Software Foundation
        Under the apache license (http://www.apache.org/licenses/LICENSE-2.0)
        """
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
                    dd = dict(zip([(x,) for x in variables[in_prior]],
                                  map(float, match.group(1).split(", "))))
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

        bn = cls(variables, dictionary)
        return bn
