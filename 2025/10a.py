from _operator import concat
import helper

'''
pressing a button twice is the same as not pressing it at all (because toggling a light twice returns it to its original state). This means we only care about parity

The target state can be represented as a binary vector T
Each button can be represented as a binary vector B
We are looking to solve:
T = x_1B_1 + x_2B_2 + ... + x_nB_n

For the first example, the generated matrix looks like this.

B_0 ¦ B_1 ¦ B_2 ¦ B_3 ¦ B_4 ¦ B_5 ¦¦ T
--------------------------------------
0   ¦ 0   ¦ 0   ¦ 0   ¦ 1   ¦ 1   ¦¦ 0
0   ¦ 1   ¦ 0   ¦ 0   ¦ 0   ¦ 1   ¦¦ 1
0   ¦ 0   ¦ 1   ¦ 1   ¦ 1   ¦ 0   ¦¦ 1
1   ¦ 1   ¦ 0   ¦ 1   ¦ 0   ¦ 0   ¦¦ 0
'''

data = helper.get_data(10).strip("\n").split("\n")
lights = []
buttons = []
jotls = []

def main():
    total_presses = 0

    for i, line in enumerate(data):
        line_split = line.split(" ")

        tmp = []
        for light in line_split[0][1:-1]:
            tmp.append(1 if light == '#' else 0)
        lights.append(tmp)

        lights_length = len(tmp)
        n_buttons = len(line_split) - 2

        group = []
        for button in line_split[1:-1]:
            button_str = button.strip("()")
            binary_list = [0] * lights_length

            indices = [int(i.strip()) for i in button_str.split(',') if i.strip()]

            for index in indices:
                bit_position = lights_length - 1 - index

                if 0 <= bit_position < lights_length:
                    binary_list[bit_position] = 1

            group.append(binary_list[::-1])
        buttons.append(group)

        system_matrix = [[0] * (n_buttons + 1) for _ in range(lights_length)]

        for j, light in enumerate(lights[i]):
            system_matrix[j][n_buttons] = light

        for j, button in enumerate(buttons[i]):
            for k, b in enumerate(button):
                system_matrix[k][j] = b

        result = solve_system_gf2(system_matrix)
        minimal_presses = find_minimal_presses_complete(result, n_buttons)
        total_presses += minimal_presses

    return total_presses

def solve_system_gf2(matrix):
    """
    Performs Gaussian Elimination on an augmented matrix over the field GF(2).

    Args:
        matrix: A list of lists representing the augmented matrix.
                The last column is the target/result vector.

    Returns:
        The matrix in row echelon form, or None if no solution exists
        due to an inconsistency.
    """
    num_rows = len(matrix)
    num_cols = len(matrix[0]) - 1 # Exclude the augmented column

    current_row = 0

    for current_col in range(num_cols):
        # 1. Find a non-zero pivot (a '1') in the current column below current_row
        pivot_row = current_row
        while pivot_row < num_rows and matrix[pivot_row][current_col] == 0:
            pivot_row += 1

        # If we reached the bottom without a 1, move to the next column
        if pivot_row == num_rows:
            continue

        # 2. Swap rows to bring the pivot to the current_row position
        matrix[current_row], matrix[pivot_row] = matrix[pivot_row], matrix[current_row]

        # 3. Eliminate all other 1s below the pivot row using XOR (addition mod 2)
        for i in range(current_row + 1, num_rows):
            if matrix[i][current_col] == 1:
                # XOR the entire pivot row with the current row
                for j in range(num_cols + 1): # Include the augmented column in the XOR
                    matrix[i][j] ^= matrix[current_row][j]
        
        # Move to the next row (since we secured this pivot position)
        current_row += 1
        
        # Stop if we run out of rows
        if current_row >= num_rows:
            break

    # Check for inconsistencies (e.g., [0, 0, ..., 0 | 1] row)
    for i in range(current_row, num_rows):
        # Check if all coefficients are zero, but the target is 1
        if any(matrix[i][j] == 1 for j in range(num_cols)):
            # This shouldn't trigger if the algorithm is working perfectly, 
            # but it's the conceptual check for unsolvable systems.
            pass 
        elif matrix[i][num_cols] == 1:
            print("System is inconsistent (no solution exists)!")
            return None
            
    # The matrix is now in row echelon form. 
    # You need to implement the back-substitution and the min-presses search next.
    return matrix

from itertools import product

def find_minimal_presses_complete(reduced_matrix, num_buttons):
    """
    Identifies free variables from the row-echelon form matrix, 
    iterates through all possibilities, performs back-substitution, 
    and finds the solution with the minimum number of 1s (presses).
    """
    num_lights = len(reduced_matrix)
    
    # 1. Map rows to their pivot columns (or None if a zero row)
    pivot_map = {}
    row_idx = 0
    for col_idx in range(num_buttons):
        # Find the row that has its pivot in this column
        while row_idx < num_lights and reduced_matrix[row_idx][col_idx] == 0:
            row_idx += 1
        
        if row_idx < num_lights:
            pivot_map[col_idx] = row_idx
            row_idx += 1
    
    # Identify free variables by finding which column indices *don't* have a pivot row mapped to them
    free_cols = [c for c in range(num_buttons) if c not in pivot_map]
    
    min_presses = float('inf')

    # 2. Iterate through all combinations of 0/1 for the free variables
    # (2^F combinations, where F is the number of free variables)
    for free_values_tuple in product([0, 1], repeat=len(free_cols)):
        
        # Initialize the solution vector for this iteration
        # e.g., current_solution[3] = 0, current_solution[5] = 1
        current_solution = [0] * num_buttons
        
        # Assign values of the free variables
        for i, col_index in enumerate(free_cols):
            current_solution[col_index] = free_values_tuple[i]
            
        # 3. Perform back-substitution for the pivot variables
        # Iterate backward through the pivot rows
        for col_index in sorted(pivot_map.keys(), reverse=True):
            row_idx = pivot_map[col_index]
            
            # The equation for this pivot row is:
            # (1 * X_pivot) XOR (coeffs * remaining X_vars) = Target
            
            # Start with the target value for this row
            calculated_pivot_value = reduced_matrix[row_idx][num_buttons] # The augmented column value
            
            # XOR with all other terms (which are either free vars or already calculated pivot vars)
            for j in range(col_index + 1, num_buttons):
                coefficient = reduced_matrix[row_idx][j]
                if coefficient == 1:
                    # XOR away the contribution of this known variable (current_solution[j])
                    calculated_pivot_value ^= current_solution[j]
            
            # Assign the resulting value to the pivot variable
            current_solution[col_index] = calculated_pivot_value
        
        # 4. Validate the solution against ALL rows in the reduced matrix
        valid = True
        for row_idx in range(num_lights):
            # Calculate the left side of the equation for this row
            left_side = 0
            for col_idx in range(num_buttons):
                if reduced_matrix[row_idx][col_idx] == 1:
                    left_side ^= current_solution[col_idx]
            
            # Check if it equals the right side (target)
            right_side = reduced_matrix[row_idx][num_buttons]
            if left_side != right_side:
                valid = False
                break
        
        # Only count valid solutions
        if valid:
            press_count = sum(current_solution)
            min_presses = min(min_presses, press_count)
        
    return min_presses


if __name__ == "__main__":
    print(main())
