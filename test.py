import heapq

class Noeud:
    def __init__(self, state, parent=None, coup=0):
        self.state = state
        self.parent = parent
        self.coup = coup
        self.heuristique_n = 0
        self.etat_final = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, "X"]
        ]
        self.heuristique()
        self.total_cost = self.coup + self.heuristique_n

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def is_goal(self):
        return self.state == self.etat_final

    def heuristique(self):
        """Calculer l'heuristique basée sur la distance de Manhattan."""
        h = 0
        for i, row in enumerate(self.state):
            for j, valeur in enumerate(row):
                if valeur != "X":
                    for x, row_final in enumerate(self.etat_final):
                        if valeur in row_final:
                            y = row_final.index(valeur)
                            h += abs(i - x) + abs(j - y)
                            break
        self.heuristique_n = h

    def get_neighbors(self):
        """Retourne les voisins en déplaçant 'X' dans toutes les directions possibles."""
        x_pos = None
        for i, lst in enumerate(self.state):
            if "X" in lst:
                x_pos = (i, lst.index("X"))
                break

        if x_pos is None:
            return []

        i, j = x_pos
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for di, dj in moves:
            ni, nj = i + di, j + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                new_state = [row[:] for row in self.state]
                new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                neighbors.append(Noeud(new_state, parent=self, coup=self.coup + 1))

        return neighbors

def game_taquin(init_state):
    """Algorithme A* pour résoudre le Taquin."""
    visited = {}
    border = []
    heapq.heappush(border, (init_state.total_cost, init_state))

    while border:
        _, current_node = heapq.heappop(border)

        if current_node.is_goal():
            return current_node

        current_state_tuple = tuple(map(tuple, current_node.state))

        # Marquer cet état comme visité avec le coût associé
        if current_state_tuple in visited and visited[current_state_tuple] <= current_node.total_cost:
            continue

        visited[current_state_tuple] = current_node.total_cost

        for neighbor in current_node.get_neighbors():
            neighbor_state_tuple = tuple(map(tuple, neighbor.state))

            # Si le voisin n'est pas visité ou a un coût inférieur, ajouter à la frontière
            if neighbor_state_tuple not in visited or neighbor.total_cost < visited[neighbor_state_tuple]:
                heapq.heappush(border, (neighbor.total_cost, neighbor))

    return None  # Retourne None si aucune solution n'est trouvée

# Exemple d'utilisation
init_state = Noeud([
    [3, 6, 8],
    [1, 2, 7],
    [5, 4, "X"]
])
result = game_taquin(init_state)

# Affichage du résultat
if result:
    solution_path = []
    while result:
        solution_path.append(result.state)
        result = result.parent
    solution_path.reverse()
    print("Chemin vers la solution :")
    for state in solution_path:
        for row in state:
            print(row)
        print("----")
else:
    print("Aucune solution trouvée.")
