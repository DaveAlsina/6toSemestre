
class ExampleGrammars():


    def __init__(self):

        self.grammars = {

            # grammar of the form:
            # a^{i} b^{j} c^{i} d^{j}, same number of a's and c's, 
            # and same number of b's and d's, where i and j are integers.

            1:    [('S', 'aWd'), ('W', 'aWd'), ('W', 'V'),
                   ('V', 'bVc'), ('V', 'X'), ('X', 'bc')],

            # grammar of the form:
            # a^{i} b^{i}, that is, same number of a's and b's.
            # where i is an integer.
            2:    [('S', 'aSb'), ('S', 'AB'),
                   ('A', 'a'), ('B', 'b')], 

            # grammar of the form:
            # a^{i} b^{j}, i>j>0, that means a's are more than b's.
            3:    [('S', 'aR'), ('R', 'aRb'), 
                   ('R', 'aR'), ('R', 'aW'), ('W', 'b')]


        }

    def get_grammar(self, grammar_num):

        return self.grammars[grammar_num]



