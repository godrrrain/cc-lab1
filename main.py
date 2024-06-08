from builder import *
import sys


def main():
    regexp = input("Введите регулярное выражение: ")

    isDraw = 1

    nfda = create_nfa(regexp)

    dfa = convert_to_dfa(nfda)

    mdfa = minimize_dfa(dfa)

    if isDraw:
        nfda.draw(1)
        dfa.draw(2)
        mdfa.draw(3)

    while(True):
        input_str = input("Введите строку (для выхода введите q): ")
        if input_str == 'q':
            exit()
        else:
            print(mdfa.model_check(input_str))

main()