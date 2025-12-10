from src.helpers.turing_machine import TuringMachineSimulator, BLANK, WILDCARD, DIR_L, DIR_R

# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        initial_config = ["", self.start_state, input_string if input_string else BLANK, None, None]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False
        accept_config = None
        total_transitions = 0
        max_reject_depth = 0

        while depth < max_depth and not accepted:
            #current_level = tree[-1]
            current_level = tree[depth]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            for config_index, config in enumerate(current_level):
                left = config[0]
                state = config[1]
                right = config[2]

                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if state == self.accept_state:
                    accepted = True
                    accept_config = config
                    accept_depth = depth
                    break
                # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if state == self.reject_state: 
                    max_reject_depth = max(max_reject_depth, depth)
                    continue
                if right:
                    current_char = right[0]
                else:
                    current_char = BLANK
            
                # 4. If not Accept/Reject, find valid transitions in self.transitions.
                read_symbols = (current_char,) #in the case of a single tape
                transitions = self.get_transitions(state, read_symbols)
                # 5. If no explicit transition exists, treat as implicit Reject.
                if not transitions:
                    max_reject_depth = max(max_reject_depth, depth)
                    continue
                #there are still valid transitions
                all_rejected = False
                # 6. Generate children configurations and append to next_level[cite: 148].
                for transition_index, transition in enumerate(transitions):
                    total_transitions += 1

                    #apply transition
                    new_left = left
                    new_right = right
                    new_state = transition['next']
                    write_char = transition['write'][0]
                    direction = transition['move'][0]

                    #writing to tape
                    if new_right:
                        new_right = write_char + new_right[1:]

                    else:
                        new_right = write_char

                    #move head
                    if direction == DIR_R:
                        if new_right:
                            new_left = new_left + new_right[0]
                            new_right = new_right[1:]  
                        else:
                            new_left = new_left + BLANK
                            new_right = ""
                    elif direction == DIR_L:
                        if new_left:
                            new_right = new_left[-1] + new_right
                            new_left = new_left[:-1]
                        else:
                            new_right = BLANK + new_right
                            new_left = ""

                    #generate children config
                    new_config = [
                        new_left, 
                        new_state,
                        new_right if new_right else BLANK,
                        (depth, config_index),
                        transition_index
                    ]
                    #append to next_level
                    next_level.append(new_config)
            if accepted:
                break

            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f"Tree depth: {depth}")
                print(f"Total transitions: {total_transitions}")
                print(f"String rejected in {max_reject_depth} steps")
                self.print_tree(tree)
                return
                
            tree.append(next_level)
            depth += 1

        if accepted:
            print(f"Tree depth: {depth}")
            print(f"Total transitions: {total_transitions}")
            print(f"String accepted in {accept_depth} steps")
            print("\nAccepting path:")
            self.print_trace_path(tree, accept_config)
            print("\nFull computation tree:")
            self.print_tree(tree)
        elif depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]
            print(f"Total transitions: {total_transitions}")
            self.print_tree(tree)
        

    def print_trace_path(self, tree, final_config):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        path = []
        curr = final_config

        #have to backtrack to root
        while curr is not None:
            path.append(curr)
            if curr[3] is None:     #parent is None
                break
            depth, index = curr[3]  #parent is depth, index
            curr = tree[depth][index]

        #printing path from start state to accpet state
        path.reverse()
        for config in path:
            self.print_config(config)
        
        #fucntion to print config in correct format
        #format--> [left, state, right, parent, transition #]
    def print_config(self, config):
        left = config[0]
        state = config[1]
        right = config[2] if config[2] else BLANK
        head = right[0] if right else BLANK
        rest = right[1:] if len(right) > 1 else ""
            
        print(f"{left} {state} {head}{rest}")

        #prints entire tree by each level
    def print_tree(self, tree):
        for level_index, level in enumerate(tree):
            print(f"Level {level_index}:")
            for config_index, config in enumerate(level):
                print(f"  [{config_index}] ", end="")
                self.print_config(config)
