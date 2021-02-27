import copy


class Automaton:
    pass


class Automaton:
    def __init__(self):
        self.__num_states = 0

        # elementos que compoem um automato
        self.__states = list()
        self.__alphabet = list()  # [ A, ... ]
        self.__transitions = dict()  # { (E, A*) : E+, ... }
        self.__initials = list()  # [ E, ... ]
        self.__finals = list()  # [ E, ... ]

    def mount_table(self):
        table = dict()
        for i in range(0, len(self.__states)-1):
            table[self.__states[i]] = dict()
            for j in range(0, len(self.__states)-(i+1)):
                reverse_states = list(reversed(self.__states))
                table[self.__states[i]][reverse_states[j]] = None
        return table

    def mark_trivially_not_equivalent(self, table):
        for row in table:
            for col in table[row]:
                if row in self.__initials and col not in self.__initials:
                    table[row][col] = False
                if row in self.__finals and col not in self.__finals:
                    table[row][col] = False
                if col in self.__finals and row not in self.__finals:
                    table[row][col] = False

    def print_eq_table(self, table):
        for row in table:
            print(row +" | "+ str(table[row]))

    def test_not_trivially(self, table):
        for row in table:
            for col in table[row]:
                if not table[row][col] is None:
                    for entry in self.__alphabet:
                        row_results = list()
                        col_results = list()
                        for t in self.__transitions:
                            if t[1] == entry and row in self.__transitions[t]:
                                row_results.append(t[0])
                        for t in self.__transitions:
                            if t[1] == entry and col in self.__transitions[t]:
                                col_results.append(t[0])
                        results_tuples = list()
                        for row_res in row_results:
                            for col_res in col_results:
                                if row_res!=col_res:
                                    results_tuples.append((row_res, col_res))
                        for result in results_tuples:
                            if result[0] in table:
                                if result[1] in table[result[0]]:
                                    table[result[0]][result[1]] = False
                            if result[1] in table:
                                if result[0] in table[result[1]]:
                                    table[result[1]][result[0]] = False
                        # if len(results_tuples) > 0:
                        print(entry+" -> "+row+"X"+col+" = "+str(row_results)+"X"+str(col_results)+" => "+str(results_tuples))
                        #     print("----------------------------------------------------------------------------")

    def minimize(self, afd: Automaton) -> Automaton:
        table = self.mount_table()
        self.mark_trivially_not_equivalent(table)
        self.test_not_trivially(table)
        self.print_eq_table(table)
        pass

    def add_state(self, name='', initial=False, final=False):
        self.__states.append(name)
        if initial:
            self.__initials.append(name)
        if final:
            self.__finals.append(name)
        return name

    def add_transition(self, source, word, destiny):
        if not source in self.__states:
            self.error('add_transition: source not exist')
        if not destiny in self.__states:
            self.error('add_transition: destiny not exist')
        for c in word:
            if not c in self.__alphabet:
                self.__alphabet.append(c)
        if (source, word) in self.__transitions:
            aux = self.__transitions[(source, word)]
        else:
            aux = []
        if not destiny in aux:
            self.__transitions[(source, word)] = aux + [destiny]

    def ge_initials(self):
        return self.__initials

    def get_finals(self):
        return self.__finals

    def get_states(self):
        return self.__states.keys()

    def get_alphabet(self):
        return self.__alphabet

    def get_transitions_from(self, state):
        resp = list()
        for (e, s) in self.__transitions:
            if e == state:
                resp.append((s, self.__transitions[(e, s)]))
        return resp

    def error(self, msg):
        print('Error: %s' % msg)
        quit()

    def move_afd(self, state, word):
        if not self.is_afd():
            self.error('move_afd')
        e = state
        for a in word:
            if not (e, a) in self.__transitions:
                return None
            transitions = self.__transitions[(e, a)]
            e = transitions[0]
        return e

    def accept(self, word):
        if not self.is_afd():
            self.error('accept')
        e = self.move_afd(self.__initials[0], word)
        if e is None:
            return False
        else:
            return e in self.__finals

    def is_afd(self):
        if len(self.__initials) > 1:
            return False
        for e in self.get_states():
            for (s, destiny) in self.get_transitions_from(e):
                if len(s) != 1 or len(destiny) != 1:
                    return False
        return True

    def has_lambda(self):
        for (e, s) in self.__transitions:
            if s == '':
                return True
        return False

    def is_afd_complete(self):
        if not self.is_afd():
            return False
        for e in self.get_states():
            for s in self.get_alphabet():
                if not (e, s) in self.__transitions:
                    return False
        return True

    def save_text_file(self, filename=''):
        pass

    def load_text_file(self, filename=''):
        try:
            f = open(filename, 'r')
            readed_lines = 0
            num_states = 0
            named = False
            for line in f:
                splitted_line = line.replace("\n", "").split(" ")
                if not named:
                    if readed_lines == 0:
                        if len(splitted_line) > 1:
                            named = True
                            for state in splitted_line:
                                final = '*' in state
                                initial = '>' in state
                                self.add_state(state.replace(">", "").replace("*", ""), initial=initial, final=final)
                        else:
                            num_states = int(line)
                        pass
                        # self.__num_states = int(line)
                    elif readed_lines == 1:
                        self.__alphabet = splitted_line
                    elif readed_lines == 2:
                        self.__initials = splitted_line
                    elif readed_lines == 3:
                        self.__finals = splitted_line
                        for i in range(0, num_states):
                            self.add_state(str(i), initial=i in self.__initials, final=i in self.__finals)
                    else:
                        self.add_transition(splitted_line[0], splitted_line[1], splitted_line[2])
                else:
                    if readed_lines >= 1:
                        self.add_transition(splitted_line[0], splitted_line[1], splitted_line[2])
                readed_lines += 1
            f.close()
            print("Automato Carregado\n "+str(self))
        except:
            self.error("load_text_file: arquivo mal formatado")

    def __str__(self):
        msg = '(E, A, ft, I, F) onde:\n' + \
              '  E  = {0}\n' + \
              '  A  = {1}\n' + \
              '  I  = {3}\n' + \
              '  F  = {4}\n' + \
              '  ft = {2}'
        ft = '{\n'
        for (e, a) in self.__transitions:
            t = self.__transitions[(e, a)]
            ft = '{0}    ({1}, {2}): {3},\n'.format(ft, e, a, t)
        ft = ft + '  }'
        return msg.format(self.__states,
                          self.__alphabet, ft,
                          self.__initials, self.__finals)
