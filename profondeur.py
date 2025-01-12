

class State:
    def __init__(self, boxes):
        self.boxes = boxes  # boxes est une liste de listes représentant les cubes dans chaque boîte

    def is_goal(self, goal_state):
        return self.boxes == goal_state

    def get_neighbors(self):
        neighbors = []
        # Boucle à travers les boîtes pour effectuer des mouvements
        for i in range(len(self.boxes)):
            if self.boxes[i]:  # Vérifier si la boîte i n'est pas vide
                # Prendre le cube du haut de la boîte i
                cube_to_move = self.boxes[i][-1]  # Le cube du haut

                for j in range(len(self.boxes)):
                    if i != j:  # Ne pas se déplacer dans la même boîte
                        # Créer un nouvel état en déplaçant le cube
                        new_boxes = [box[:] for box in self.boxes]  # Copier l'état actuel des boîtes
                        new_boxes[i].pop()  # Retirer le cube du haut de la boîte i
                        new_boxes[j].append(cube_to_move)  # Ajouter le cube au haut de la boîte j
                        neighbors.append(State(new_boxes))
        
        return neighbors

def dfs(initial_state, goal_state, visited=None):
    if visited is None:
        visited = set()
    
    # Convertir l'état actuel en tuple pour le stockage dans visited
    state_tuple = tuple(tuple(box) for box in initial_state.boxes)
    if state_tuple in visited:
        return None  # Si l'état a déjà été visité, retourner None
    
    print(initial_state.boxes)  # Afficher l'état actuel
    visited.add(state_tuple)  # Marquer cet état comme visité

    if initial_state.is_goal(goal_state):
        return initial_state.boxes  # Retourner l'état final trouvé

    for neighbor in initial_state.get_neighbors():
        result = dfs(neighbor, goal_state, visited)  # Appeler DFS sur l'état voisin
        if result:
            return result  # Retourner l'état trouvé si c'est un succès

    return None  # Aucune solution trouvée

# Exemple d'utilisation
initial_state = State([['B', 'A'], ['C'], []])  # État initial
goal_state = [['A'], ['B'], ['C']]  # État final souhaité

result = dfs(initial_state, goal_state)
if result:
    print(f"État final atteint avec dfs: {result}")
else:
    print("Aucune solution trouvée.")
