import helper

"""
Coordinate Compression
   - The coordinates are large (~100,000) but the number of vertices is small (~500).
   - We map the unique X and Y coordinates to sorted indices 0..N.
   - This creates a non-uniform grid where 'cells' represent rectangular regions of the original space.
   - A cell `grid[i][j]` corresponds to the region `[xs[i], xs[i+1]]` x `[ys[j], ys[j+1]]`.

Sweep Line Algorithm (Polygon Interior)
   - To determine which cells are "inside" the polygon, we use a sweep-line approach.
   - For each row of the grid, we scan from left to right.
   - We toggle an "inside/outside" state whenever we cross a vertical edge of the polygon.
   - This fills a logical boolean grid `inside[W][H]`.

2D Prefix Sums
   - We precompute 2D prefix sums for the `inside` grid and valid edges.
   - Let `S[x][y]` be the sum of values from `(0,0)` to `(x,y)`.
   - The sum of a sub-rectangle `(x1, y1)` to `(x2, y2)` is `S[x2][y2] - S[x1][y2] - S[x2][y1] + S[x1][y1]`.
   - This allows us to check if a candidate rectangle is fully valid in O(1) time.
"""

data = helper.get_data(9).strip("\n").split("\n")
raw_points = [tuple(map(int, line.split(","))) for line in data]

def solve():
    # Coordinate Compression
    xs = sorted(list(set(p[0] for p in raw_points)))
    ys = sorted(list(set(p[1] for p in raw_points)))
    
    x_map = {x: i for i, x in enumerate(xs)}
    y_map = {y: i for i, y in enumerate(ys)}
    
    W = len(xs) - 1
    H = len(ys) - 1
    
    # Grid[i][j] is True if cell [xs[i], xs[i+1]] x [ys[j], ys[j+1]] is inside
    inside = [[False for _ in range(H)] for _ in range(W)]
    
    # Sweep Line to build Inside Grid
    # Events: vertical edges of the polygon
    # Polygon edges connect p[i] to p[i+1]
    
    # Build vertical segments
    v_segments = []
    n_points = len(raw_points)
    for k in range(n_points):
        p1 = raw_points[k]
        p2 = raw_points[(k + 1) % n_points]
        
        if p1[0] == p2[0]:
            x = p1[0]
            if x not in x_map:
                continue
            xi = x_map[x]
            
            y_start = min(p1[1], p2[1])
            y_end = max(p1[1], p2[1])
            
            yi_start = y_map[y_start]
            yi_end = y_map[y_end]
            
            for j in range(yi_start, yi_end):
                v_segments.append((xi, j))
    
    v_segments.sort()
    
    # For each row j, find all vertical edges crossing it
    row_v_edges = [[] for _ in range(H)]
    for xi, j in v_segments:
        if 0 <= j < H:
            row_v_edges[j].append(xi)
            
    for j in range(H):
        row_v_edges[j].sort()

        # A vertical polygon edge flips the inside/outside state
        current_inside = False
        edge_idx = 0
        edges = row_v_edges[j]
        
        for i in range(W):
            # Check if there is an edge at the LEFT boundary of this cell (line i)
            # There might be multiple overlapping edges
            if edge_idx < len(edges) and edges[edge_idx] == i:
                current_inside = not current_inside
                edge_idx += 1
                # Handle duplicate edges
                while edge_idx < len(edges) and edges[edge_idx] == i:
                    current_inside = not current_inside
                    edge_idx += 1
            
            inside[i][j] = current_inside

    # Build Edge Validities
    # h_edge_valid[i][j] : segment at y=ys[j] between xs[i] and xs[i+1]
    # v_edge_valid[i][j] : segment at x=xs[i] between ys[j] and ys[j+1]
    h_edge_valid = [[False for _ in range(H + 1)] for _ in range(W)]
    for i in range(W):
        for j in range(H + 1):
            top_in = inside[i][j-1] if j > 0 else False
            bot_in = inside[i][j] if j < H else False
            h_edge_valid[i][j] = top_in or bot_in
    v_edge_valid = [[False for _ in range(H)] for _ in range(W + 1)]
    for i in range(W + 1):
        for j in range(H):
            left_in = inside[i-1][j] if i > 0 else False
            right_in = inside[i][j] if i < W else False
            v_edge_valid[i][j] = left_in or right_in

    # Prefix Sums
    def build_prefix_sum(grid, w, h):
        psum = [[0 for _ in range(h + 1)] for _ in range(w + 1)]
        for i in range(w):
            for j in range(h):
                psum[i+1][j+1] = psum[i][j+1] + psum[i+1][j] - psum[i][j] + (1 if grid[i][j] else 0)
        return psum
    
    def query(psum, x1, y1, x2, y2):
        # Sum inclusive from (x1, y1) to (x2, y2)
        return psum[x2+1][y2+1] - psum[x1][y2+1] - psum[x2+1][y1] + psum[x1][y1]

    grid_psum = build_prefix_sum(inside, W, H)
    h_edge_psum = build_prefix_sum(h_edge_valid, W, H + 1)
    v_edge_psum = build_prefix_sum(v_edge_valid, W + 1, H)

    biggest_area = 0

    # Check all pairs
    mapped_points = [(x_map[p[0]], y_map[p[1]]) for p in raw_points]

    for k1 in range(n_points):
        p1_orig = raw_points[k1]
        ix1, iy1 = mapped_points[k1]
        
        for k2 in range(n_points):
            if k1 == k2:
                continue
            
            p2_orig = raw_points[k2]
            ix2, iy2 = mapped_points[k2]
            
            # Normalize coords for checking
            rx1, rx2 = min(ix1, ix2), max(ix1, ix2)
            ry1, ry2 = min(iy1, iy2), max(iy1, iy2)
            
            valid = False
            
            if rx1 == rx2:
                # I will assume no vertical line will have the biggest area
                continue
            elif ry1 == ry2:
                # I will assume no horizontal line will have the biggest area
                continue
            else:
                count = query(grid_psum, rx1, ry1, rx2 - 1, ry2 - 1)
                expected = (rx2 - rx1) * (ry2 - ry1)
                if count == expected:
                    valid = True
            
            if valid:
                area = calculate_area(p1_orig, p2_orig)
                if area > biggest_area:
                    biggest_area = area

    return biggest_area

def calculate_area(p1, p2):
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)

if __name__ == "__main__":
    print(solve())
