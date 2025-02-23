import json
import subprocess

from create_grid import create_hexagonal_grid, create_rectangular_grid
from make_paths import select_node_pairs_hex, select_node_pairs_rec


def run_command(command, shortEnding=False):
    try:
        resultat = subprocess.run(command, capture_output=True)
        sortie = str(resultat.stdout)
        sortie_split = sortie.split("\\n")
        is_satisfiable = False
        answer = "v"
        for line in sortie_split:
            if len(line) > 0 and line[0] == "s":
                is_satisfiable = "UNSATISFIABLE" not in line
            if len(line) > 0 and line[0] == "v":
                if shortEnding:
                    answer = line[2:]
                else:
                    answer = line[2:-2]
        return is_satisfiable, answer

    except subprocess.CalledProcessError as e:
        print(f"erreur survenue lors de l'execution de la commande {e}")
        return False, False


class NumberlinkSolver:
    def __init__(self, V, E, X):
        # G=(V,E) X=[(s1,t1)...(sk,tk)] pairs to join
        self.V = V
        self.E = E
        self.X = X
        self.k = len(X)
        self.n = len(V)
        self.xvip = [
            f"x_{v}_{i}_{p}"
            for v in range(self.n)
            for i in range(self.k)
            for p in range(self.n)
        ]
        self.xphant_ip = [
            f"xphant_{i}_{p}" for i in range(self.k) for p in range(self.n)
        ]
        self.no_none = self.__count_no_none__()

    def __count_no_none__(self):
        count = 0
        for v in self.V:
            if v is not None:
                count += 1
        return count

    def constraint_one(self, v):
        # Each vertex v appears at a single position in a single path
        clauses = []

        # At least appears at one position and path
        if v < self.no_none:
            at_least_one = " ".join([f'x_{v}_{i}_{p}' for i in range(self.k) for p in range(self.n)])
            clauses.append(at_least_one)

        # At most appears at one path
        for i in range(self.k):
            for j in range(i + 1, self.k):
                for p in range(self.n):
                    for q in range(self.n):
                        clauses.append(f"-x_{v}_{i}_{p} -x_{v}_{j}_{q}")

        # At most appears at one position
        for i in range(self.k):
            for p in range(self.n):
                for q in range(p + 1, self.n):
                    clauses.append(f"-x_{v}_{i}_{p} -x_{v}_{i}_{q}")
        return clauses

    def constraint_two(self, i, p):
        # Each position p in a path i is occupied by exactly one vertex (or phantom vertex)
        clauses = []
        at_least_one = " ".join(
            [f"x_{v}_{i}_{p}" for v in range(self.n)] + [f"xphant_{i}_{p}"]
        )
        clauses.append(at_least_one)
        for v1 in range(self.n):
            for v2 in range(v1 + 1, self.n):
                clauses.append(f"-x_{v1}_{i}_{p} -x_{v2}_{i}_{p}")
            clauses.append(f"-x_{v1}_{i}_{p} -xphant_{i}_{p}")
        return clauses

    def constraint_three(self, i, p):
        # If a path i is finished before position p, it is also finished before p+1
        return [f"-xphant_{i}_{p} xphant_{i}_{p+1}"]

    def constraint_four(self, i, p):
        # for each index i, consecutive vertices along the path i are adjacent in G
        clauses = []
        for v1 in range(self.n):
            for v2 in range(self.n):
                if (v1, v2) not in self.E and (v2, v1) not in self.E and v1 != v2:
                    clauses.append(f"-x_{v1}_{i}_{p} -x_{v2}_{i}_{p+1}")
        return clauses

    def constraint_five(self, i):
        # for each index i, the source si appears first and the sink ti is followed by phantom vertex
        s_i, t_i = self.X[i]
        clauses = [
            f"x_{s_i}_{i}_{0}",
        ]
        for p in range(self.n):
            # all following t_i are phantom
            k = 1
            while k < self.n - p:
                clauses.append(f"-x_{t_i}_{i}_{p} xphant_{i}_{p+k}")
                k += 1
        t_exists = " ".join([f"x_{t_i}_{i}_{p}" for p in range(self.n)])
        clauses.append(t_exists)
        return clauses

    def get_constraints(self):
        all_constraints = []
        for v in range(self.n):
            all_constraints.extend(self.constraint_one(v))
        for i in range(self.k):
            for p in range(self.n):
                all_constraints.extend(self.constraint_two(i, p))
                if p < self.n - 1:
                    all_constraints.extend(self.constraint_three(i, p))
                    all_constraints.extend(self.constraint_four(i, p))
            all_constraints.extend(self.constraint_five(i))
        return all_constraints


config = json.load(open("config.json", "r"))

# Squared case
grid_size = config["grid_size"]
# x_human = [
#     ((0, 3), (6, 4)),
#     ((1, 1), (2, 3)),
#     ((1, 4), (6, 0)),
#     ((1, 5), (3, 3)),
#     ((2, 4), (5, 2)),
# ] # Couples of cartesian coordinates of ((s_i x, s_i y) (t_i x, t_i y))
# Hexagonal case
# x_human = [
#     ((0,3),(6,0)),
#     ((0,4),(6,1)),
#     ((0,5),(6,2)),
#     ((0,6),(6,3)),
#     ((1,6),(5,4)),
#     ((2,6),(3,6))
# ]
# x_human = [
#     ((0, 4), (6, 0)),
#     ((0, 6), (6, 1)),
#     ((1, 3), (3, 2)),
#     ((1, 5), (5, 3)),
#     ((2, 2), (5, 1)),
#     ((2, 5), (4, 3)),
#     ((3, 6), (6, 2)),
# ]
shape = config["shape"]
if shape == "rectangle":
    x_human = select_node_pairs_rec(grid_size)
elif shape == "hexagon":
    x_human = select_node_pairs_hex(grid_size)
else:
    raise ValueError("shape must be either 'rectangle' or 'hexagon'")
config["extremities"] = x_human
json.dump(config, open("config.json", "w"))

if shape == "rectangle":
    V, E, X = create_rectangular_grid(grid_size, x_human)
else:
    V, E, X = create_hexagonal_grid(grid_size, x_human)
print(V, E, X)
solver = NumberlinkSolver(V, E, X)
clauses = solver.get_constraints()
correspondance_dict = {}
j = 0
for v in range(solver.n):
    for i in range(solver.k):
        for p in range(solver.n):
            correspondance_dict[f"x_{v}_{i}_{p}"] = j + 1
            j += 1
for i in range(solver.k):
    for p in range(solver.n):
        correspondance_dict[f"xphant_{i}_{p}"] = j + 1
        j += 1
constraint = []
for clause in clauses:
    clause_int = []
    vars = clause.split(" ")
    for var in vars:
        if var[0] == "-":
            clause_int.append(-correspondance_dict[var[1:]])
        else:
            clause_int.append(correspondance_dict[var])
    clause_int.append(0)
    clause_int = " ".join(map(str, clause_int))
    constraint.append(clause_int)

with open("numberlink.cnf", "w") as f:
    f.write(f"p cnf {len(correspondance_dict)} {len(constraint)}\n")
    for condition in constraint:
        f.write(f"{condition}\n")

f.close()


def solve_sokoban(path):
    command = ["gophersat", "--verbose", path]
    is_satisfiable, answer = run_command(command)
    return is_satisfiable, answer


path = "numberlink.cnf"
is_sat, answer = solve_sokoban(path)

if is_sat:
    print("Solution found")
    with open("answer.txt", "w") as f:
        f.write(f"{answer}")
        f.close()
else:
    print("No solution found")
