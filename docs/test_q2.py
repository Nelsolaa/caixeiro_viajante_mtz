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

# Q2 Constraint: Force 2 -> 3
c_q2 = solver.Constraint(1, 1)
c_q2.SetCoefficient(x[(2, 3)], 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    custo = int(round(objetivo.Value()))
    rota = []
    proximo = {}
    for i, j, c in arcos:
        if x[(i, j)].solution_value() > 0.5:
            proximo[i] = j
    atual = 1
    for _ in range(num_vertices):
        rota.append(atual)
        atual = proximo[atual]
    rota.append(1)
    print(f"Rota: {' -> '.join(map(str, rota))}")
    print(f"Custo: {custo}")
else:
    print("No optimal solution")
