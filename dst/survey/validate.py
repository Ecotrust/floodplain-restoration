from bbn import BeliefNetwork
from django.conf import settings

class SystemCheckError(Exception):
    pass
    
def systemcheck():
    bn = BeliefNetwork.from_bif(settings.BBN_BIF)

    # Valid BBN?
    valid = bn.is_valid
    if not valid[0]:
        raise SystemCheckError("BBN from {} is not valid:\n  {}".format(
            settings.BBN_BIF, valid[1]))

    # the terminal nodes of the belief network match questions
    terminalnode_names = []
    for name, prob in bn.probabilities.items():
        if not prob['given']:  # terminal node
            terminalnode_names.append(name)

    from survey.models import Question
    question_names = [q.name for q in Question.objects.all()]

    tnn = set(terminalnode_names)
    qn = set(question_names)
        
    diff = list(qn - tnn)
    if len(diff) > 0:
        raise SystemCheckError("Extraneous questions without terminal nodes:\n\t%s" % diff)

    diff = list(tnn - qn)
    if len(diff) > 0:
        raise SystemCheckError("Terminal nodes missing questions:\n\t%s" % diff)

    # Make sure choices are valid; 
    # first choice in bn.variables must have value of 1.0
    # all others must have values bt 0 and 1
    for question in Question.objects.all():
        first = bn.variables[question.name][0]
        for choice in question.choices:
            if choice['value'] < 0.0 or choice['value'] > 1.0:
                raise SystemCheckError("`{}` has invalid values in choices "\
                    "(must be 0 to 1)".format(question.name))

            if choice['choice'] == first and choice['value'] != 1.0:
                raise SystemCheckError("`{}` has invaid values in choices; "\
                    "`{}` must be 1.0".format(question.name, first))
