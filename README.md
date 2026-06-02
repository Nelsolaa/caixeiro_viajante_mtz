# Problema do Caixeiro Viajante — Formulação MTZ (AV3)

Trabalho da disciplina **Modelagem em Programação Matemática** (Unifor).
Implementação de um modelo genérico de **Programação Linear Inteira** para o **Problema do Caixeiro Viajante (PCV/TSP)**, utilizando a formulação de **Miller-Tucker-Zemlin (MTZ)** com **OR-Tools** e **Pandas**.

## Equipe

| Integrante  | Matrícula   |
| ----------- | ----------- |
| Nelson      | _matrícula_ |
| Luiz Carlos | _matrícula_ |
| Isaias      | _matrícula_ |

## Sobre o problema

O Problema do Caixeiro Viajante consiste em determinar a **rota de menor custo** que permite a um viajante visitar um conjunto de cidades **exatamente uma vez** e **retornar à cidade de origem**.

Dado um dígrafo completo `D = (V, A)` com `|V| = n` cidades e custo `cᵢⱼ` em cada arco `(i, j)`, o objetivo é encontrar um **ciclo Hamiltoniano de custo mínimo**.

### Formulação MTZ

- **Variáveis:** `xᵢⱼ ∈ {0, 1}` (arco na rota) e `uᵢ ∈ ℤ` (ordem de visita, para eliminação de subciclos).
- **Objetivo:** `min Σ cᵢⱼ · xᵢⱼ`
- **Restrições de designação:** cada cidade tem exatamente 1 arco saindo e 1 entrando.
- **Eliminação de subciclos (MTZ):** `uᵢ - uⱼ + n · xᵢⱼ ≤ n - 1`, para `i, j ≠ 1`.

A formulação completa com LaTeX está documentada na primeira célula do notebook.

## Estrutura do projeto

```text
caixeiro_viajante_mtz/
├── README.md                       # este arquivo
├── .gitignore                      # ignorar arquivos desnecessários
├── caixeiro_viajante_mtz.ipynb     # implementação principal (entrega)
├── dados/
│   ├── dados-gerais.csv            # entrada: num_vertices
│   └── dados-arcos.csv             # entrada: origem, destino, custo
├── docs/
│   └── problema.md                 # enunciado do trabalho
└── referencia/
    ├── caminho_minimo.ipynb        # notebook de referência da aula do professor
    ├── dados-gerais.csv            # dados de referência da aula (caminho mínimo)
    └── dados-arcos.csv             # dados de referência da aula (caminho mínimo)
```

## Requisitos

- Python 3.8+
- Jupyter Notebook
- Bibliotecas: `ortools`, `pandas`

## Como executar

1. Certifique-se de que os arquivos de dados estão localizados na pasta `dados/` (`dados/dados-gerais.csv` e `dados/dados-arcos.csv`).
2. Abra o terminal no diretório do projeto e execute:

```bash
pip install jupyter ortools pandas
jupyter notebook caixeiro_viajante_mtz.ipynb
```

3. Execute as células em ordem (`Shift + Enter`).

## Formato da entrada

### dados-gerais.csv

Uma coluna com o número de vértices:

```csv
num_vertices
5
```

### dados-arcos.csv

Três colunas: origem, destino e custo. O grafo deve ser **completo** (um arco para cada par de vértices distintos):

```csv
origem,destino,custo
1,2,10
1,3,15
...
```

Para `n` vértices, o arquivo deve ter exatamente `n × (n - 1)` linhas de arcos.

## Exemplo de saída

Para o grafo de 5 cidades fornecido nos CSVs de exemplo:

- **Rota ótima:** `1 -> ... -> 1` (ciclo Hamiltoniano de custo mínimo)
- **Custo total:** valor ótimo
- **Modelo PLI** impresso em formato LP via `solver.ExportModelAsLpFormat(False)`
- **Ordem de visita** (variáveis `u`) para verificação da eliminação de subciclos

## Observações sobre a implementação

- Utiliza **exclusivamente** as bibliotecas OR-Tools (`pywraplp` + SCIP) e Pandas, conforme exigência do enunciado.
- Sintaxe alinhada com os exercícios da disciplina: `Solver.CreateSolver('SCIP')`, `BoolVar`, `IntVar`, `Objective` + `SetCoefficient` + `SetMinimization`, `Constraint` + `SetCoefficient`, `ExportModelAsLpFormat`.
- Para testar com dados diferentes, basta substituir os arquivos CSV e re-executar o notebook.
