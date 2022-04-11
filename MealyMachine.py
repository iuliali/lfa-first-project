class MealyMachine:
    def __init__(self, filein_name, fileout_name):
        self.filein_name = filein_name
        self.fileout_name = fileout_name
        self.adjacency_list = {}
        self.alphabet_set = set()
        self.initial_state = 0
        self.no_final_states = 0
        self.final_states_list = []
        self.no_states = 0
        self.no_transitions = 0
        self.output_list = []
        self.path_list = []
        self.words_list = []
        self.read_machine(self.filein_name)
        self.complete_machine()


    def read_machine(self, file_in_name):
        ### read from file the input - no.states, no. transitions-- tranzitions
        file_in = open(file_in_name, "r")
        no_states, no_transitions = tuple(int(x) for x in file_in.readline().split())
        self.adjacency_list = {state: {} for state in range(no_states)}
        for i in range(no_transitions):
            line = file_in.readline().split()  # format: state - state2 - letter of alphabet- letter/no for output
            if int(line[1]) not in self.adjacency_list[int(line[0])]:
                self.adjacency_list[int(line[0])][int(line[1])] = [(line[2], line[3])]
            else:
                self.adjacency_list[int(line[0])][int(line[1])].append((line[2], line[3]))
            self.alphabet_set.add(line[2])

        # initial state, no of final states & final states
        self.initial_state = int(file_in.readline())
        line = file_in.readline().split()
        self.no_final_states = int(line[0])
        self.final_states_list = [int(final_state) for final_state in line[1:]]

        ### no of inputs to test -- inputs
        no_words = int(file_in.readline())
        self.words_list = [file_in.readline().strip() for _ in range(no_words)]
        file_in.close()


    def complete_machine(self):
        ## creating a new non-final state
        new_state = max(self.adjacency_list.keys()) + 1
        self.adjacency_list[new_state] = {new_state: []}
        self.adjacency_list[new_state][new_state] = [(letter, None) for letter in self.alphabet_set]

        ### try to make the graph complete
        for state in self.adjacency_list.keys():
            temp_transition_set = set()
            for state2 in self.adjacency_list[state].keys():
                temp_transition_set = temp_transition_set | set(
                    letter for letter in [transition[0] for transition in self.adjacency_list[state][state2]])
                # print(state, " ", state2, " ", temp_transition_set)
            transitions_to_do = self.alphabet_set - temp_transition_set
            # print(state)
            # print(transitions_to_do)
            if len(transitions_to_do) != 0:
                self.adjacency_list[state][new_state] = []
                for transition in transitions_to_do:
                    self.adjacency_list[state][new_state].append((transition, None))
        print(self.adjacency_list)

    def dfs(self, state, word_to_process, letter_position):
        if letter_position < len(word_to_process):
            for state2 in self.adjacency_list[state].keys():
                for tuple in self.adjacency_list[state][state2]:
                    if tuple[0] == word_to_process[letter_position]:
                        self.output_list.append(tuple[1])
                        self.path_list.append(state2)
                        return self.dfs(state2, word_to_process, letter_position + 1)
        else:
            return state

    def is_accepted(self, state):
        if state in self.final_states_list:
            return True
        else:
            return False

    def process_words(self):
        file_out = open(self.fileout_name, "a")
        # print(self.words_list)
        for word in self.words_list:
            self.path_list = [self.initial_state]
            self.output_list = []
            destination_state = self.dfs(self.initial_state, word, 0)
            if self.is_accepted(destination_state):
                print("DA")
                file_out.write("DA\n")
                print(*self.output_list, sep="")
                for letter in self.output_list:
                    file_out.write(letter)
                file_out.write("\n")
                print(f"Traseu:", end=" ")
                file_out.write(f"Traseu: ")
                print(*self.path_list, sep=" ")
                for node in self.path_list:
                    file_out.write(str(node) + " ")
                file_out.write("\n")

            else:
                print("NU")
                file_out.write("NU\n")
        file_out.close()
