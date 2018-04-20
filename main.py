from logic_sentence_checker import is_correct_logic_sentence, prepare_logic_sentence
from truth_table import truth_table
from quine_mcCluskey_algorithm import optimize


def main():
    while True:

        print("\nWelcome to my logic optimizer! please type Your logic sentence")
        print("\nexample: ( a & b ) > ( c | ( ~d ))")
        print("\nexample: ( kura & jajko ) & ( kura  ^ jajko ) > (~ jajko )")
        print("\nAllowed operators:\n\n and: &\n or: |\n implication: >\n xor: ^\n not: ~")
        print("\nBe careful with parentheses, it's really important!")
        sentence = input("\nType the logic sentence:  ")

        if is_correct_logic_sentence(sentence):

            minterms = []

            ready_sentence = (prepare_logic_sentence(sentence))
            (variables, answer) = truth_table(ready_sentence)

            for i in range(len(answer)):
                if answer[i]:
                    minterms.append(i)
            print("\nVariables: ", variables)
            print("Minterms: ", minterms)

            optimize(variables, minterms)

        else:
            print("your sentence is gramatically wrong!")

        if input("Press type 'y' to continue or anything to exit: ") == 'y':
            continue
        else:
            return

if __name__ == "__main__":
    main()
