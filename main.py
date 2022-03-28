###LFA-project-1
### Mealy Machine


def dfs(list, state, word_to_process, letter_position, output_list, path_list):
    if letter_position < len(word_to_process):
        for state2 in list[state].keys():
            for tuple in list[state][state2]:
                if tuple[0] == word_to_process[letter_position]:
                    output_list.append(tuple[1])
                    path_list.append(state2)
                    return dfs(list, state2, word_to_process, letter_position + 1, output_list, path_list)
    return state


def is_accepted(final_states_list, state):
    if state in final_states_list:
        return True
    return False


# def print_output(list, state, word_to_process, letter_position):
#     if letter_position < len(word_to_process):
#         for state2 in list[state].keys():
#             for tuple in list[state][state2]:
#                 if tuple[0] == word_to_process[letter_position]:
#                     print(tuple[1], end=" ")
#                     return print_output(list, state2, word_to_process, letter_position + 1)
#     return state



### read from file the input - no.states, no. transitions-- tranzitions
### no of inputs to test -- inputs
file_in = open("data.in", "r")
no_states, no_transitions = tuple(int(x) for x in file_in.readline().split())
adjacency_list = {state: {} for state in range(no_states)}
alphabet_set = set()
for i in range(no_transitions):
    line = file_in.readline().split() # format: states - state2 - number - letter
    if int(line[1]) not in adjacency_list[int(line[0])]:
        adjacency_list[int(line[0])][int(line[1])] = [(line[2], int(line[3]))]
    else:
        adjacency_list[int(line[0])][int(line[1])].append((line[2], int(line[3])))
    alphabet_set = alphabet_set | {line[2]}

print(adjacency_list)
initial_state = int(file_in.readline())
line = file_in.readline().split()
no_final_states = int(line[0])
list_final_states = [int(final_state) for final_state in line[1:]]

# print(initial_state)
# print(list_final_states)
# print(alphabet_set)
# print(max(adjacency_list.keys())) # nr celei mai mari stari

## apare o noua stare, care e nefinala
new_state = max(adjacency_list.keys()) + 1
adjacency_list[new_state] = {new_state: []}
adjacency_list[new_state][new_state] = [(letter, None) for letter in alphabet_set]
print(adjacency_list)
### try to make the graph complete
temp_transition_set = set()
for state in adjacency_list.keys():
    for state2 in adjacency_list[state].keys():
        temp_transition_set = temp_transition_set | set(letter for letter in [transition[0] for transition in adjacency_list[state][state2]])
        # print(state, " ", state2, " ", temp_transition_set)
    transitions_to_do = alphabet_set - temp_transition_set
    if len(transitions_to_do) != 0:
        adjacency_list[state][new_state] = []
        for transition in transitions_to_do:
            adjacency_list[state][new_state].append((transition, None))


print(adjacency_list)

no_words = int(file_in.readline())
file_out = open("data.out", "a")
for i in range(no_words):
    word = file_in.readline().strip()
    path = [initial_state]
    output = []
    if is_accepted(list_final_states, dfs(adjacency_list, initial_state, word, 0, output, path)):
        print("DA")
        print(*output, sep="")
        print(f"Traseu : ", end=" ")
        print(*path, sep=" ")

    else:
        print("NU")


file_in.close()
file_out.close()









