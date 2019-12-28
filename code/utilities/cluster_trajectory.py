"""
Inputs:
    df = {o1, o2, o3, ...}
    outer = Outer radius for density calculation
    inner = Inner radius for density calculation
    minPts = Minimum number of points in neighbourhood
"""
def t_dbscan(df, outer, inner, minPts):
    
    centers = 0
    Cp = {}
    UNMARKED = 777777

    df["cluster"] = UNMARKED
    df["visited"] = False
    maxID = -1

    for index, row in df.iterrows():
        if index > maxID:
            df.set_value(index, 'visited', True)
            # Search for continuous density-based neighbors N
            N = getNeighbors(row, outer, inner, df, index)
            maxID = index
            # Create new cluster
            if len(N) > minPts:
                centers += 1
            # Expand the cluster