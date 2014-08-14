from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Checks the current system for data integrity'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        #raise CommandError('Not yet implemented')
        from bbn import BeliefNetwork
        bn = BeliefNetwork.from_bif(settings.BBN_BIF)

        # Valid BBN?
        valid = bn.is_valid
        if not valid[0]:
            raise Exception("BBN from {} is not valid:\n  {}".format(
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
            raise Exception("Extraneous questions without terminal nodes:\n\t%s" % diff)

        diff = list(tnn - qn)
        if len(diff) > 0:
            raise Exception("Terminal nodes missing questions:\n\t%s" % diff)

        # Make sure choices are valid; 
        # first choice in bn.variables must have value of 1.0
        # all others must have values bt 0 and 1
        for question in Question.objects.all():
            first = bn.variables[question.name][0]
            for choice in question.choices:
                if choice['value'] < 0.0 or choice['value'] > 1.0:
                    raise Exception("`{}` has invalid values in choices "\
                        "(must be 0 to 1)".format(question.name))

                if choice['choice'] == first and choice['value'] != 1.0:
                    raise Exception("`{}` has invaid values in choices; "\
                        "`{}` must be 1.0".format(question.name, first))


        # make sure we can query the belief network
        self.stdout.write('Successfully checked system...')
