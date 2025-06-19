# All angles are in radians

import math
import random
from matplotlib import pyplot as plt

class SingleQubit:
    def __init__(self, theta = 0):
        self.theta = theta % (2 * math.pi)
        self.history = [self.theta]
        self.basis_history = [(0, math.pi / 2)]

    def read_state(self):
        return self.theta
    
    def rotation(self, theta):
        self.theta = (self.theta + theta) % (2 * math.pi)
        self.history.append(self.theta)

    def reflection(self, theta):
        self.theta = (2 * theta - self.theta) % (2 * math.pi)
        self.history.append(self.theta)

    def draw_state(self):
        plt.figure()
        self._draw_unit_circle()
        self._draw_arrow(self.theta, label='Current State', color='blue')
        plt.title("Current Quantum State")
        plt.axis('equal')
        plt.show()

    def draw_all_states(self):
        plt.figure()
        self._draw_unit_circle()
        for idx, angle in enumerate(self.history):
            self._draw_arrow(angle, label=str(idx), color='blue')
            x, y = math.cos(angle), math.sin(angle)
            plt.text(x * 1.1, y * 1.1, str(idx), ha='center', va='center')
        plt.title("All Visited Quantum States")
        plt.axis('equal')
        plt.show()

    def reflect_and_draw(self, theta):
        plt.figure()
        self._draw_unit_circle()
        self._draw_arrow(self.theta, label='Before Reflection', color='red')
        self._draw_line(theta, label='Reflection Axis', color='green')
        self.reflection(theta)
        self._draw_arrow(self.theta, label='After Reflection', color='blue')
        plt.title("Reflection Operation")
        plt.axis('equal')
        plt.show()

    def prob(self):
        # Measure the probability of the state being in the |0> and |1> basis
        prob_0 = math.cos(self.theta / 2) ** 2
        prob_1 = math.sin(self.theta / 2) ** 2
        return prob_0, prob_1
    
    def measure(self, number_of_shots):
        Results = {0: 0, 1: 0}
        prob_0, prob_1 = self.prob()

        for _ in range(number_of_shots):
            if random.random() < prob_0:
                Results[0] += 1
            else:
                Results[1] += 1

        return Results
    
    def change_basis(self, theta):
        if math.isclose(theta, self.basis_history[-1][0]):
            raise ValueError("The basis is already the same as the last basis")
        
        self.basis_history.append((theta, theta + math.pi / 2))
        self.history = [(angle - theta) % (2 * math.pi) for angle in self.history]
        self.theta = self.history[-1]

    def draw_state_in_both_basis(self):
        if len(self.basis_history) < 2:
            raise ValueError("Not enough basis changes to draw the state in both bases")

        old_basis = self.basis_history[-2][0]
        new_basis = self.basis_history[-1][0]

        # Transform current theta back to old basis
        old_theta = (self.theta + new_basis - old_basis) % (2 * math.pi)

        fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        for ax, title, angle in zip(
            axes,
            ["Previous Basis", "Current Basis"],
            [old_theta, self.theta]
        ):
            self._draw_unit_circle(ax)
            self._draw_arrow(angle, label='State', color='red', ax=ax)
            ax.set_title(title)
            ax.set_aspect('equal')

        plt.tight_layout()
        plt.show()


    def prob_in_both_basis(self):
        if len(self.basis_history) < 2:
            raise ValueError("Not enough basis changes to calculate probabilities in both bases")

        old_basis = self.basis_history[-2][0]
        new_basis = self.basis_history[-1][0]

        old_theta = (self.theta + new_basis - old_basis) % (2 * math.pi)

        prob_0_old = math.cos(old_theta) ** 2
        prob_1_old = 1 - prob_0_old

        prob_0_new = math.cos(self.theta) ** 2
        prob_1_new = 1 - prob_0_new

        return {'new_basis': {'0': prob_0_new, '1': prob_1_new}, 'old_basis': {'0': prob_0_old, '1': prob_1_old}}

    def take_back_basis_change(self):
        if len(self.basis_history) < 2:
            return

        current_shift = self.basis_history[-1][0]
        previous_shift = self.basis_history[-2][0]
        net_shift = (current_shift - previous_shift)

        self.history = [(angle + net_shift) % (2 * math.pi) for angle in self.history]
        self.theta = self.history[-1]
        self.basis_history.pop()


    # Helpers
    def _draw_unit_circle(self, ax=None):
        if ax is None:
            ax = plt.gca()
        circle = plt.Circle((0, 0), 1, color='lightgray', fill=False)
        ax.add_artist(circle)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

    def _draw_arrow(self, angle, label=None, color='blue', ax=None):
        if ax is None:
            ax = plt.gca()
        x, y = math.cos(angle), math.sin(angle)
        ax.arrow(0, 0, x, y, head_width=0.05, head_length=0.1, fc=color, ec=color)
        if label:
            ax.text(x * 1.1, y * 1.1, label, ha='center', va='center', color=color)

    def _draw_line(self, angle, label=None, color='green'):
        x = math.cos(angle)
        y = math.sin(angle)
        plt.plot([-x, x], [-y, y], linestyle='--', color=color)
        if label:
            plt.text(x * 1.1, y * 1.1, label, ha='center', va='center', color=color)


def main():
    q = SingleQubit()
    q.rotation(math.pi/3)
    q.draw_state()
    q.reflect_and_draw(math.pi/4)
    print(q.prob())
    print(q.measure(1000))
    q.change_basis(math.pi/2)
    q.draw_state_in_both_basis()
    print(q.prob_in_both_basis())
    q.take_back_basis_change()
    q.draw_all_states()


if __name__ == "__main__":
    main()
