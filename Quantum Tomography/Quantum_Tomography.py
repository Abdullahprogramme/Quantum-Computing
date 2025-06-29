from random import randrange, choices
from math import cos, sin, pi

class UnknownQuantumSystem:
    def __init__(self, the_number_of_qubits = 2, the_number_of_copies = 1000):
        self.number_of_qubits = the_number_of_qubits
        self.available_copies = the_number_of_copies

        # Thetas in range [0, pi]
        self.thetas = [ (randrange(18000) / 18000) * pi for _ in range(self.number_of_qubits)]

        self.original_state = self.__make_state(self.thetas)
        self.copy_state = self.original_state.copy()

        self.active_copies = 0
        print(f"{self.available_copies} copies of a {self.number_of_qubits}-qubit system created")

    
    def __make_state(self, thetas):
        """Builds the full 2^n state vector from theta angles"""
        state1 = [1.0]
        for theta in thetas:
            state2 = [cos(theta), sin(theta)]

            # tensor product
            state1 = self.__tensor_product(state1, state2)

        return state1
        
    def __tensor_product(self, state1, state2):
        """Computes the tensor product of two states"""
        return [a * b for a in state1 for b in state2]
    
    def get_qubits(self, number_of_copies = None):
        if number_of_copies is None:
            print(f"Must specify the number of qubits to return")
        elif number_of_copies > self.available_copies:
            print(f"Cannot return {number_of_copies} qubits, only {self.available_copies} available")
        else:
            self.active_copies = number_of_copies
            self.available_copies -= number_of_copies
            self.copy_state = self.original_state.copy()
            print(f"Have {self.active_copies} qubits, {self.available_copies} copies remaining")

    def rotate_qubit(self, qubit_index, angle = None):
        if angle is None or (isinstance(angle, float) is False and isinstance(angle, int) is False):
            print()
            print("ERROR: the method 'rotate_qubits' takes a real-valued angle in radian as its parameter, i.e., rotate_qubits(1.2121)")
        
        if not (0 <= qubit_index < self.number_of_qubits):
            print()
            print("ERROR: Invalid qubit index")
            return
        
        print(f"Rotating qubit {qubit_index} by {angle:.4f} radians")

        # Build the full matrix as I ⊗ I ⊗ Ry ⊗ I ⊗ ...
        full_matrix = self._build_rotation_matrix(angle, qubit_index)
        self.copy_state = self._apply_matrix(full_matrix, self.copy_state)

    def _apply_matrix(self, matrix, vector):
        """Applies a 2^n x 2^n matrix to a vector"""
        size = len(vector)
        result = [0.0] * size
        for i in range(size):
            for j in range(size):
                result[i] += matrix[i][j] * vector[j]
        return result

    def _build_rotation_matrix(self, angle, target_qubit):
        """Constructs the 2^n x 2^n matrix for Ry rotation on a target qubit"""
        ry = [
            [cos(angle), -sin(angle)],
            [sin(angle),  cos(angle)]
        ]
        matrices = []
        for i in range(self.number_of_qubits):
            if i == target_qubit:
                matrices.append(ry)
            else:
                matrices.append([[1, 0], [0, 1]])  # Identity

        return self._kronecker_chain(matrices)

    def _kronecker_chain(self, matrices):
        """Computes the Kronecker product of a list of 2x2 matrices"""
        result = matrices[0]
        for m in matrices[1:]:
            result = self._kronecker_2x2(result, m)
        return result
    
    def _kronecker_2x2(self, A, B):
        """Kronecker product of two matrices A (2^k x 2^k), B (2 x 2)"""
        size_A = len(A)
        size_B = len(B)
        result = [[0.0 for _ in range(size_A * size_B)] for _ in range(size_A * size_B)]
        for i in range(size_A):
            for j in range(size_A):
                for k in range(size_B):
                    for l in range(size_B):
                        result[i*size_B + k][j*size_B + l] = A[i][j] * B[k][l]
        return result
    
    def measure_qubits(self):
        """Simulates measurement for the current state and counts results"""
        if self.active_copies == 0:
            print("No active systems. Use get_qubits() first.")
            return
        
        probabilities = [abs(amplitude)**2 for amplitude in self.copy_state]
        outcomes = list(range(2**self.number_of_qubits))
        measured_outcomes = choices(outcomes, weights=probabilities, k=self.active_copies)

        result = {outcome: 0 for outcome in measured_outcomes}
        for outcome in measured_outcomes:
            result[outcome] += 1

        print("Measurement results:", result)
        self.active_copies = 0
        return result
    
    def compare_guess(self, guesses):
        if not isinstance(guesses, list) or len(guesses) != self.number_of_qubits:
            print("ERROR: You must provide a list of", self.number_of_qubits, "angles in radian")
            return
        print("\nComparison of guessed angles:")

        for i, (guess, theta) in enumerate(zip(guesses, self.thetas)):
            difference = abs(guess - theta) * 180 / pi
            print(f"Qubit {i}: Guessed angle = {guess:.4f} rad, Actual angle = {theta:.4f} rad, Difference = {difference:.2f} degrees")
        print("\nComparison complete. No more copies available for measurement.")
        self.available_copies = 0

    def available_qubits(self):
        print("Available unused systems:", self.available_copies)

def main():
    sys = UnknownQuantumSystem(the_number_of_qubits=2)
    sys.get_qubits(100)
    sys.rotate_qubit(0, 0.5)  # Rotate qubit 0
    sys.rotate_qubit(1, 0.7)  # Rotate qubit 1
    results = sys.measure_qubits()  # Measure the qubits

    # Try to guess angles
    guesses = []
    for i in range(sys.number_of_qubits):
        angle = input(f"Guess the angle for qubit {i} in radians in the range [0, pi]: ")
        try:
            angle = float(angle)
            if 0 <= angle <= pi:
                guesses.append(angle)
            else:
                print(f"Invalid angle {angle}. Must be in the range [0, pi].")
        except ValueError:
            print(f"Invalid input '{angle}'. Please enter a valid number.")
            guesses.append(0)
    sys.compare_guess(guesses)

if __name__ == "__main__":
    main()
