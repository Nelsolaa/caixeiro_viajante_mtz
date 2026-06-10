# 📝 Caderno de Revisão Final — Questões de Itens (A e B) [COM GABARITO]

Este documento foi criado como guia de revisão final para a prova de Modelagem em Programação Matemática (Unifor). Ele contém todas as questões de modificação do Caixeiro Viajante (MTZ) estruturadas no modelo de dois itens cobrado pelo professor, incluindo as respostas completas.

Todas as expressões matemáticas estão formatadas em texto simples para garantir leitura limpa em qualquer dispositivo.

---

## 🧭 Sumário das Questões
1. [Questão 1: Encontrar Outra Rota Ótima (Corte de Rota)](#questão-1)
2. [Questão 2: Forçar ou Proibir um Arco Específico](#questão-2)
3. [Questão 3: Minimizar a Quantidade de Arcos Caros](#questão-3)
4. [Questão 4: Transformar em Caminho Aberto (Sem retornar ao início)](#questão-4)
5. [Questão 5: Precedência de Visitação (Visitar cidade i antes da cidade j)](#questão-5)
6. [Questão 6: Fixar uma Cidade em uma Posição Específica da Rota](#questão-6)
7. [Questão 7: Ativação Condicional de Arcos (Se passar por A, deve passar por B)](#questão-7)

---

## <a name="questão-1"></a> 1. Questão 1: Encontrar Outra Rota Ótima (Corte de Rota)
> **Problema:** *"Como forçar o modelo a encontrar uma nova rota (seja uma segunda melhor solução ou outra ótima de mesmo custo), proibindo a rota ótima que já foi encontrada?"*

* **Item A) Modelagem Matemática:**
  Para proibir a rota atual, somamos as variáveis dos arcos que estavam ativos na solução atual e limitamos essa soma a no máximo `n - 1` (onde `n` é o número de vértices). Isso impede que o solver reative todas as mesmas conexões ao mesmo tempo.
  
  Equação:
  `Soma(x_ij) <= n - 1`  (para todos os pares (i, j) onde x_ij = 1 na solução anterior)

* **Item B) Implementação no OR-Tools:**
  ```python
  # Cria a restrição de corte e define o limite superior como n - 1
  c = solver.Constraint(-infinity, num_vertices - 1)
  
  # Adiciona coeficiente 1 apenas para os arcos que estavam ativos (valor > 0.5)
  for (i, j), var in x.items():
      if var.solution_value() > 0.5:
          c.SetCoefficient(var, 1)
  ```

---

## <a name="questão-2"></a> 2. Questão 2: Forçar ou Proibir um Arco Específico
> **Problema:** *"Ajuste o modelo para que o caixeiro seja obrigado a viajar diretamente da cidade 2 para a cidade 3. Em seguida, mostre como proibir essa viagem direta."*

* **Item A) Modelagem Matemática:**
  Como a variável de decisão de arco é binária (0 ou 1), basta fixar o valor limite da variável.
  * Para forçar: `x_23 = 1`
  * Para proibir: `x_23 = 0`

* **Item B) Implementação no OR-Tools:**
  * Para Forçar (limites inferior e superior iguais a 1):
    ```python
    x[(2, 3)].SetBounds(1, 1)
    ```
  * Para Proibir (limites inferior e superior iguais a 0):
    ```python
    x[(2, 3)].SetBounds(0, 0)
    ```

---

## <a name="questão-3"></a> 3. Questão 3: Minimizar a Quantidade de Arcos Caros
> **Problema:** *"Altere o objetivo do modelo. Em vez de minimizar o custo financeiro total, minimize a quantidade de trechos viajados cujo custo seja estritamente maior que 15."*

* **Item A) Modelagem Matemática:**
  Redefinimos os coeficientes da função objetivo. Em vez de multiplicar cada arco `x_ij` por seu custo real `c_ij`, multiplicamos por um peso `d_ij` que vale `1` se `c_ij > 15`, e `0` caso contrário.
  
  Objetivo:
  `Minimizar Soma(d_ij * x_ij)`
  Onde:
  * `d_ij = 1` se `custo(i -> j) > 15`
  * `d_ij = 0` se `custo(i -> j) <= 15`

* **Item B) Implementação no OR-Tools:**
  ```python
  # Reinicia o objetivo
  objetivo = solver.Objective()
  
  # Aplica o coeficiente 1 para arcos caros (>15) e 0 para os demais
  for a in arcos:
      i, j, c = a[0], a[1], a[2]
      if c > 15:
          objetivo.SetCoefficient(x[(i, j)], 1)
      else:
          objetivo.SetCoefficient(x[(i, j)], 0)
          
  objetivo.SetMinimization()
  ```

---

## <a name="questão-4"></a> 4. Questão 4: Transformar em Caminho Aberto (Sem retornar ao início)
> **Problema:** *"Altere o modelo para que o caixeiro realize um caminho aberto que inicia na cidade 1 e termina em qualquer outra cidade, sem a necessidade de retornar à cidade 1."*

* **Item A) Modelagem Matemática:**
  Para manter o caminho aberto a partir da origem 1:
  1. O nó de origem 1 não pode receber nenhum arco de entrada:
     `Soma(x_i1) = 0` (para todo i)
  2. Qualquer outra cidade pode ter 0 ou 1 arco de saída (já que a cidade final do caminho terá 0 saídas):
     `Soma(x_vj) <= 1` (para todo nó v diferente de 1)

* **Item B) Implementação no OR-Tools:**
  ```python
  # 1. Zera a entrada na origem (entrada_1 = 0)
  for c in solver.constraints():
      if c.name() == 'entrada_1':
          c.SetBounds(0, 0)
          
  # 2. Afrouxa a saída dos demais nós para <= 1 (em vez de = 1)
  for v in vertices:
      if v != 1:
          for c in solver.constraints():
              if c.name() == f'saida_{v}':
                  c.SetBounds(0, 1)
  ```

---

## <a name="questão-5"></a> 5. Questão 5: Precedência de Visitação (Visitar cidade i antes da cidade j)
> **Problema:** *"O caixeiro precisa obrigatoriamente visitar a cidade 4 antes de visitar a cidade 2 na rota final (não necessariamente de forma consecutiva). Como modelar e programar essa restrição?"*

* **Item A) Modelagem Matemática:**
  A variável de ordem `u_i` representa numericamente a posição da cidade na rota. Para que 4 seja visitada antes de 2, a ordem de 4 deve ser estritamente menor que a de 2:
  `u_4 < u_2`
  Como as variáveis de ordem são estritamente inteiras, convertemos para desigualdade não-estrita para o solver:
  `u_4 <= u_2 - 1`  (ou  `u_4 - u_2 <= -1`)

* **Item B) Implementação no OR-Tools:**
  ```python
  # Adiciona a restrição de precedência de forma simplificada
  solver.Add(u[4] <= u[2] - 1)
  ```

---

## <a name="questão-6"></a> 6. Questão 6: Fixar uma Cidade em uma Posição Específica da Rota
> **Problema:** *"A cidade 3 deve ser visitada obrigatoriamente como a terceira cidade da rota (lembrando que a origem 1 ocupa a primeira posição). Como fixar essa posição?"*

* **Item A) Modelagem Matemática:**
  Como a origem ocupa a posição 1 (`u_1 = 1`), a terceira cidade da rota deve ter o valor de ordem igual a 3:
  `u_3 = 3` (ou equivalentemente: `3 <= u_3 <= 3`)

* **Item B) Implementação no OR-Tools:**
  * **Opção 1 (Via limites - mais eficiente para o solver):**
    ```python
    u[3].SetBounds(3, 3)
    ```
  * **Opção 2 (Via igualdade direta):**
    ```python
    solver.Add(u[3] == 3)
    ```

---

## <a name="questão-7"></a> 7. Questão 7: Ativação Condicional de Arcos (Se passar por A, deve passar por B)
> **Problema:** *"Se o caixeiro utilizar o arco 2 -> 3 (ir de 2 diretamente para 3), ele é obrigado a também utilizar o arco 4 -> 5 na mesma rota. Como modelar essa condicional?"*

* **Item A) Modelagem Matemática:**
  As variáveis dos arcos `x_23` e `x_45` são binárias (0 ou 1). A implicação lógica "se x_23 = 1 então x_45 = 1" é modelada limitando o termo independente pelo dependente:
  `x_23 <= x_45`  (ou  `x_23 - x_45 <= 0`)
  
  * Se `x_23 = 1` -> força `1 <= x_45` (logo `x_45 = 1`).
  * Se `x_23 = 0` -> a restrição vira `0 <= x_45`, deixando `x_45` livre para ser 0 ou 1.

* **Item B) Implementação no OR-Tools:**
  ```python
  # Adiciona a restrição condicional de ativação de arcos
  solver.Add(x[(2, 3)] <= x[(4, 5)])
  ```
