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

### Q13. "O que acontece se o grafo de entrada não for completo?"
* **Resposta:** *"O modelo MTZ assume que o grafo é completo. Se faltarem arcos no arquivo `dados-arcos.csv`, nosso script criará apenas as variáveis $x_{ij}$ correspondentes aos arcos presentes. Caso não existam caminhos ligando todos os nós em um ciclo único viável, o solver retornará que o problema é inviável (`pywraplp.Solver.INFEASIBLE`)."*

---

## 📝 5. Análise Comparativa com as Questões da Prova Real (Relato de Colega)

Esta seção analisa as questões aplicadas na prova do colega do dia 08/06/2026, comparando-as com o nosso material de revisão e fornecendo as soluções teóricas e práticas (código).

### Questão da Prova 1: Rodar o notebook com uma nova planilha de dados e relatar a rota ótima
* **Nível de Dificuldade:** Baixo.
* **Comparação com nossa revisão:** É o comportamento padrão do notebook. Como o nosso notebook foi parametrizado com a variável global `cidade_origem` (Célula 5), qualquer alteração na origem ou nos dados pode ser simulada instantaneamente bastando alterar essa variável e reexecutar a resolução.
* **O que fazer na hora:** Salve a planilha fornecida na pasta `dados/` ou ajuste a célula de leitura de CSV para apontar para o novo arquivo (ex: `pd.read_csv('dados/dados-novos.csv')`).

---

### Questão da Prova 2: Restrição de Precedência (Visitar o vértice 2 antes do vértice 10)
* **Nível de Dificuldade:** Médio.
* **Comparação com nossa revisão:** É **idêntica** à **Q14** de nossa revisão (onde propusemos visitar a cidade 4 antes da 2). O nível de complexidade matemática e de código é exatamente o mesmo.
* **A) Equação Matemática da Restrição:**
  Como a variável $u_i$ representa a ordem de visitação do nó $i$, se o vértice 2 deve ser visitado antes do 10, a ordem de visita de 2 deve ser menor do que a de 10:
  $$u_2 < u_{10} \quad \text{ou, em formato linear/inteiro,} \quad u_2 \leq u_{10} - 1$$
* **B) Implementação no OR-Tools (Código):**
  Insira na célula de montagem de restrições (ou antes do `Solve`):
  ```python
  solver.Add(u[2] <= u[10] - 1)
  ```

---

### Questão da Prova 3: Ativação Condicional de Arcos (Se o arco $(i,j)$ for visitado, então o arco $(k,l)$ também deve ser visitado)
* **Nível de Dificuldade:** Alto (Exige modelagem de lógica condicional).
* **Comparação com nossa revisão:** **Nova Questão!** Não constava originalmente no nosso caderno de revisão e eleva consideravelmente o nível da nossa preparação.
* **A) Equação Matemática da Restrição:**
  Dado que as variáveis de decisão $x_{ij}$ e $x_{kl}$ são binárias ($0$ ou $1$), a implicação lógica $x_{ij} \implies x_{kl}$ (se $x_{ij} = 1$, então $x_{kl} = 1$) é expressa algebricamente por:
  $$x_{ij} \leq x_{kl}$$
  * Se $x_{ij} = 1$, força $1 \leq x_{kl} \implies x_{kl} = 1$.
  * Se $x_{ij} = 0$, a restrição fica $0 \leq x_{kl}$, que é sempre satisfeita para variáveis binárias, permitindo que $x_{kl}$ seja $0$ ou $1$.
* **B) Implementação no OR-Tools (Código):**
  Suponha que, se percorrermos o arco $2 \to 3$, devemos obrigatoriamente percorrer o arco $4 \to 5$:
  ```python
  solver.Add(x[(2, 3)] <= x[(4, 5)])
  ```

---

### Questão da Prova 4: Incompatibilidade de Dados na Segunda Entrada (Inviabilidade do Solver)
* **Nível de Dificuldade:** Alto (Diagnóstico e Depuração).
* **Comparação com nossa revisão:** **Nova Questão!** Aborda uma situação prática onde o notebook original falha em virtude de dados de teste inconsistentes.
* **Causa do Problema:**
  Se o arquivo geral aponta `num_vertices = 10` e criamos vértices de $1$ a $10$, mas o arquivo de arcos contém apenas conexões para cidades de $1$ a $5$ (sem menção de $6$ a $10$), a restrição de grau de saída criada para $v \geq 6$:
  ```python
  for v in vertices:
      restricao = solver.Constraint(1, 1, f'saida_{v}')
      # ... tenta associar variáveis x[(v, j)] que não existem no CSV ...
  ```
  Resulta em uma restrição vazia: $0 = 1$. Por ser impossível satisfazer $0 = 1$, o solver SCIP declara imediatamente que o modelo é **Inviável (INFEASIBLE)**.
* **Como Prevenir/Ajustar no Código:**
  Em vez de usar o número estático `num_vertices` do arquivo geral, crie a lista de vértices dinamicamente a partir dos nós reais presentes no CSV de arcos:
  ```python
  # Extrair lista dinâmica de vértices reais
  vertices_reais = sorted(list(set(df_dados_arcos['origem'].unique()).union(set(df_dados_arcos['destino'].unique()))))
  num_vertices = len(vertices_reais)
  ```
  Dessa forma, o código se adapta aos nós que de fato existem nos dados dos arcos, evitando criar equações vazias do tipo $0=1$.
