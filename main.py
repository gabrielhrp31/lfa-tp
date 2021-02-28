from Automaton import Automaton

if __name__ == '__main__':
    automaton = Automaton()
    automaton.load_text_file('./afd_named_aaa_or_bbb.txt')
    minimizado = Automaton()
    minimizado = automaton.minimize(minimizado)
