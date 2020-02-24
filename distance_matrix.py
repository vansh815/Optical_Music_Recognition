import collections

def distance_matrix(A):
    """
    :param A: Edge detected image
    :return: Distance of nearest edge (1) for every pixel
    """
    R, C = len(A), len(A[0])

    def neighbors(r, c):
        for cr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= cr < R and 0 <= cc < C:
                yield cr, cc

    q = collections.deque([((r, c), 0, 0, 0)
                           for r in range(R)
                           for c in range(C)
                           if A[r][c] == 1])
   
    #seen = {(-1,-1)}
    seen = {x for x,_,_,_ in q}

    ans = [[1] * C for _ in A]

    # BFS to find nearest edge (1) for every pixel
    while q:
        (r, c), depth, parent_i, parent_j = q.popleft()
        if A[r][c] == 1:
            ans[r][c] = 0
        else:
            ans[r][c] = round(math.sqrt((r-parent_i)**2 + (c-parent_j)**2))
        for nei in neighbors(r, c):
            if nei not in seen:
                seen.add(nei)
                if depth+1 == 1:
                    q.append((nei, depth+1, r,c))
                elif depth+1 > 1:
                    q.append((nei, depth + 1,parent_i,parent_j))

    return ans