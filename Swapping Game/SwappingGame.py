import math
import random

class SwappingGame:
    def __init__(self):
        self.qubits = [-3, -2, -1, 0, +1, +2, +3]
        self.n_qubits = len(self.qubits)
        self.index_map = {q : i for i, q in enumerate(self.qubits)}

        self.neighbors = {
            -3 : [-1],
            -2 : [-1],
            -1 : [-3, -2, 0],
            0 : [-1, +1],
            +1 : [0, +2, +3],
            +2 : [+1],
            +3 : [+1]
        }

        self.list_of_states = [
            [1, 0] if i % 2 == 0 else [0, 1]  # alternating |0⟩ and |1⟩
            for i in range(7)
        ]



        self.state = self.tensor_product_all(self.list_of_states)

    def tensor_product(self, state1, state2):
        return [a * b for a in state1 for b in state2]


    def tensor_product_all(self, states):
        result = states[0]
        for state in states[1:]:
            result = self.tensor_product(result, state)
        return result

    def matrix_vector_multiply(self, matrix, vector):
        result = []
        for row in matrix:
            value = sum(row[i] * vector[i] for i in range(len(vector)))
            result.append(value)
        return result

    def CNOT(self, control_idx, target_idx):
        assert 0 <= control_idx < self.n_qubits
        assert 0 <= target_idx < self.n_qubits

        dim = 2 ** self.n_qubits
        new_state = [0.0 for _ in range(dim)]

        for i in range(dim):
            bitstring = f"{i:07b}"  # MSB on the left

            # Convert to LSB-order indexing
            logical_control = self.n_qubits - 1 - control_idx
            logical_target = self.n_qubits - 1 - target_idx

            control_bit = bitstring[logical_control]
            target_bit = bitstring[logical_target]

            new_bitstring = list(bitstring)
            if control_bit == '1':
                new_bitstring[logical_target] = '0' if target_bit == '1' else '1'

            j = int(''.join(new_bitstring), 2)
            new_state[j] += self.state[i]

        self.state = new_state

    def apply_CNOTs(self, control, target):
        c, t = self.index_map[control], self.index_map[target]
        self.CNOT(c, t)

    def swap_neighbors(self, qubit1, qubit2):
        if qubit2 not in self.neighbors[qubit1]:
            raise ValueError(f"Qubit {qubit2} is not a neighbor of {qubit1}")
        
        c1 = self.index_map[qubit1]
        c2 = self.index_map[qubit2]

        self.CNOT(c1, c2)
        self.CNOT(c2, c1)
        self.CNOT(c1, c2)

        self.list_of_states[c1], self.list_of_states[c2] = self.list_of_states[c2], self.list_of_states[c1]
        # Recompute full state from list_of_states (don't use CNOTs!)
        self.state = self.tensor_product_all(self.list_of_states)
        
        result = self.verify_state()
        if not result:
            print(f"Error: Swapping states of qubits {qubit1} and {qubit2} did not maintain tensor product state.")
        else:
            print(f"Swapped states of qubits {qubit1} and {qubit2} successfully.")

    def swap(self, qubit1, qubit2):
        if qubit1 == qubit2:
            return
        
        path = self.find_path(qubit1, qubit2)

        for i in range(len(path) - 1):
            self.swap_neighbors(path[i], path[i + 1])

        for i in range(len(path) - 1, 0, -1):
            self.swap_neighbors(path[i], path[i - 1])

    def find_path(self, start, end):  
        from collections import deque
        
        visited = set()
        queue = deque([start])
        parent = {}

        while queue:
            current = queue.popleft()
            if current == end:
                break
            
            for neighbor in self.neighbors[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent[neighbor] = current

        path = []
        current = end
        while current != start:
            path.append(current)
            current = parent[current]
        path.append(start)
        path.reverse()

        return path

    def verify_state(self):
        expected_state = self.tensor_product_all(self.list_of_states)
        for i in range(len(self.state)):
            if not math.isclose(self.state[i], expected_state[i], abs_tol=1e-9):
                return False
        return True

if __name__ == "__main__":
    game = SwappingGame()
    game.swap(-3, 0)
