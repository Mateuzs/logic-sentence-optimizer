
def is_correct_logic_sentence(sentence):

    variables = [chr(i) for i in range(97, 123)] + ["1"] + ["0"]
    parentheses = 0
    operators = ['|', '&', '>', '^', '~']
    state = True
    neg_flag = False
    var_flag = False

    for character in sentence:
        if character == ' ':
            var_flag = False
            continue
        elif var_flag:
            if character not in variables:
                return False
        else:
            if state:
                if character in variables:
                    state = False
                    var_flag = True
                elif character == '(':
                    parentheses = parentheses + 1
                elif character == '~' and neg_flag is False:
                    neg_flag = True
                else:
                    return False
            else:
                if character in operators:
                    state = True
                elif character == ')':
                    parentheses = parentheses - 1
                else:
                    return False

    return (parentheses == 0) and (not state)


def prepare_logic_sentence(sentence):

    # We need to change ~ symbol to negation
    sentence = sentence.replace("~", "not ")

    # We also need to change '>' symbol into another equal sentention not p or q#

    sentence_stack = []
    auxiliary_stack = []

    for character in sentence:

        if character == '>':
            auxiliary_stack.append(sentence_stack.pop())
            auxiliary_stack.append(sentence_stack.pop())

            if auxiliary_stack[len(auxiliary_stack)-1] == ")":
                parentheses = 1
                while parentheses != 0:
                    if sentence_stack[len(sentence_stack)-1] == ")":
                        parentheses += 1
                    elif sentence_stack[len(sentence_stack)-1] == "(":
                        parentheses -= 1

                    auxiliary_stack.append(sentence_stack.pop())

            sentence_stack.append("(not ( ")

            while auxiliary_stack:
                sentence_stack.append(auxiliary_stack.pop())

            sentence_stack.append(")) |")
            continue

        sentence_stack.append(character)

    return ''.join(sentence_stack)
