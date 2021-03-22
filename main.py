from Automaton import Automaton


def read_input_automaton():
    try:
        print("Obs.: * é utilizado em estados finais e > em estados iniciais\n")
        states = input("Digite os estados do automato (Ex.: >a b *c):")
        new = Automaton()
        splitted_line = states.replace("\n", "").split(" ")
        if len(splitted_line) > 1:
            for state in splitted_line:
                final = '*' in state
                initial = '>' in state
                new.add_state(state.replace(">", "").replace("*", ""), initial=initial, final=final)
            t ="aa"
            while not t=="":
                t = input("Digite a transição ou vazio para parar (Ex.: origem caracter destino):")
                if t == "":
                    break
                else:
                    splitted_line = t.replace("\n", "").split(" ")
                    new.add_transition(splitted_line[0], splitted_line[1], splitted_line[2])
        return new
    except:
        print("Digite os valores como indicado")
        return None


def load_and_return(text=None):
    loaded = Automaton()
    if text is None:
        filename = input("Digite o caminho do arquivo(Ex:'./afd.txt'):")
        loaded.load_text_file(filename=filename)
    else:
        filename = input("Digite o caminho do arquivo(Ex:'./afd.txt'):")
        loaded.load_text_file(filename=filename)
    return loaded



if __name__ == '__main__':
    option = -1
    automaton = None
    while True:
        try:
            print("---------------------------------------------------------------\n"
                  "-----------------------------Opções----------------------------\n"
                  "---------------------------------------------------------------\n"
                  "0 - Sair\n"
                  "1 - Carregar Automato de um Arquivo\n"
                  "2 - Salvar Automato em um Arquivo\n"
                  "3 - Minimizar Automato\n"
                  "4 - Mostrar Estados Equivalentes\n"
                  "5 - Testar Equivalencia Entre Automatos\n"
                  "6 - Multiplicar Automatos\n"
                  "7 - Operações entre Automatos\n"
                  "8 - Converter AFN para AFD\n"
                  "9 - Converter AFN-γ para AFN\n"
                  "10 - Converter AFN-γ para AFD\n"
                  )
            option = int(input('Selecione a operação que deseja realizar:'))
        except:
            option = -1
        if option == 0:
            quit()
        elif option == 1:
            automaton = load_and_return()
        elif option == 2:
            automaton = read_input_automaton()
            if not automaton is None:
                automaton.save_text_file(input("Digite o caminho para salvar o arquivo(Ex:'./afd.txt'):"))
        elif option == 3:
            if automaton is None:
                automaton = load_and_return()
            if not automaton is None:
                result = automaton.minimize()
                print(result)
                result.save_text_file(input("Digite o caminho para salvar a minimização(Ex:'./afd.txt'):"))
        elif option == 4:
            if automaton is None:
                automaton = load_and_return()
            if not automaton is None:
                print("Estados Equivalentes: "+str(automaton.get_equivalents()))
        elif option == 5:
            text = ""
            automaton1 = load_and_return()
            automaton2 = load_and_return("Digite o caminho do arquivo(Ex:'./afd2.txt'):")
            if not automaton1 is None and not automaton2 is None:
                equivalent = automaton1.is_equivalent_afd(automaton2)
                text = "Resultado da equivalência: "
                if equivalent:
                    text += "EQUIVALENTE"
                else:
                    text += "NÂO EQUIVALENTE"
                print(text)
        elif option == 6:
            automaton1 = load_and_return()
            automaton2 = load_and_return("Digite o caminho do arquivo(Ex:'./afd2.txt'):")
            if not automaton1 is None and not automaton2 is None:
                multiplication = automaton1.multiplication(automaton2)
                print("RESULTADO DA MULTIPLICAÇÃO")
                print(multiplication)
                multiplication.save_text_file(input("Digite o caminho para salvar a multiplicacao(Ex:'./afd.txt'):"))
        elif option == 7:
            automaton1 = load_and_return()
            automaton2 = load_and_return("Digite o caminho do arquivo(Ex:'./afd2.txt'):")
            if not automaton1 is None and not automaton2 is None:
                operation = input("Digite o tipo de operação(U=União, I=Interseção,D=Diferença,C=Complemento):")
                while not(operation.lower() == "u" or operation.lower() == "i" or operation.lower() == "d"
                          or operation.lower() == "c"):
                    operation = input("Digite o tipo de operação(U=União, I=Interseção,D=Diferença,C=Complemento):")
                operation = automaton1.operation(automaton2, operation)
                print("RESULTADO DA OPERAÇÃO")
                print(operation)
                operation.save_text_file(input("Digite o caminho para salvar a operação realizada(Ex:'./afd.txt'):"))
        elif option == 8:
            automaton1 = load_and_return()
            if not automaton1 is None:
                result = automaton1.afn_afd()
                print("AFD -> AFN")
                print(result)
                result.save_text_file("afn_to_afd.txt")
        elif option == 9:
            # automaton1 = load_and_return()
            automaton1 = Automaton()
            automaton1.load_text_file("./afn_vazio.txt")
            if not automaton1 is None:
                result = automaton1.afn_vazio_afn()
                print("AFN-γ -> AFN")
                print(result)
                result.save_text_file(input("Digite o caminho para salvar a conversão realizada(Ex:'./afny-afd.txt'):"))
        elif option == 10:
            automaton1 = load_and_return()
            if not afn_vazio is None:
                afn = afn_vazio.afn_vazio_afn()
                afd = afn.afn_afd()
                print("AFN-γ -> AFD")
                print(afd)
                afd.save_text_file(input("Digite o caminho para salvar a conversão realizada(Ex:'./afny-afd.txt'):"))
        else:
            print("Opção Inválida!")
        input("Aperte uma Tecla para Continuar!")
