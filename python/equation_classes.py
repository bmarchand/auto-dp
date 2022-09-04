def ext_to_letter(k):
    """
    Simply returns the k-th letter of the alphabet.
    """
    return chr(ord('a')+int(k))

class CommonEquationFeatures():
    """
    Basic equation class from which other equation object
    classes will inherit. 

    Its main purpose is to require the implementation 
    of some methods (for now, just latex_print, but
    in the future, c_code_print maybe ?)
    """
    def latex_print(self, letter_table, ext_to_letter):
        # request implementation of latex_print
        raise NotImplementedError('latex_print must be implemented for class '+self.__class__.__name__)

class TransitionalEquation(CommonEquationFeatures):
    """
    Class for representing 
    DP equations linked to ``transitional''
    bags (i.e. bags that are not part of a clique
    representation)

    Its fields contain all of the information 
    needed to reconstruct the equation. They
    are initialized to dummy values, and
    will be updated based on what read 
    in canonical tree decompositions.

    As any class inheriting from CommonEquationFeatures,
    it needs to implement latex_print
    """

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

class CliqueCaseHelix(CommonEquationFeatures):

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

class DiagCaseHelix(CommonEquationFeatures):

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
