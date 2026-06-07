from ortools.linear_solver import pywraplp
import pandas as pd

# Load data
df_dados_gerais = pd.read_csv('dados/dados-gerais.csv')
df_dados_arcos = pd.read_csv('dados/dados-arcos.csv')

num_vertices = int(df_dados_gerais['num_vertices'][0])
vertices = list(range(1, num_vertices + 1))
arcos = [(row.origem, row.destino, row.custo) for row in df_dados_arcos.itertuples()]

# Setup Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
infinity = solver.infinity()

x = {(i, j): solver.BoolVar(f'x{i}{j}') for i, j, c in arcos}
u = {i: solver.IntVar(2, num_vertices, f'u{i}') for i in vertices if i != 1}

# Objective
objetivo = solver.Objective()
for i, j, c in arcos:
    objetivo.SetCoefficient(x[(i, j)], c)
objetivo.SetMinimization()

# Output constraint
for v in vertices:
    c_out = solver.Constraint(1, 1, f'saida_{v}')
    for i, j, c in arcos:
        if i == v:
            c_out.SetCoefficient(x[(i, j)], 1)

# Input constraint
for v in vertices:
    c_in = solver.Constraint(1, 1, f'entrada_{v}')
    for i, j, c in arcos:
        if j == v:
            c_in.SetCoefficient(x[(i, j)], 1)

# MTZ subtour elimination
for i, j, c in arcos:
    if i != 1 and j != 1:
        c_mtz = solver.Constraint(-infinity, num_vertices - 1, f'mtz_{i}_{j}')
        c_mtz.SetCoefficient(u[i], 1)
        c_mtz.SetCoefficient(u[j], -1)
        c_mtz.SetCoefficient(x[(i, j)], num_vertices)

# Solve 1
print("--- SOLVE 1 ---")
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    custo1 = int(round(objetivo.Value()))
    rota1 = []
    proximo = {}
    for i, j, c in arcos:
        if x[(i, j)].solution_value() > 0.5:
            proximo[i] = j
    atual = 1
    for _ in range(num_vertices):
        rota1.append(atual)
        atual = proximo[atual]
    rota1.append(1)
    print(f"Rota 1: {' -> '.join(map(str, rota1))}")
    print(f"Custo 1: {custo1}")
else:
    print("No optimal solution 1")
    exit(1)

# Save active variables before modifying model
active_vars = []
for (i, j), var in x.items():
    if var.solution_value() > 0.5:
        active_vars.append((i, j, var))

# Add Q1 Cut Constraint
print("\n--- ADDING Q1 CUT ---")
c_cut = solver.Constraint(-infinity, num_vertices - 1)
for i, j, var in active_vars:
    print(f"Corte: adicionando x[{i},{j}] ao corte")
    c_cut.SetCoefficient(var, 1)

# Solve 2
print("\n--- SOLVE 2 ---")
status2 = solver.Solve()
if status2 == pywraplp.Solver.OPTIMAL:
    custo2 = int(round(objetivo.Value()))
    rota2 = []
    proximo2 = {}
    for i, j, c in arcos:
        if x[(i, j)].solution_value() > 0.5:
            proximo2[i] = j
    atual = 1
    for _ in range(num_vertices):
        rota2.append(atual)
        atual = proximo2[atual]
    rota2.append(1)
    print(f"Rota 2: {' -> '.join(map(str, rota2))}")
    print(f"Custo 2: {custo2}")
else:
    print("No optimal solution 2")
