import random
from collections import defaultdict

class CorrelationGame:
    def __init__(self):
        self.__states = {"0" : 0.5, "1" : 0.5}

    def add_a_new_bit(self, state_value = -1):
        new_state = {}

        if state_value == -1:
            state_value = random.choice([0, 1])
        
        for state, probability in self.__states.items():
            new_bit_0 = state + "0"
            new_bit_1 = state + "1"

            if state_value == 0:
                new_state[new_bit_0] = probability
            elif state_value == 1:
                new_state[new_bit_1] = probability
            else:
                new_state[new_bit_0] = probability * 0.5
                new_state[new_bit_1] = probability * 0.5

        self.__states = new_state

    def print_state(self):
        for state, probability in sorted(self.__states.items()):
            print(f"{probability:.2f} <{state}>")

    def print_state_vector(self):
        print(sorted(self.__states.items()))

    def not_bit(self, index_of_bit):
        new_state = {}

        for state, probability in self.__states.items():
            flipped_state = list(state)
            flipped_state[index_of_bit] = "0" if flipped_state[index_of_bit] == "1" else "1"

            # Convert back to string
            flipped_state = "".join(flipped_state)
            new_state[flipped_state] = new_state.get(flipped_state, 0) + probability

        self.__states = new_state

    def cnot(self, control_bit, target_bit):
        new_state = {}

        for state, probability in self.__states.items():
            flipped_state = list(state)
            if flipped_state[control_bit] == "1":
                flipped_state[target_bit] = "0" if flipped_state[target_bit] == "1" else "1"

            # Convert back to string
            flipped_state = "".join(flipped_state)
            new_state[flipped_state] = new_state.get(flipped_state, 0) + probability

        self.__states = new_state

    def random_cnot(self):
        if len(self.__states) == 1:
            return
        
        state_length = len(next(iter(self.__states)))
        control_bit = random.randint(0, state_length - 1)
        target_bit = random.randint(0, state_length - 1)

        self.cnot(control_bit, target_bit)

    def is_correlated(self, index_of_bit):
        values = set(state[index_of_bit] for state in self.__states)
        return len(values) > 1
    
    def uncorrelated_bits(self):
        uncorrelated_bits = []

        if not self.__states:
            return uncorrelated_bits
        
        # Get the length from any state string in the dictionary
        state_length = len(next(iter(self.__states)))
        
        for i in range(state_length):
            if not self.is_correlated(i):
                uncorrelated_bits.append(i)

        return uncorrelated_bits
    
    def correlated_bits(self):
        correlated_bits = []

        if not self.__states:
            return correlated_bits
        
        # Get the length from any state string in the dictionary
        state_length = len(next(iter(self.__states)))
        
        for i in range(state_length):
            if self.is_correlated(i):
                correlated_bits.append(i)

        return correlated_bits
    
    def create_correlations(self):
        uncorrelated_bits = self.uncorrelated_bits()
        correlated_bits = self.correlated_bits()

        if not correlated_bits: return 

        for i in uncorrelated_bits:
            random_bit = random.choice(correlated_bits)
            self.cnot(i, random_bit)

    def __remove_bit(self, bit_index):
        new_state = defaultdict(float)

        for state, probability in self.__states.items():
            new_state[state[:bit_index] + state[bit_index + 1:]] += probability

        self.__states = new_state

    def remove_an_uncorrelated_bit(self):
        if len(self.__states) == 1: return

        uncorrelated_bits = self.uncorrelated_bits()
        if not uncorrelated_bits: return

        random_bit = random.choice(uncorrelated_bits)
        return self.__remove_bit(random_bit)

    def remove_uncorrelated_bits(self):
        if len(self.__states) == 1: return

        uncorrelated_bits = self.uncorrelated_bits()
        if not uncorrelated_bits: return

        for index in sorted(uncorrelated_bits):
            self.__remove_bit(index)
            if len(self.__states) == 1: return

    def print_empty_line(self):
        print()


def main():
    game = CorrelationGame()
    game.add_a_new_bit()
    game.print_state()
    game.print_empty_line()
    game.add_a_new_bit()
    game.print_state()

    game.print_empty_line()

    game.create_correlations()
    game.print_state()

    game.print_empty_line()

    game.remove_an_uncorrelated_bit()
    game.print_state()

    game.print_empty_line()

    game.remove_uncorrelated_bits()
    game.print_state()

    game.print_empty_line()

    game.random_cnot()
    game.print_state()


if __name__ == "__main__":
    main()
