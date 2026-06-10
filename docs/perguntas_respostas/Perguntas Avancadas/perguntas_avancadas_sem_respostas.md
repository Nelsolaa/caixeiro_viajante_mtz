# Guia de Questões Avançadas — Caixeiro Viajante (MTZ)

Este documento contém perguntas de nível avançado sobre a formulação Miller-Tucker-Zemlin (MTZ), relaxação linear, sensibilidade de limites e o comportamento do algoritmo Branch-and-Bound. Utilize estas questões para aprofundar seu domínio sobre o tema e preparar-se para sabatinas complexas da banca de Modelagem em Programação Matemática.

---

## 🧭 Sumário
1. [Questões Práticas de Modificação de Código (Desafios MTZ)](#-questões-práticas-de-modificação-de-código-desafios-mtz)
2. [Questões Teóricas de Otimização e Comportamento do Solver](#-questões-teóricas-de-otimização-e-comportamento-do-solver)

---

## 💻 Questões Práticas de Modificação de Código (Desafios MTZ)

### Q14. Código Prático: Restrição de Precedência de Visitação
> **Pergunta:** *"Suponha que, por exigências operacionais, o caixeiro viaje de tal forma que ele precise visitar a cidade 4 obrigatoriamente ANTES da cidade 2 na rota final (não necessariamente de forma consecutiva). Como adicionar essa restrição no modelo MTZ usando as variáveis u e como ficaria a linha de código correspondente no OR-Tools?"*

---

### Q15. Código Prático: Sensibilidade nos Limites das Variáveis u_i
> **Pergunta:** *"O que acontece se alterarmos os limites da variável de ordem u_i no código de 'u_i = solver.IntVar(2, num_vertices, ...)' para 'u_i = solver.IntVar(3, num_vertices, ...)'? O modelo continuará viável e correto para encontrar o ciclo Hamiltoniano? Demonstre como alterar os limites de bounds no código."*

---

### Q16. Código Prático: Fixar a Posição de Visita de uma Cidade Específica
> **Pergunta:** *"Imagine que a cidade 3 seja um centro de distribuição que precisa ser visitado exatamente na terceira posição da rota geral (lembrando que a cidade de origem 1 é a posição 1). Como você modificaria as variáveis u no código do OR-Tools para forçar essa ordem de visitação exata?"*

---

## 🧠 Questões Teóricas de Otimização e Comportamento do Solver

### Q17. Mecânica Algébrica de Corte de Subciclos pelo Branch-and-Bound
> **Pergunta:** *"Como a restrição MTZ dada por 'u_i - u_j + n * x_ij <= n - 1' atua algebricamente para impedir que o solver adote um subciclo de tamanho 3 (por exemplo, a rota isolada 2 -> 3 -> 4 -> 2) quando as variáveis de decisão x_23, x_34 e x_42 assumem valor 1? Demonstre a soma das equações e a contradição gerada."*

---

### Q18. MTZ aplicado a Grafos Simétricos
> **Pergunta:** *"Se o grafo de entrada for simétrico (custo de ida i -> j é igual ao de volta j -> i), a formulação clássica do MTZ ainda é suficiente para impedir que o solver retorne um subciclo de tamanho 2 (ida e volta isolada, como 2 -> 3 -> 2)? Explique como a inequação se comporta nessa situação."*

---

### Q19. Relaxação Linear e Variáveis Fracionárias no MTZ
> **Pergunta:** *"Ao resolver a relaxação linear do MTZ (onde as variáveis x_ij deixam de ser binárias e passam a ser contínuas no intervalo [0, 1]), o solver SCIP frequentemente encontra soluções com valores fracionários (ex: x_ij = 0.5) que ainda assim satisfazem a desigualdade do MTZ. Por que a relaxação linear do MTZ é considerada 'frouxa' (weak) comparada a outras formulações?"*

---

### Q20. Código Prático: Ativação Condicional de Arcos
> **Pergunta:** *"Suponha que, devido a acordos de tráfego aéreo, se o caixeiro utilizar o trecho de ida da cidade 2 para a cidade 3, ele seja obrigado a utilizar o trecho da cidade 4 para a cidade 5 na mesma rota. Escreva a equação linear dessa restrição e como programá-la no OR-Tools."*

---

### Q21. Conceito Prático: Inconsistência nos Dados de Entrada (Inviabilidade 0 = 1)
> **Pergunta:** *"Suponha que o arquivo de dados gerais informe que existem 10 vértices, mas o arquivo de arcos forneça conexões apenas entre os vértices de 1 a 5. Por que o modelo original com restrição de grau rígido 'entrada_v' e 'saida_v' se tornará inviável? Como ajustar o código para evitar essa falha?"*

