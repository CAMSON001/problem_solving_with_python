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
 #Optimized
    def get_neighbors(self):
            x_pos = None
            for i, lst in enumerate(self.state):
                if "X" in lst:
                    x_pos = (i, lst.index("X"))
                    break

            if x_pos is None:
                return []

            i, j = x_pos
            new_states = []

            # Génération des voisins avec déplacement dans chaque direction possible
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, Bas, Gauche, Droite
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < 3 and 0 <= nj < 3:  # Vérification des limites
                    new_state = [row[:] for row in self.state]
                    new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                    new_states.append(Noeud(new_state, parent=self, coup=self.coup + 1))

            return new_states 
    
#Last self version 
    """ def get_neighbors(self):
        # Localisation de 'X'
        x_pos = None
        for i, lst in enumerate(self.state):
            if "X" in lst:
                x_pos = (i, lst.index("X"))
                break

        if x_pos is None:
            return []

        i, j = x_pos
        new_states = []

        # Définir les déplacements pour chaque cas de position de X
        if i == 0 or i == 2:  # Première ou dernière ligne
            if j == 0 or j == 2:  # Première ou dernière colonne
                # Échanger avec l'élément adjacent de la même ligne
                new_list = [elem for elem in self.state[i]]
                new_list[j], new_list[j + (1 if j == 0 else -1)] = new_list[j + (1 if j == 0 else -1)], new_list[j]
                new_state = [new_list if idx == i else lst for idx, lst in enumerate(self.state)]
                new_states.append(Noeud(new_state, parent=self, coup=self.coup + 1))

                # Échanger avec l'élément de la ligne adjacente ayant le même index de colonne
                new_list = [row[:] for row in self.state]
                new_list[i][j], new_list[i + (1 if i == 0 else -1)][j] = new_list[i + (1 if i == 0 else -1)][j], new_list[i][j]
                new_states.append(Noeud(new_list, parent=self, coup=self.coup + 1))

            elif j == 1:  # Colonne du milieu
                # Échanger avec les éléments adjacents de la même ligne
                for dj in [-1, 1]:
                    new_list = [elem for elem in self.state[i]]
                    new_list[j], new_list[j + dj] = new_list[j + dj], new_list[j]
                    new_state = [new_list if idx == i else lst for idx, lst in enumerate(self.state)]
                    new_states.append(Noeud(new_state, parent=self, coup=self.coup + 1))

                # Échanger avec l'élément de la ligne adjacente ayant le même index de colonne
                new_list = [row[:] for row in self.state]
                new_list[i][j], new_list[i + (1 if i == 0 else -1)][j] = new_list[i + (1 if i == 0 else -1)][j], new_list[i][j]
                new_states.append(Noeud(new_list, parent=self, coup=self.coup + 1))

        elif i == 1:  # Deuxième ligne
            if j == 0 or j == 2:  # Première ou dernière colonne
                # Échanger avec l'élément adjacent de la même ligne
                new_list = [elem for elem in self.state[i]]
                new_list[j], new_list[j + (1 if j == 0 else -1)] = new_list[j + (1 if j == 0 else -1)], new_list[j]
                new_state = [new_list if idx == i else lst for idx, lst in enumerate(self.state)]
                new_states.append(Noeud(new_state, parent=self, coup=self.coup + 1))

                # Échanger avec l'élément de la ligne du haut et du bas ayant le même index de colonne
                for di in [-1, 1]:
                    new_list = [row[:] for row in self.state]
                    new_list[i][j], new_list[i + di][j] = new_list[i + di][j], new_list[i][j]
                    new_states.append(Noeud(new_list, parent=self, coup=self.coup + 1))

            elif j == 1:  # Colonne du milieu
                # Échanger avec les éléments adjacents de la même ligne
                for dj in [-1, 1]:
                    new_list = [elem for elem in self.state[i]]
                    new_list[j], new_list[j + dj] = new_list[j + dj], new_list[j]
                    new_state = [new_list if idx == i else lst for idx, lst in enumerate(self.state)]
                    new_states.append(Noeud(new_state, parent=self, coup=self.coup + 1))

                # Échanger avec les éléments des lignes du haut et du bas ayant le même index de colonne
                for di in [-1, 1]:
                    new_list = [row[:] for row in self.state]
                    new_list[i][j], new_list[i + di][j] = new_list[i + di][j], new_list[i][j]
                    new_states.append(Noeud(new_list, parent=self, coup=self.coup + 1))

        return new_states """

  

    def afficher_chemin(self):
        chemin = []
        noeud = self
        while noeud:
            chemin.append(noeud)
            noeud = noeud.parent
        for n in reversed(chemin):
            print(n.state)
        print("Nombre de coups :", self.coup)


def game_taquin(init_state):
    init_state.heuristique()
    visited = []
    border = [init_state]
    
    while border:
        border.sort()
        current_node = border.pop(0)

        if current_node.is_goal():
            return current_node

        visited.append(current_node)

        for neighbor in current_node.get_neighbors():
            in_visited = any(node.state == neighbor.state for node in visited)
            in_border = any(node.state == neighbor.state for node in border)
            
            if not in_visited and not in_border:
                border.append(neighbor)
            elif in_visited:
                existing_node = next(node for node in visited if node.state == neighbor.state)
                if neighbor.total_cost < existing_node.total_cost:
                    visited.remove(existing_node)
                    border.append(neighbor)
            elif in_border:
                existing_node = next(node for node in border if node.state == neighbor.state)
                if neighbor.total_cost < existing_node.total_cost:
                    border.remove(existing_node)
                    border.append(neighbor)

# Exemple d'utilisation
init_state = Noeud([
    [3, 6, 8],
    [1, 2, 7],
    [5, 4, "X"]
])
result = game_taquin(init_state)
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
