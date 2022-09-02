from tree_of_bags import TreeOfBags

class TreeOfEquations(TreeOfBags):

    def __init__(self):
        """
        For clarity, all attributes specific to TreeOfEquations
        (other attributes are inherited from TreeOfBags) are set here to
        empty/dummy values. No other attributes will be defined in the methods.
        """
        super().__init__()

        # will store for each helix label the set of bags representing the helix
        self.representation_bags = {}

        # for a bag, tells you for which helix it is part of the representation. 
        self.which_helix = {}

        # helices
        self.helices = []

        # all extremities: the set of all anchors, for practicality
        self.all_extremities = set([])

        # helix extremities: gives you the set of extremities associated to an helix
        self.helix_extremities = {}

        # const part: the anchors present in all bags representing an helix (for diag case mostly)
        self.const_part = {}

        # DP table names: associate a letter to each bag. The only bags that are not given
        # a letter are the "second bags" representing a diag case helix.
        self.dp_table_names = {}
        self.dp_table_latex_snips = {}

        # extremity (position/integer) to variable name (latin letter)
        self.ext_to_letter = {}

    def set_ext_to_letter(self):
        for k, e in enumerate(sorted(list(self.all_extremities),key=lambda x: int(x))):
            self.ext_to_letter[e] = chr(ord('a')+k)

    def set_dp_table_names(self):

        cnt = 0 # alphabet/variable increment variable
        cnt_col = 0 # color increment variable (to match colors of other drawings)

        for prev, u in self.dfs_edge_iterator():
            if not u[:1]=='H':
                self.dp_table_names[u] = self.num_to_letters(cnt)
                self.dp_table_latex_snips[u] = self.num_to_letters(cnt)
                cnt += 1
            else:
                if set(self.helix_extremities[self.which_helix[u]]).issubset(set(self.bag_content[prev])):
                # clique
                    self.dp_table_names[u] = "CLIQUE"
                    self.dp_table_latex_snips[u] = "\\colorbox{c"+u.split('-')[0][1:]+"}{$C_{\\boxtimes}$}"
                    cnt_col += 1
                else:
                # diag: only setting the letter for the first bag out of the two representating of the helix.
                    if prev.split('-')[0]!=u.split('-')[0]:
                        self.dp_table_names[u] = self.num_to_letters(cnt)
                        self.dp_table_latex_snips[u] = "\\colorbox{c"+u.split('-')[0][1:]+"}{$"+self.num_to_letters(cnt)+"$}"
                        cnt += 1
                        cnt_col += 1

    def set_helices(self, helices):
        """
        sets a lot of fields: helices, helix_extremities, all_extremities, representation_bags
        and which_helix
        
        Input:
            - helices: lines of helix annotation files. typically open(snakemake.input.helix).readlines()
        """
        self.helices = helices

        for helixline in self.helices:

            # helix info extraction
            label = helixline.split(' ')[0]
            extremities = [c.replace(' ','') for c in helixline.split('(')[1].split(')')[0].split(',')]
            
            # set helix_extremities
            self.helix_extremities[label] = extremities
            self.all_extremities = self.all_extremities.union(extremities)
           
            # set representation_bags and which helix
            self.representation_bags[label] = []
            print(label)
            for u in self.dfs_bag_iterator():
                print(u)
                if u.split('-')[0]==label:
                    self.representation_bags[label].append(u)
                    self.which_helix[u] = label
            # set const part
            print(self.representation_bags[label])
            self.const_part[label] =set.intersection(*[set(self.bag_content[u]) for u in self.representation_bags[label]])

    @staticmethod
    def num_to_letters(cnt):
        if cnt < 26:
            return chr(ord('a') + cnt).upper() #'\\colorbox{c'+str(cnt)+'}{'+chr(ord('a') + cnt).upper()+'}'
        else:
            return chr(ord('a') + int(cnt/26)).upper()+chr(ord('a') + int(cnt%26)).upper()
         

    def contract_to_skeleton(self):
        """
        Contracts each helix representation to 2 bags in the diag
        case and one bag in the clique case.
        """

        for helixline in self.helices:
            label = helixline.split(' ')[0]
            extremities = [c.replace(' ','') for c in helixline.split('(')[1].split(')')[0].split(',')]

            queue = [('-1',self.root)]
            while len(queue) > 0:
                prev,u = queue.pop()

                if u.split('-')[0]==label:
                    if not set(extremities).issubset(set(self.bag_content[prev])):
                    # diag case
                        keep_going = True
                        while keep_going:
                            keep_going = False
                            for v in self.bag_adj[u]:
                                if v.split('-')[0]==label:
                                    for w in self.bag_adj[v]:
                                        if w!=u and w.split('-')[0] == label:
                                            # grand-child is still in helix, contracting v into u
                                            self.bag_adj[u] = [bag for bag in self.bag_adj[u] if bag!=v]+[w]
                                            self.bag_adj[w] = [bag for bag in self.bag_adj[w] if bag!=v]+[u]
                                            keep_going = True

                    else: 
                    # clique case    
                        self.bag_adj[u] = []



                for v in self.bag_adj[u]:
                    if v!=prev:
                        queue.append((u,v))

    def filter_anchors(self):
        """
        Processes the bags so that they contain anchors (helix extremities only)
        """
        for u in self.dfs_bag_iterator():
            self.bag_content[u] = [vert for vert in self.bag_content[u] if vert in self.all_extremities]

    def extract_diag_equation(self, parent, diag_first_bag):

        # if diag_first_bag is indeed the first bag of a diag case helix representation,
        # then the following asserts should be true
        print(parent, diag_first_bag)
        assert(parent.split('-')[0]!=diag_first_bag.split('-')[0])

        # return object
        equation = DiagCaseHelix()
        equation.first_bag = diag_first_bag

        # figuring out what are the variable indices of the equations (before the |)
        absent_ex = (set(self.helix_extremities[self.which_helix[diag_first_bag]])-set(self.bag_content[parent])).pop() 
        sorted_exs = sorted(self.helix_extremities[self.which_helix[diag_first_bag]], key=lambda x: int(x))
        indices = sorted(list(set(self.helix_extremities[self.which_helix[diag_first_bag]]) - set([absent_ex, partner(absent_ex, sorted_exs)])),key=lambda x: int(x))
        if absent_ex in sorted_exs[1:2]:
            equation.inward = True
        else:
            equation.inward = False

        equation.increments = [increment(e, sorted_exs) for e in indices]

        # setting variable indices: 
        equation.variable_indices = [self.ext_to_letter[e] for e in indices]
        
        # will be used for putting indices in children tables.
        local_index_label = {}

        for i in indices:
            local_index_label[i] = self.ext_to_letter[i]
            local_index_label[subs(i, sorted_exs)] = self.ext_to_letter[i]

        for e in sorted(self.const_part[self.which_helix[diag_first_bag]], key=lambda x : int(x)):
            if e in indices:
            # if const part is also one of the indices: add a prime '
                equation.constant_indices.append(self.ext_to_letter[e]+"'")
                local_index_label[e] = self.ext_to_letter[e]+"'"
            else:
                equation.constant_indices.append(self.ext_to_letter[e])
                local_index_label[e] = self.ext_to_letter[e]

        print("diag first bag", diag_first_bag)
        print(self.bag_adj[diag_first_bag])
        second_helix_bag = [v for v in self.bag_adj[diag_first_bag] if v!=parent].pop()
        equation.second_bag
        if len(self.bag_adj[second_helix_bag]) >= 2:
            normal_childs = []
            normal_child_letters = {}
            diag_childs = []
            diag_child_letters = {}
            diag_child_const_parts = {}
            clique_childs = []
            clique_childs_letters = {}
            for child_table in self.bag_adj[second_helix_bag]:
                if child_table!=diag_first_bag:

                    # sort
                    child_indices = sorted(self.bag_content[child_table], key=lambda x:int(x))

                    # intersection with second helix case
                    child_indices = [i for i in child_indices if i in self.bag_content[second_helix_bag]] 

                    if child_table[0]=='H' and not set(self.helix_extremities[self.which_helix[child_table]]).issubset(set(self.bag_content[second_helix_bag])):
                    # diag case below

                        diag_childs.append(child_table)

                        absent_ex = (set(self.helix_extremities[self.which_helix[child_table]])-set(self.bag_content[second_helix_bag])).pop() 
                        sorted_exs = sorted(self.helix_extremities[self.which_helix[child_table]], key=lambda x: int(x))
                        child_indices = sorted(list(set(self.helix_extremities[self.which_helix[child_table]]) - set([absent_ex, partner(absent_ex, sorted_exs)])),key=lambda x: int(x))
                        child_letters = [local_index_label[i] for i in child_indices]
            
                        diag_child_letters[child_table] = child_letters

                        child_const = [local_index_label[i] for i in sorted(self.const_part[self.which_helix[child_table]],key=lambda x : int(x))]
            
                        diag_child_const_parts[child_table] = child_const

                    elif child_table[0]=='H' and set(self.helix_extremities[self.which_helix[child_table]]).issubset(set(self.bag_content[second_helix_bag])):
                        clique_childs.append(child_table)
                        child_letters = [local_index_label[i] for i in child_indices]
                        clique_childs_letters[child_table] = child_letters
                    else:
                    # normal table below
                        normal_childs.append(child_table)
                        child_letters = [local_index_label[i] for i in child_indices]
                        normal_child_letters[child_table] = child_letters

            for child_table in normal_childs:
                child_letters = normal_child_letters[child_table]
                for k, e in enumerate(child_letters):
                    if e==equation.variable_indices[1]:
                        child_letters[k]=e+'+1'
                term = self.dp_table_latex_snips[child_table]+"'["+",".join(child_letters)+']'
                equation.subterms.append(term)
            for child_table in diag_childs:
                child_letters = diag_child_letters[child_table]
                for k, e in enumerate(child_letters):
                    if e==equation.variable_indices[1]:
                        child_letters[k]=e+'+1'
                child_const = diag_child_const_parts[child_table]
                term = self.dp_table_latex_snips[child_table]+"'["+",".join(child_letters)+'|'+",".join(child_const)+']'
                equation.subterms.append(term)
            for child_table in clique_childs:
                child_letters = clique_childs_letters[child_table]
                for k, e in enumerate(child_letters):
                    if e==equation.variable_indices[1]:
                        child_letters[k]=e+'+1'
                child_letters[1] =  child_letters[1]+'-1'
                child_letters[3] =  child_letters[3]+'-1'
                term = self.dp_table_latex_snips[child_table]+"'["+",".join(child_letters)+']'
                equation.subterms.append(term)

        return equation

        
class DiagCaseHelix():

    def __init__(self):

        # the ones before the |
        self.variable_indices = []

        # the ones after the | (the constraints, constant)
        self.constant_indices = []

        # whether the variable indices get a +1 (external bp) or -1 (internal)
        self.increments = []

        # the recursion terms - "children" equations
        self.subterms = []

        # boolean for in which sense it goes
        self.inward = True

        # diag helix canonical representation: two bags
        self.first_bag = '-1'
        self.second_bag = '-1'


def increment(e, sorted_exs):
    """
    depending on wheter internal
    or external extremal base pair,
    the increment in the dp equations
    that update variables are not the
    same.
    """
    if e==sorted_exs[0]:
        return '+1'
    if e==sorted_exs[1]:
        return '-1'
    if e==sorted_exs[2]:
        return '+1'
    if e==sorted_exs[3]:
        return '-1'

def partner(e, sorted_ext):
    """
    in the standard (i,ip,jp,j) representation
    of helices that we use, 
    with i < ip < jp < j, i.e.
    i,j the outer arc and ip,jp the inner arc,
    i and j are partners, 
    and ip, jp as well.
    """
    if e==sorted_ext[0]:
        return sorted_ext[3]
    if e==sorted_ext[1]:
        return sorted_ext[2]
    if e==sorted_ext[3]:
        return sorted_ext[0]
    if e==sorted_ext[2]:
        return sorted_ext[1]

def subs(e, sorted_exs):
    """
    In the diag case, i is incrementally
    transformed into ip, or vice-versa.
    same for j and jp.
    subs: i -> ip, ip -> o, jp ->j, j->jp
    """
    if e==sorted_exs[0]:
        return sorted_exs[1]
    if e==sorted_exs[1]:
        return sorted_exs[0]
    if e==sorted_exs[2]:
        return sorted_exs[3]
    if e==sorted_exs[3]:
        return sorted_exs[2]
