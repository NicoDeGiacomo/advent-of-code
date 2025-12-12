import helper
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


'''
This second part of the problem transforms the challenge from a binary (modulo 2) system to an integer-based system. We are no longer toggling states; we are accumulating counts.
- The target joltage vector T is a vector of positive integers.
- Each button vector B_i represents which counters increase by 1 when pressed

We are looking to solve:
T = x_1B_1 + x_2B_2 + ... + x_nB_n

With constraints: 
- x_i >= 0
- sum(x_i) is minimal
'''

data = helper.get_data(10).strip("\n").split("\n")

jolts = []
buttons = []

def main():
    total_presses = 0

    for i, line in enumerate(data):
        line_split = line.split(" ")

        tmp = []
        for jolt in line_split[-1].strip("{}").split(","):
            tmp.append(int(jolt))
        jolts.append(tmp)

        jolts_length = len(tmp)
        n_buttons = len(line_split) - 2

        group = []
        for button in line_split[1:-1]:
            button_str = button.strip("()")
            binary_list = [0] * jolts_length

            indices = [int(i.strip()) for i in button_str.split(',') if i.strip()]

            for index in indices:
                bit_position = jolts_length - 1 - index

                if 0 <= bit_position < jolts_length:
                    binary_list[bit_position] = 1

            group.append(binary_list[::-1])
        buttons.append(group)

        # Build coefficient matrix (buttons only, no target column)
        A = np.zeros((jolts_length, n_buttons))
        for j, button in enumerate(buttons[i]):
            for k, b in enumerate(button):
                A[k][j] = b

        # Target vector
        b = np.array(jolts[i])

        # Objective: minimize sum of button presses
        c = np.ones(n_buttons)
        
        # Constraints: A @ x = b (equality constraints)
        constraints = [LinearConstraint(A, b, b)]

        # All variables must be non-negative integers
        integrality = np.ones(n_buttons)
        bounds = Bounds(lb=0, ub=np.inf)

        res = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)
        
        if res.success:
            total_presses += res.fun
        else:
            print(f"Failed to solve machine {i}: {res.message}")
            return None

    return int(total_presses)

if __name__ == "__main__":
    print(main())
