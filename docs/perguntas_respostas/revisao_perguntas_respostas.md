# Caderno de Revisão — Otimização e Defesa do Caixeiro Viajante (MTZ)

Este documento reúne todas as perguntas conceituais e práticas estudadas para a defesa do projeto do Caixeiro Viajante (MTZ). Ele contém as explicações matemáticas e os ajustes de código ideais para a sabatina em laboratório.

---

## 💻 1. Questões Práticas de Código (Modificações de 10 Minutos)

### Q1. Adicionar uma nova restrição para achar outra solução ótima (Nova Rota)
> **Pergunta:** *"A rota atual é ótima, mas eu quero ver outra. Como você adiciona uma restrição para forçar o modelo a achar um novo caminho (segunda melhor ou outra ótima se houver)?"*

* **Explicação Teórica:** Proibimos a rota atual limitando a soma de suas variáveis ativas (arcos que valem 1) a no máximo $n - 1$. Isso impede que o solver repita o mesmo ciclo completo.
* **Solução via Código (Corrigindo o bug de cache do OR-Tools):**
  ```python
  # 1. Armazena as variáveis ativas antes de alterar o modelo
  arcos_ativos = []
  for (i, j), var in x.items():
      if var.solution_value() > 0.5:
          arcos_ativos.append(var)

  # 2. Cria a restrição de corte e adiciona os coeficientes
  c = solver.Constraint(-infinity, num_vertices - 1)
  for var in arcos_ativos:
      c.SetCoefficient(var, 1)
  ```
* **Solução Hardcoded Rápida (Sem loops):**
  ```python
  c = solver.Constraint(-infinity, num_vertices - 1)
  c.SetCoefficient(x[(1, 3)], 1)
  c.SetCoefficient(x[(3, 5)], 1)
  c.SetCoefficient(x[(5, 4)], 1)
  c.SetCoefficient(x[(4, 2)], 1)
  c.SetCoefficient(x[(2, 1)], 1)
  ```

---

### Q2. Forçar ou Proibir um Arco Específico
> **Pergunta:** *"Modifique o código para que o caixeiro passe obrigatoriamente de 2 diretamente para 3 (ou proíba que ele faça esse trajeto)."*

* **Explicação Teórica:** Fixamos os limites (*bounds*) da própria variável binária para forçar (igual a 1) ou proibir (igual a 0).
* **Ajuste Mínimo (1 linha no Jupyter):**
  * **Para Forçar o arco 2 -> 3:**
    ```python
    x[(2, 3)].SetBounds(1, 1)
    ```
  * **Para Proibir o arco 2 -> 3:**
    ```python
    x[(2, 3)].SetBounds(0, 0)
    ```

---

### Q3. Mudar a Função Objetivo para minimizar o número de "arcos caros"
> **Pergunta:** *"Mude a função objetivo para minimizar o número de voos/arcos cuja tarifa (custo) seja estritamente maior que 15, em vez de minimizar o custo total."*

* **Explicação Teórica:** Em vez de multiplicar a variável $x_{ij}$ pelo seu custo, multiplicamos por 1 (se o custo for $>15$) ou por 0 (se for $\leq 15$). Assim, o solver minimiza a quantidade de arcos caros na rota completa.
* **Ajuste de Código:**
  ```python
  objetivo = solver.Objective()
  for a in arcos:
      i, j, c = a[0], a[1], a[2]
      if c > 15:
          objetivo.SetCoefficient(x[(i, j)], 1)
      else:
          objetivo.SetCoefficient(x[(i, j)], 0)
  objetivo.SetMinimization()
  ```

---

### Q4. Desativar a volta à origem (Transformar em Caminho Hamiltoniano)
> **Pergunta:** *"Como você alteraria o código para que o caixeiro não precise voltar ao ponto de partida? Ou seja, ele começa no 1 e termina em qualquer outra cidade."*

* **Explicação Teórica:** Mantemos as restrições MTZ para evitar loops e alteramos as restrições de grau. O início (1) não pode receber arcos (entrada = 0). As outras cidades podem ter 0 ou 1 saída (saída $\leq 1$).
* **Ajuste de Código (inserir antes de rodar o solver):**
  ```python
  # Origem 1 não tem arco de entrada
  for c in solver.constraints():
      if c.name() == 'entrada_1':
          c.SetBounds(0, 0)

  # Outros nós podem terminar a rota (saída <= 1)
  for v in vertices:
      if v != 1:
          for c in solver.constraints():
              if c.name() == f'saida_{v}':
                  c.SetBounds(0, 1)
  ```

---

## 🧠 2. Questões Conceituais de Otimização e Formulação

### Q5. Por que mudar a restrição de demanda de `">="` para `"="` no problema de Corte de Bobinas gera inviabilidade?
* **Explicação:** Porque o problema de corte exige padrões inteiros de corte. Ao exigir a igualdade exata ($=$), você proíbe qualquer tipo de excedente (*surplus*). Se a combinação inteira de padrões inevitavelmente produzir itens a mais para atender a demanda, a restrição $=$ se tornará matematicamente inviável.

---

### Q6. Por que as restrições MTZ de eliminação de subciclo são indexadas apenas para $i, j \neq 1$? O que acontece se incluirmos a origem (vértice 1)?
* **Explicação:** A restrição MTZ força uma ordem de visitação crescente ao longo do caminho ($u_j \geq u_i + 1$). Como a origem 1 é o início da rota ($u_1 = 1$), se aplicássemos a restrição ao arco de retorno final ($k \to 1$), ela exigiria que $u_1 \geq u_k + 1 \implies 1 \geq u_k + 1 \implies u_k \leq 0$. Isso é impossível, pois $u_k$ deve ser pelo menos 2. Portanto, incluir o vértice 1 inviabilizaria o retorno à origem.

---

### Q7. Por que a remoção das restrições MTZ resulta em subciclos (rotas desconexas)?
* **Explicação:** Sem o MTZ, restam apenas as restrições de grau (1 entrada e 1 saída por nó). Subciclos desconexos (ex: `1 -> 2 -> 4 -> 1` e `3 -> 5 -> 3`) satisfazem individualmente essa regra e, como o solver busca minimizar custos, ele escolherá esses caminhos curtos e desconexos se eles somarem um custo total menor.

---

### Q8. Quantidade de soluções viáveis/ótimas no TSP Simétrico vs. Assimétrico
* **Explicação:** 
  * **Assimétrico:** O custo de ida e volta é diferente. Existem **(n - 1)!** soluções.
  * **Simétrico:** O custo de ida e volta é igual (sentido horário e anti-horário têm o mesmo custo). Dividimos o total por 2, restando **(n - 1)! / 2** soluções distintas.

---

## 📊 3. Análise de Variáveis e Comportamento do Solver

### Q9. Como exibir os valores de TODAS as variáveis do solver (mesmo as que são 0)?
* **Ajuste de Código:**
  ```python
  for i, j in x:
      print(f"x[{i},{j}] = {x[(i, j)].solution_value()}")
  for w in u:
      print(f"u[{w}] = {u[w].solution_value()}")
  ```

---

### Q10. O que representam matematicamente as variáveis $u_i$ na solução ótima?
* **Explicação:** Representam a ordem sequencial em que as cidades são visitadas a partir da origem (cidade 1, que é a posição 1).
* **Exemplo:** Se $u_3 = 2$, a cidade 3 é a segunda a ser visitada. Se $u_2 = 5$ (em um grafo de 5 cidades), a cidade 2 é a quinta e última a ser visitada antes de retornar para a cidade 1.

---

## 💬 4. Perguntas Individuais / Corpo a Corpo

### Q11. "Como os dados são gerados e lidos aqui?"
* **Resposta:** Lemos dois arquivos CSV (`dados-gerais.csv` e `dados-arcos.csv`) usando a biblioteca **Pandas**. Em seguida, utilizamos o método **`itertuples()`** para varrer o DataFrame e criar as variáveis de decisão $x_{ij}$ apenas para os arcos válidos.

---

### Q12. "Como está configurado o solver de vocês? Qual biblioteca e algoritmo?"
* **Resposta:** Utilizamos a biblioteca **Google OR-Tools** (módulo `pywraplp`) configurando o solver open-source **SCIP**. Ele resolve o problema usando o algoritmo **Branch-and-Cut** (combinação de Branch-and-Bound com Planos de Corte).

---

### Q13. "O que acontece se o grafo de entrada não for completo?"
* **Resposta:** O código funciona normalmente, gerando variáveis apenas para os arcos descritos no CSV. Se ainda restar pelo menos um Ciclo Hamiltoniano viável no grafo esparso, o solver encontrará a rota ótima. Caso contrário, ele retornará o status de **Inviável (Infeasible)**.
