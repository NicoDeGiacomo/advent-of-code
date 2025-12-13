import helper

'''

'''

data = helper.get_data(12).strip()

ALL_SHAPES = {}
ALL_REGIONS = []

def main():
    for line in data.split('\n\n'):
        X = {}
        Y = {}

        if line[1] == ':':
            shape_index = int(line[0])
            ALL_SHAPES[shape_index] = []
            for i, row in enumerate(line.split('\n')[1:]):
                for j, col in enumerate(row):
                    if col == '#':
                        ALL_SHAPES[shape_index].append((i, j))
        else:
            for system in line.split('\n'):
                dimensions, requirements = system.split(':')
                
                w, h = map(int, dimensions.split('x'))
                requirements_ints = list(map(int, requirements.strip().split()))

                counts = {i: requirements_ints[i] for i in range(len(requirements_ints))}

                ALL_REGIONS.append((w, h, counts))

    solvable_count = 0
    for region in ALL_REGIONS:
        if solve_region(region):
            solvable_count += 1

    return solvable_count

def solve_region(region):
    w, h, counts = region
    
    # Pre-compute all variations for available shapes
    available_shapes = {}
    total_requested_area = 0
    
    for shape_id, count in counts.items():
        if count > 0:
            available_shapes[shape_id] = get_variations(ALL_SHAPES[shape_id])
            total_requested_area += len(ALL_SHAPES[shape_id]) * count
            
    # Optimization: Area check
    if total_requested_area > w * h:
        return False
    
    # Flatten counts to list of IDs
    pieces = []
    for shape_id, count in counts.items():
        pieces.extend([shape_id] * count)
        
    # Sort by size
    pieces.sort(key=lambda sid: len(ALL_SHAPES[sid]), reverse=True)
    
    occupied_cells = set()
    def backtrack(idx):
        if idx == len(pieces):
            return True
            
        shape_id = pieces[idx]
        variations = available_shapes[shape_id]
                
        for x in range(w):
            for y in range(h):
                if (x, y) in occupied_cells:
                    continue

                for shape in variations:
                    newly_occupied = []
                    fits = True
                    for dx, dy in shape:
                        nx, ny = x + dx, y + dy
                        if not (0 <= nx < w and 0 <= ny < h):
                            fits = False
                            break
                        if (nx, ny) in occupied_cells:
                            fits = False
                            break
                        newly_occupied.append((nx, ny))
                    
                    if fits:
                        for pos in newly_occupied:
                            occupied_cells.add(pos)
                        
                        if backtrack(idx + 1):
                            return True
                        
                        # Backtrack
                        for pos in newly_occupied:
                            occupied_cells.remove(pos)
                            
        return False

    return backtrack(0)

def get_variations(shape_coords):
    """
    Generates all 8 symmetries (rotations and flips) of a shape.
    Normalizes coordinates to start at (0,0).
    """
    variations = []
    
    current = shape_coords
    for _ in range(2): # Flip
        for _ in range(4): # Rotate
            if not current:
                variations.append([])
            else:
                # Normalize
                min_r = min(r for r, c in current)
                min_c = min(c for r, c in current)
                normalized = sorted([(r - min_r, c - min_c) for r, c in current])
                
                if normalized not in variations:
                    variations.append(normalized)
            
            # Rotate 90 deg clockwise: (r, c) -> (c, -r)
            current = [(c, -r) for r, c in current]
            
        # Flip: (r, c) -> (r, -c)
        current = [(r, -c) for r, c in shape_coords]
        
    return variations

if __name__ == "__main__":
    print(main())
