from random import randint

class ExampleGrammars():


    def __init__(self):

        self.grammars = {

            # grammar of the form:
            # a^{i} b^{i}, that is, same number of a's and b's.
            # where i is an integer.
            1:    [('S', 'aSb'), ('S', 'AB'),
                   ('A', 'a'), ('B', 'b')], 

            # grammar of the form:
            # a^{i} b^{j} c^{i} d^{j}, same number of a's and c's, 
            # and same number of b's and d's, where i and j are integers.

            2:    [('S', 'aWd'), ('W', 'aWd'), ('W', 'V'),
                   ('V', 'bVc'), ('V', 'X'), ('X', 'bc')],


            # grammar of the form:
            # a^{i} b^{j}, i>j>0, that means a's are more than b's.
            3:    [('S', 'aR'), ('R', 'aRb'), 
                   ('R', 'aR'), ('R', 'aW'), ('W', 'b')],

            # grammar of the form:
            # the alphabet is {0, 1}, and the grammar is:
            # where the words are palindromes. ex: 10101, 01010, 1001, 1111, 0000 etc.
            4:    [('S', 'CA'), ('S', 'DB'), ('S', '1'), 
                   ('S', '0'), ('S', 'CC'), ('S', 'DD'),
                   ('A', 'SC'), ('B', 'SD'), ('C', '1'),
                   ('D', '0')]


        }

    def get_grammar(self, grammar_num: int):

        return self.grammars[grammar_num]


    def generate_word(self, grammar_num: int, word_interval_len: tuple):

        """
            Generates a word from a grammar. This could be done by a recursive function,
            or going through the grammar and generating a word from each rule. but
            I felt lazy enough to do it this way.
        """

        if grammar_num not in self.grammars.keys():

            print("Please select a valid grammar number")
            print("available grammars: {}".format(self.grammars.keys()))
            return None 

        ans = ""
    
        if grammar_num == 1:
            ans = self.generate_word_grammar1(word_interval_len)
        
        elif grammar_num == 2:
            ans = self.generate_word_grammar2(word_interval_len)

        elif grammar_num == 3:
            ans = self.generate_word_grammar3()

        elif grammar_num == 4:
            ans = self.generate_word_grammar4()

        return ans

    def generate_word_grammar1(self, word_interval_len: tuple) -> str:

        """
            Generates a word from the grammar 1.
        """

        i = randint(word_interval_len[0] , word_interval_len[1])

        return ("a"*i) + ("b"*i)

    def generate_word_grammar2(self, word_interval_len: tuple) -> str:


        """
            Generates a word from the grammar 2.
        """


        return 






