def ext_to_letter(k):
    print("computing letter of",k)
    return chr(ord('a')+int(k))

class TransitionalEquation():

    def __init__(self):

        # type of equation
        self.type = "TRANSITIONAL"
        
        # name of the main table of the equation
        self.main_name = ""
        self.latex_name = ""

        # table indices
        self.indices = set([])

        # new variable (marginalization)
        self.marginalization = set([])

        # sub-terms: list of other equations
        self.subterms = []

    def latex_print(self, letter_table, ext_to_letter):

        for e in self.indices:
            if e not in letter_table.keys():
                letter_table[e] = ext_to_letter[e]

        res = ""
        res += self.latex_name+'['
        res += ','.join([letter_table[e] for e in self.indices])
        res += ']'
        return res

class CliqueCaseHelix():

    def __init__(self):

        # tupe
        self.type = "CLIQUE"

        # table indices
        self.indices = []
        
        # name of the main table of the equation
        self.main_name = ""
        self.latex_name = ""

    def latex_print(self, letter_table, ext_to_letter):

        for e in self.indices:
            if e not in letter_table.keys():
                letter_table[e] = ext_to_letter[e]

        res = ""
        res += self.latex_name+'['
        res += ','.join([letter_table[e] for e in self.indices])
        res += ']'
        return res

class DiagCaseHelix():

    def __init__(self):

        # type
        self.type = "DIAG"

        # name of the main table of the equation
        self.main_name = ""
        self.latex_name = ""

        # the ones before the |
        self.variable_indices = []

        # absent indices
        self.absent_indices = []

        # to connect the two
        self.corresponding_variable = {}

        # the ones after the | (the constraints, constant)
        self.constant_indices = []

        # whether the variable indices get a +1 (external bp) or -1 (internal)
        self.increments = []

        # the recursion terms - "children" equations
        self.subterms = []

        # boolean for in which sense it goes
        self.inward = True

        # substitution matrix for subterms
        self.subs_table = {}

        # diag helix canonical representation: two bags
        self.first_bag = '-1'
        self.second_bag = '-1'

    def latex_print(self, letter_table, ext_to_letter):

        for e in list(self.variable_indices)+list(self.constant_indices):
            if e not in letter_table.keys():
                letter_table[e] = ext_to_letter[e]

        res = self.latex_name+'['
        res += ','.join([letter_table[e] for e in self.variable_indices])
        res += '|'
        res += ','.join([letter_table[e] for e in self.constant_indices])
        res += ']'

        return res
