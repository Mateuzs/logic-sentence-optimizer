def truth_table(sentence):

    from itertools import product

    table = []

    sentence = sentence.strip()
    code = compile(sentence, '<string>', 'eval')
    names = code.co_names
    print("Prepare sentence: ", sentence)
    for values in product(range(2), repeat=len(names)):
        env = dict(zip(names, values))
        answer = eval(code, env)
        if answer:
            answer = 1
        if not answer:
            answer = 0

        print(' '.join(str(v) for v in values), ':', answer)
        table.append(answer)

    return names, table
