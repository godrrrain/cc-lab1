import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz-11.0.0-win64/bin/'

from graphviz import Digraph
from typing import Dict, List, Set
import copy
import numpy as np

FDA_table = Dict[str, List[int]]
NFDA_table = Dict[str, List[List[int]]]
EPSILON = 'ε'


class CharCantBeAccepted(Exception):
    pass


class Automata:
    def accepts(self, input_string):
        raise NotImplementedError()

    def num_of_states(self):
        raise NotImplementedError()

    def alphabet(self):
        raise NotImplementedError()
    
    def draw(self):
        raise NotImplementedError()


class NDA(Automata):
    def __init__(self, table: NFDA_table, final_states):
        self.table = table
        self.final_states = final_states

        self.states = None

    def next_state(self, state, char):
        if char not in self.table:
            raise CharCantBeAccepted
        return self.table[char][state]

    def forward(self, old_state, char):
        new_state = set()
        for state in old_state:
            new_state.update(self.next_state(state, char))
            if EPSILON in self.table.keys():
                new_state.update(sum([self.eps_close(s) for s in new_state], []))
        return list(new_state)

    def add_transition(self, start, char, finish):
        if char not in self.table:
            self.table[char] = [[] for _ in range(self.num_of_states())]
        self.table[char][start].append(finish)

    def accepts(self, input_string):
        self.states = self.eps_close(0)
        try:
            for c in input_string:
                self.states = self.forward(self.states, c)
            for state in self.states:
                if set(self.eps_close(state)).intersection(self.final_states):
                    return True
            return False
        except CharCantBeAccepted:
            return False

    def num_of_states(self):
        return len(list(self.table.values())[0])

    def copy(self):
        new_table = copy.deepcopy(self.table)
        new_final = copy.deepcopy(self.final_states)
        return NDA(new_table, new_final)

    def draw(self, type):
        dot = Digraph()
        
        for char, state_list in self.table.items():
            for i, s in enumerate(state_list):
                if len(s) != 0:
                    for t in s:
                        dot.edge(str(i), str(t), char)

        for i in self.final_states:
            dot.node(str(i),shape='cds')
        
        dot.edge('START', '0')
        
        if type == 1:
            dot.render('НКА', view=True)
        if type == 2:
            dot.render('ДКА', view=True)
        if type == 3:
            dot.render('МДКА', view=True)


    def eps_close(self, state: int) -> List[int]:
        if EPSILON not in self.table.keys():
            return [state]
        visited = []
        active = [state]
        while len(active) != 0:
            new_active = []
            for s in active:
                new_active.extend(self.table[EPSILON][s])
            visited = list(set(visited + active))
            active = list(set(new_active).difference(visited))
        return visited

    def alphabet(self):
        return list(self.table.keys())

class DA(Automata):
    def __init__(self, table: FDA_table, final_states: List[int]):
        self.table = table
        self.final_states = final_states
        proxy_table = {}
        for char, states in table.items():
            proxy_table[char] = [[state] if state is not None else [] for state in states]
        self.proxy = NDA(proxy_table, final_states)

    def accepts(self, input_string: str) -> bool:
        return self.proxy.accepts(input_string)

    def draw(self, type):
        self.proxy.draw(type)

    def num_of_states(self):
        return self.proxy.num_of_states()

    def alphabet(self):
        return self.proxy.alphabet()
    
    def model_check(self, check_str):
        check_arr = [*check_str]
        size = len(self.table[list(self.table.keys())[0]])
        Ssize = len(self.table)
        true_table = np.full((size,size,Ssize), None)
        j = 0
        for char, state_list in self.table.items():
            for i, s in enumerate(state_list):
                if s != None:
                    true_table[i][s][j] = char
            j += 1
        
        carette = 0
        
        while(True):
            if not check_arr:
                break
            for i in range(size):
                if check_arr:
                    arr = []
                    for a in true_table[carette]:
                        for b in a:
                            arr.append(b)
                    if check_arr[0] not in arr:
                            return "NO"
                    for symbol in true_table[carette][i]:
                        if check_arr[0] == symbol:
                            check_arr.pop(0)
                            carette = i
                            break

        if not check_arr and carette in self.final_states:
            return "YES"
        else:
            return "NO"