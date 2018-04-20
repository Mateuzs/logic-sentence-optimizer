from itertools import groupby


def optimize(variables, minterms):
    # let's create groups of minterms with '1', there's always n+1 groups
    group = [[] for _ in range(len(variables) + 1)]

    for i in range(len(minterms)):
        # convert to binary - it's simple : this is the number of the minterm
        minterms[i] = bin(minterms[i])[2:]
        if len(minterms[i]) < len(variables):
            for j in range(len(variables) - len(minterms[i])):
                minterms[i] = '0' + minterms[i]
        elif len(minterms[i]) > len(variables):
            print('\nError : Wrong number of input data!\n')
            return
        # we need to group minterms by the number of '1' in it's body
        index = minterms[i].count('1')
        group[index].append(minterms[i])

    print("\nGenerated groups of minterms:\n")
    for i in group:
        print(i)

    # next step: let's find prime implicants! we need to look for any combination

    prime_implicants = []

    # combine the pairs in series until nothing new can be matched
    while not is_empty(group):
        new_group, unchecked = combine(group, prime_implicants)
        group = remove_repeating_elements(new_group)

    print("\nOur prime implicants:\n")
    for implicant in prime_implicants:
        print(implicant)

    # next step: create a chart!
    chart = [[0 for _ in range(len(minterms))] for _ in range(len(prime_implicants))]

    for i in range(len(minterms)):
        for j in range(len(prime_implicants)):
            if include_minterm(minterms[i], prime_implicants[j]):
                chart[j][i] = 1

    print("\nOur chart: \n")
    for i in range(len(prime_implicants)):
        print(prime_implicants[i], " : ", chart[i])

    # last step: find optimal solution:

    optimal_primes = find_optimal(chart, prime_implicants)
    optimal_primes = remove_repeating_elements(optimal_primes)

    print_answer(variables, optimal_primes, prime_implicants)


# some auxiliary functions


def is_empty(group):
    if len(group) == 0:
        return True
    else:
        number = 0
        for subgroup in group:
            if subgroup:
                number += 1
        return number == 0


# we check the element matches in order to find implicants
def combine(group, prime_implicants):
    checked = []
    new_group = [[] for _ in range(len(group) - 1)]

    for i in range(len(group) - 1):
        for element1 in group[i]:
            for element2 in group[i + 1]:
                matched, position = compare_bits(element1, element2)

                if matched:
                    checked.append(element1)
                    checked.append(element2)

                    new_element = list(element1)
                    new_element[position] = '-'
                    new_element = "".join(new_element)
                    new_group[i].append(new_element)

    for subgroup in group:
        for element in subgroup:
            if element not in checked:
                prime_implicants.append(element)

    return new_group, prime_implicants


def remove_repeating_elements(group):
    new_group = []

    for sub_group in group:
        new_subgroup = []
        for element in sub_group:
            if element not in new_subgroup:
                new_subgroup.append(element)
        new_group.append(new_subgroup)

    return new_group


def compare_bits(element1, element2):
    differences = 0
    position = 0

    for i in range(len(element1)):
        if element1[i] != element2[i]:
            differences += 1
            position = i

    if differences == 1:
        return True, position
    else:
        return False, None


def include_minterm(minterm, prime_implicant):
    for i in range(len(prime_implicant)):
        if prime_implicant[i] != "-" and prime_implicant[i] != minterm[i]:
            return False
    return True


def find_optimal(chart, prime_implicants):
    final_implicants = []
    # wee need to find these implicants, which must be in the solution,
    # they have the one and only "1" in chart's column
    essential_implicants = find_essentials(chart)
    essential_implicants = remove_repeating_elements_in_list(essential_implicants)

    # check wheter essential implicants are the solution or not:
    for implicant in range(len(essential_implicants)):
        for column in range(len(chart[0])):
            if chart[essential_implicants[implicant]][column] == 1:
                for row in range(len(chart)):
                    chart[row][column] = 0

    # if the chart is full of '0' that means, essential_primes is the optimal solution:
    if chart_full_of_zeros:
        return [essential_implicants]
    else:

        # if we still have some '1' in the chart, there could be better solution
        # in order to find minimal solution, we could use Pterick's method
        optimal = petrick_method(chart)

        # count the cost of optimals in order to find shortest solution
        cost = []
        for solution in optimal:
            cost_value = 0
            for implicant in range(len(prime_implicants)):
                for element in solution:
                    if implicant == element:
                        cost_value = cost_value + real_cost(prime_implicants[implicant])
            cost.append(cost_value)

        # find the shortest solution
        for value in range(len(cost)):
            if cost[value] == min(cost):
                final_implicants.append(optimal[value])

        # add our essential implicants to the answer
        for implicant in final_implicants:
            for essential in essential_implicants:
                if essential not in implicant:
                    implicant.append(essential)

    return final_implicants


def find_essentials(chart):
    essentials = []

    for column in range(len(chart[0])):
        number_of_ones = 0
        position = 0
        for row in range(len(chart)):
            if chart[row][column] == 1:
                number_of_ones += 1
                position = row

        if number_of_ones == 1:
            essentials.append(position)

    return essentials


def remove_repeating_elements_in_list(implicants_list):
    new_list = []

    for element in implicants_list:
        if element not in new_list:
            new_list.append(element)

    return new_list


def chart_full_of_zeros(chart):
    for row in chart:
        for column in row:
            if column != 0:
                return False
    return True


def petrick_method(chart):
    # step 1: collect every set of implicants covering together at least one case
    petrick_sums = []
    for column in range(len(chart[0])):
        petrick_sum = []
        for row in range(len(chart)):
            if chart[row][column] == 1:
                petrick_sum.append([row])
        petrick_sums.append(petrick_sum)

    # step 2: perform multiplication
    for psum in range(len(petrick_sums) - 1):
        petrick_sums[psum + 1] = multiplication(petrick_sums[psum], petrick_sums[psum + 1])

    # step 3: sort these sum of products and pick the shortest one
    # there could be more than one shortest solution
    sums = sorted(petrick_sums[len(petrick_sums) - 1], key=len)

    answer = []
    shortest = len(sums[0])
    for solution in sums:
        if len(solution) == shortest:
            answer.append(solution)
        else:
            break

    return answer


def real_cost(implicant):
    cost = 0
    for bit in implicant:
        if bit != '-':
            cost += 1
    return cost


def multiplication(sum1, sum2):
    result = []

    if is_empty(sum1) and is_empty(sum2):
        return result
    elif is_empty(sum1):
        return sum2
    elif is_empty(sum2):
        return sum1
    else:
        for elem1 in sum1:
            for elem2 in sum2:
                if elem1 == elem2:
                    result.append(elem1)
                else:
                    result.append(list(set(elem1 + elem2)))

        result.sort()
        return list(result for result, _ in groupby(result))


def print_answer(variables, primes, implicants):
    print("\nSolution (one or more): \n")

    if len(primes) == 1:
        if len(primes[0]) == 1:
            flag = 1
            for bit in implicants[primes[0][0]]:
                if bit != '-':
                    flag = 0
            if flag == 1:
                print("1\n\n")
                return

    for group in primes:
        word = []
        for element in group:
            for i in range(len(implicants[element])):

                if implicants[element][i] == '-':
                    continue
                elif implicants[element][i] == '0':
                    word.append("(~")
                    word.append(variables[i])
                    word.append(")")
                elif implicants[element][i] == '1':
                    word.append(variables[i])

            if element != group[len(group) - 1]:
                word.append(" + ")

        print("".join(word))

    print("\n\n")
