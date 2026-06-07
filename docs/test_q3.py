from ortools.linear_solver import pywraplp
import pandas as pd

df_dados_gerais = pd.read_csv('dados/dados-gerais.csv')
df_dados_arcos = pd.read_csv('dados/dados-arcos.csv')

num_vertices = int(df_dados_gerais['num_vertices'][0])
vertices = list(range(1, num_vertices + 1))
arcos = [(row.origem, row.destino, row.custo) for row in df_dados_arcos.itertuples()]

def solve_with_objective(set_coef_func):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    infinity = solver.infinity()
    
    x = {(i, j): solver.BoolVar(f'x{i}{j}') for i, j, c in arcos}
    u = {i: solver.IntVar(2, num_vertices, f'u{i}') for i in vertices if i != 1}
    
    objetivo = solver.Objective()
    for i, j, c in arcos:
        coef = set_coef_func(c)
        objetivo.SetCoefficient(x[(i, j)], coef)
    objetivo.SetMinimization()
    
    for v in vertices:
        c_out = solver.Constraint(1, 1, f'saida_{v}')
        for i, j, c in arcos:
            if i == v:
                c_out.SetCoefficient(x[(i, j)], 1)
                
    for v in vertices:
        c_in = solver.Constraint(1, 1, f'entrada_{v}')
        for i, j, c in arcos:
            if j == v:
                c_in.SetCoefficient(x[(i, j)], 1)
                
    for i, j, c in arcos:
        if i != 1 and j != 1:
            c_mtz = solver.Constraint(-infinity, num_vertices - 1, f'mtz_{i}_{j}')
            c_mtz.SetCoefficient(u[i], 1)
            c_mtz.SetCoefficient(u[j], -1)
            c_mtz.SetCoefficient(x[(i, j)], num_vertices)
            
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        rota = []
        proximo = {}
        for i, j, c in arcos:
            if x[(i, j)].solution_value() > 0.5:
                proximo[i] = j
        atual = 1
        for _ in range(num_vertices):
            rota.append(atual)
            atual = proximo[atual]
            if atual not in proximo:
                break
        rota.append(1)
        
        # Calculate real total cost and number of expensive arcs (>15)
        total_cost = 0
        expensive_count = 0
        used_arcs = []
        for i, j, c in arcos:
            if x[(i, j)].solution_value() > 0.5:
                total_cost += c
                used_arcs.append((i, j, c))
                if c > 15:
                    expensive_count += 1
                    
        print(f"Rota: {' -> '.join(map(str, rota))}")
        print(f"Custo total real: {total_cost}")
        print(f"Número de arcos >15: {expensive_count}")
        print("Arcos utilizados:", used_arcs)
    else:
        print("Infeasible")

print("--- VERSÃO DO USUÁRIO (coeficiente = c se c > 15) ---")
solve_with_objective(lambda c: c if c > 15 else 0)

print("\n--- VERSÃO CORRETA (coeficiente = 1 se c > 15) ---")
solve_with_objective(lambda c: 1 if c > 15 else 0)
