import copy


class Automaton(object):
    pass


class Automaton(object):
    __num_states = 0
    # elementos que compoem um automato
    __states = []
    __alphabet = []  # [ A, ... ]
    __transitions = {}  # { (E, A*) : E+, ... }
    __initials = []  # [ E, ... ]
    __finals = []

    def __init__(self, *args):
        if len(args) == 6:
            self.__num_states = args[0]
            # elementos que compoem um automato
            self.__states = args[1]
            self.__alphabet = args[2]  # [ A, ... ]
            self.__transitions = args[3]  # { (E, A*) : E+, ... }
            self.__initials = args[4] # [ E, ... ]
            self.__finals = args[5]  # [ E, ... ]
        else:
            self.__num_states = 0
            # elementos que compoem um automato
            self.__states = list()
            self.__alphabet = list()  # [ A, ... ]
            self.__transitions = dict()  # { (E, A*) : E+, ... }
            self.__initials = list() # [ E, ... ]
            self.__finals = list()  # [ E, ... ]

    def copy_af(self):
        copied = copy.deepcopy(self)
        return copied

    def mount_table(self):
        table = dict()
        for i in range(0, len(self.__states) - 1):
            table[self.__states[i]] = dict()
            for j in range(0, len(self.__states) - (i + 1)):
                reverse_states = list(reversed(self.__states))
                table[self.__states[i]][reverse_states[j]] = dict()
                table[self.__states[i]][reverse_states[j]]['tested'] = False
                table[self.__states[i]][reverse_states[j]]['equivalent'] = True
        return table

    def mark_trivially_not_equivalent(self, table):
        for row in table:
            for col in table[row]:
                # if row in self.__initials and col not in self.__initials:
                #     table[row][col] = False
                if row in self.__finals and col not in self.__finals:
                    table[row][col]['tested'] = False
                    table[row][col]['equivalent'] = False
                if col in self.__finals and row not in self.__finals:
                    table[row][col]['tested'] = False
                    table[row][col]['equivalent'] = False

    def print_eq_table(self, table):
        for row in table:
            print(row + " | " + str(table[row]))

    def tested_all(self, table):
        for row in table:
            for col in table[row]:
                if not table[row][col]['tested'] and not table[row][col]['equivalent']:
                    return False
        return True

    def test_not_trivially(self, table):
        while not self.tested_all(table):
            for row in table:
                for col in table[row]:
                    if not table[row][col]['tested'] and not table[row][col]['equivalent']:
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
                                    if row_res != col_res:
                                        results_tuples.append((row_res, col_res))
                            for result in results_tuples:
                                if result[0] in table:
                                    if result[1] in table[result[0]]:
                                        table[result[0]][result[1]]['equivalent'] = False
                                if result[1] in table:
                                    if result[0] in table[result[1]]:
                                        table[result[1]][result[0]]['equivalent'] = False
                            # if len(results_tuples) > 0:
                            table[row][col]['tested'] = True
                            # print(entry + " -> " + row + "X" + col + " = " + str(row_results) + "X" + str(
                            #     col_results) + " => " + str(results_tuples))
                            #     print("----------------------------------------------------------------------------")

    def get_equivalents(self, table=None):
        if table is None:
            table = self.mount_table()
            self.mark_trivially_not_equivalent(table)
            self.test_not_trivially(table)
        equivalents = []
        for row in table:
            for col in table[row]:
                if table[row][col]['equivalent']:
                    equivalents.append([row, col])
        for index, equivalent in enumerate(equivalents):
            for other_index, other_equivalent in enumerate(equivalents):
                if index != other_index:
                    for state in equivalent:
                        if state in other_equivalent:
                            new_equivalents = list(set(equivalent+other_equivalent))
                            if new_equivalents in equivalents:
                                equivalents.pop(other_index)
                                break
                            else:
                                equivalents[other_index] = list(set(equivalent+other_equivalent))
        return equivalents

    def minimize(self, rename=True) -> Automaton():
        table = self.mount_table()
        self.mark_trivially_not_equivalent(table)
        self.test_not_trivially(table)
        new_transitions = copy.deepcopy(self.__transitions)
        new_states = copy.deepcopy(self.__states)
        new_finals = copy.deepcopy(self.__finals)
        new_initials = copy.deepcopy(self.__initials)
        for equivalent in self.get_equivalents(table):
            if rename:
                new_name = ""
                for state in equivalent:
                    new_name += state
            else:
                new_name = equivalent[0]
            for t in new_transitions:
                for index, result in enumerate(new_transitions[t]):
                    if result in equivalent:
                        new_transitions[t][index] = new_name
            remove_from_dict = []
            for t in list(new_transitions):
                if t[0] in equivalent:
                    new_transitions[(new_name, t[1])] = new_transitions[t]
                    if rename:
                        remove_from_dict.append(t)
                    elif not equivalent.index(t[0]) == 0:
                        remove_from_dict.append(t)
            for t in remove_from_dict:
                new_transitions.pop(t)

            for index, state in enumerate(equivalent):
                if not index == 0:
                    if state in new_states:
                        new_states.remove(state)
                    if state in new_finals:
                        new_finals.remove(state)
                    if state in new_initials:
                        new_initials.remove(state)
            if equivalent[0] in new_initials:
                new_initials[new_initials.index(equivalent[0])] = new_name
            if equivalent[0] in new_finals:
                new_finals[new_finals.index(equivalent[0])] = new_name
            if equivalent[0] in new_states:
                new_states[new_states.index(equivalent[0])] = new_name
        new_num_states = len(new_states)
        return Automaton(new_num_states, new_states,
                         self.__alphabet, new_transitions,
                         new_initials, new_finals)

    def is_equivalent_afd(self, afd: Automaton()) -> bool:
        afd2_states = copy.deepcopy(afd.__states)
        afd2_initials = copy.deepcopy(afd.__initials)
        afd2_finals = copy.deepcopy(afd.__finals)
        afd2_transitions = copy.deepcopy(afd.__transitions)
        afd2 = self.rename(afd)
        test_transitions = dict()
        test_transitions.update(self.__transitions)
        test_transitions.update(afd2_transitions)
        afd_test = Automaton(len(afd2_states)+len(self.__states), self.__states+afd2_states,
                             list(set(self.__alphabet+afd.__alphabet)), test_transitions,
                             self.__initials+afd2_initials, self.__finals+afd2_finals)
        initials_eq_counter = 0
        for i in self.__initials:
            for i2 in afd2.__initials:
                for equivalents in afd_test.get_equivalents():
                    if i in equivalents and i2 in equivalents:
                        initials_eq_counter += 1
        if len(self.__initials) == 0 or len(afd2.__initials) == 0:
            return False
        if initials_eq_counter == len(self.__initials)*len(afd2.__initials):
            return True
        return False

    def complete(self) -> Automaton or None:
        error_name = '|Error|'
        for state in self.__states:
            for letter in self.__alphabet:
                if (state, letter) not in self.__transitions:
                    if error_name not in self.__states:
                        self.add_state(error_name)
                    self.__transitions[(state, letter)] = [error_name]

    def rename(self, afd: Automaton()) -> Automaton():
        afd2_states = copy.deepcopy(afd.__states)
        afd2_initials = copy.deepcopy(afd.__initials)
        afd2_finals = copy.deepcopy(afd.__finals)
        afd2_transitions = copy.deepcopy(afd.__transitions)
        for state in afd2_states:
            if state in self.__states:
                new_name = state+"|2"
                for t in afd2_transitions:
                    for index, result in enumerate(afd2_transitions[t]):
                        if state == result:
                            afd2_transitions[t][index] = new_name
                remove_from_dict = []
                for t in list(afd2_transitions):
                    if t[0] == state:
                        afd2_transitions[(new_name, t[1])] = afd2_transitions[t]
                        remove_from_dict.append(t)
                for t in remove_from_dict:
                    afd2_transitions.pop(t)
                afd2_states[afd2_states.index(state)] = new_name
                if state in afd2_finals:
                    afd2_finals[afd2_finals.index(state)] = new_name
                if state in afd2_initials:
                    afd2_initials[afd2_initials.index(state)] = new_name
        afd2 = Automaton(len(afd2_states), afd2_states,
                         afd.__alphabet, afd2_transitions,
                         afd2_initials, afd2_finals)
        return afd2

    def multiplication(self, afd: Automaton()) -> Automaton() or None:
        self_copy = copy.deepcopy(self)
        for letter_self in self_copy.__alphabet:
            if letter_self not in afd.__alphabet:
                afd.__alphabet.append(letter_self)
        for letter in afd.__alphabet:
            if letter not in self_copy.__alphabet:
                self_copy.__alphabet.append(letter)
        afd2 = self.rename(afd)
        afd2.complete()
        afd.__states = afd2.__states
        afd.__initials = afd2.__initials
        afd.__finals = afd2.__finals
        afd.__transitions = afd2.__transitions
        self_copy.complete()
        afd_multiplication = Automaton()
        for state_af1 in self_copy.__states:
            for state_af2 in afd2.__states:
                afd_multiplication.add_state(state_af1+state_af2,
                                             initial=(state_af2 in afd2.__initials and state_af1 in self.__initials)
                                             )
        error_name = '|Error|'
        for state_af1 in self_copy.__states:
            for state_af2 in afd2.__states:
                for letter in self_copy.__alphabet:
                    if (state_af1, letter) in self_copy.__transitions:
                        for result_af1 in self_copy.__transitions[(state_af1, letter)]:
                            if (state_af2, letter) in afd2.__transitions:
                                for result_af2 in afd2.__transitions[(state_af2, letter)]:
                                    if result_af1+result_af2 in afd_multiplication.__states:
                                        afd_multiplication.add_transition(state_af1+state_af2, letter, result_af1+result_af2)
                                    elif result_af2+result_af1 in afd_multiplication.__states:
                                        afd_multiplication.add_transition(state_af1+state_af2, letter, result_af2+result_af1)
        afd_multiplication.__alphabet = self_copy.__alphabet
        afd_multiplication.complete()
        return afd_multiplication

    def operation(self, afd: Automaton(), operation: str) -> Automaton or None:
        multiplication_result = self.multiplication(afd)
        if operation.lower() == "u":
            for state_af1 in self.__states:
                for state_af2 in afd.__states:
                    if state_af1 in self.__finals or state_af2 in afd.__finals:
                        multiplication_result.__finals.append(state_af1+state_af2)
        elif operation.lower() == "i":
            for state_af1 in self.__states:
                for state_af2 in afd.__states:
                    if state_af1 in self.__finals and state_af2 in afd.__finals:
                        multiplication_result.__finals.append(state_af1+state_af2)
        elif operation.lower() == "d":
            for state_af1 in self.__states:
                for state_af2 in afd.__states:
                    if state_af1 in self.__finals and state_af2 not in afd.__finals:
                        multiplication_result.__finals.append(state_af1+state_af2)
                    if state_af1 not in self.__finals and state_af2 in afd.__finals:
                        multiplication_result.__finals.append(state_af1+state_af2)
        elif operation.lower() == "c":
            for state_af1 in self.__states:
                for state_af2 in afd.__states:
                    if state_af1 not in self.__finals and state_af2 not in afd.__finals:
                        multiplication_result.__finals.append(state_af1+state_af2)
                    if state_af1 not in self.__finals and state_af2 not in afd.__finals:
                        multiplication_result.__finals.append(state_af1+state_af2)
        return multiplication_result

    def afn_afd(self) -> Automaton() or None:
        afn = self.copy_af()
        if  afn.has_lambda():
            print("Converta o AFN-γ para AFN primeiro")
            return None
        if not afn.is_afd():
            afd = Automaton()
            afd.__alphabet = afn.__alphabet
            new_initial = "|".join(afn.__initials)
            transitions = {}
            afd.add_state(new_initial, initial=True)
            for letter in afn.__alphabet:
                for state in afn.__initials:
                    if (state, letter) in afn.__transitions:
                        for destiny in afn.__transitions[(state, letter)]:
                            if (new_initial, letter) in transitions:
                                if not destiny in transitions[(new_initial, letter)]:
                                    has_destiny_str = False
                                    for d in transitions[(new_initial, letter)]:
                                        if "|"+destiny in d or destiny+"|" in d:
                                            has_destiny_str = True
                                    if not has_destiny_str:
                                        transitions[(new_initial, letter)].append(destiny)
                            else:
                                transitions[(new_initial, letter)] = [destiny]
                        if len(transitions[(new_initial, letter)]) > 1:
                            sorted_transition = transitions[(new_initial, letter)]
                            sorted_transition.sort()
                            transitions[(new_initial, letter)] = ["|".join(sorted_transition)]
            state_missing = True
            while state_missing:
                state_missing = False
                for t in list(transitions):
                    for destiny in transitions[t]:
                        if destiny not in afd.__states:
                            original_states = destiny.split("|")
                            is_final = False
                            for original in original_states:
                                if original in afn.__finals:
                                    is_final = True
                            afd.add_state(destiny, final=is_final)
                            for letter in afn.__alphabet:
                                for state in original_states:
                                    if (state, letter) in afn.__transitions:
                                        for destiny_new in afn.__transitions[(state, letter)]:
                                            if (destiny, letter) in transitions:
                                                if not destiny_new in transitions[(destiny, letter)]:
                                                    has_destiny_str = False
                                                    for d in transitions[(destiny, letter)]:
                                                        if "|"+destiny_new in d or destiny_new+"|" in d:
                                                            has_destiny_str = True
                                                    transitions[(destiny, letter)].append(destiny_new)
                                            else:
                                                transitions[(destiny, letter)] = [destiny_new]
                                        if len(transitions[(destiny, letter)]) > 1:
                                            sorted_transition = transitions[(destiny, letter)]
                                            sorted_transition.sort()
                                            new_state = "|".join(sorted_transition)
                                            if new_state not in afd.__states:
                                                state_missing = True
                                            transitions[(destiny, letter)] = [new_state]
            afd.__transitions = transitions
            afd.complete()
            return afd
        else:
            print("O automato ja é um afd")
            return None

    def afn_vazio_afn(self) -> Automaton() or None:
        afn_vazio = self.copy_af()
        if afn_vazio.has_lambda():
            eclose = {}
            for state in afn_vazio.__states:
                if (state, 'γ') in afn_vazio.__transitions:
                    eclose[state] = [state]+afn_vazio.__transitions[(state, 'γ')]
                else:
                    eclose[state] = [state]
            afn = self.copy_af()
            afn.__alphabet.remove('γ')
            for t in list(afn.__transitions):
                if t[1] == 'γ':
                    afn.__transitions.pop(t)
                else:
                    eclose_destinations = []
                    for destiny in afn.__transitions[t]:
                        eclose_destinations = eclose_destinations + eclose[destiny]
                    afn.__transitions[t] = eclose_destinations
            return afn
        else:
            print("O automato não tem o transições γ")

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
        for e in self.__states:
            for (s, destiny) in self.get_transitions_from(e):
                if len(s) != 1 or len(destiny) != 1:
                    return False
        return True

    def has_lambda(self):
        for (e, s) in self.__transitions:
            if s == 'γ':
                return True
        return False

    def is_afd_complete(self):
        if not self.is_afd():
            return False
        for e in self.__states:
            for s in self.get_alphabet():
                if not (e, s) in self.__transitions:
                    return False
        return True

    def save_text_file(self, filename=''):
        try:
            f = open(filename, 'w+')
            file_text = ""
            for state in self.__states:
                if not file_text=="":
                    file_text += " "
                if state in self.__initials:
                    file_text += ">"
                file_text += state
                if state in self.__finals:
                    file_text += "*"
            file_text += "\n"
            for transition in self.__transitions:
                for result in self.__transitions[transition]:
                    file_text += transition[0]+" "+transition[1]+" "+result+"\n"
            f.write(file_text)
            f.close()
        except:
            self.error("erro ao criar arquivo python")

    def load_text_file(self, filename: str = ''):
        try:
            f = open(filename, 'r')
            readed_lines = 0
            num_states = 0
            named = False
            for line in f:
                splitted_line = line.replace("\n", "").split(" ")
                if not named:
                    while '' in splitted_line:
                        splitted_line.remove('')
                    if readed_lines == 0:
                        if len(splitted_line) != 0:
                            named = True
                            for state in splitted_line:
                                final = '*' in state
                                initial = '>' in state
                                self.add_state(state.replace(">", "").replace("*", ""), initial=initial, final=final)
                        # self.__num_states = int(line)
                    elif readed_lines == 1:
                        num_states = int(line)
                    elif readed_lines == 2:
                        self.__alphabet = splitted_line
                    elif readed_lines == 3:
                        self.__initials = splitted_line
                    elif readed_lines == 4:
                        self.__finals = splitted_line
                        for i in range(1, num_states+1):
                            self.add_state(str(i), initial=i in self.__initials, final=i in self.__finals)
                    else:
                        self.add_transition(splitted_line[0], splitted_line[1], splitted_line[2])
                else:
                    if readed_lines >= 1:
                        self.add_transition(splitted_line[0], splitted_line[1], splitted_line[2])
                readed_lines += 1
            f.close()
            print("Automato Carregado\n " + str(self))
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
