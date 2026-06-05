# Guia de Perguntas e Respostas — Defesa do Caixeiro Viajante (MTZ)

Este documento foi preparado para auxiliar a equipe (**Nelson, Luiz Carlos e Isaias**) na apresentação e sabatina do projeto de Caixeiro Viajante com Formulação Miller-Tucker-Zemlin (MTZ), utilizando o OR-Tools e Pandas.

Com base na metodologia do professor (sprints de 10 minutos para alterar código ou responder a perguntas conceituais no laboratório), este guia está dividido em 4 categorias de possíveis perguntas.

---

## 🧭 Sumário
1. [Dinâmica da Apresentação e Dicas Gerais](#-dinâmica-da-apresentação-e-dicas-gerais)
2. [Questões Práticas de Código (Modificações de 10 Minutos)](#-questões-práticas-de-código-modificações-de-10-minutos)
3. [Questões Conceituais de Otimização e Formulação](#-questões-conceituais-de-otimização-e-formulação)
4. [Análise de Variáveis e Comportamento do Solver](#-análise-de-variáveis-e-comportamento-do-solver)
5. [Perguntas Individuais / Corpo a Corpo](#-perguntas-individuais--corpo-a-corpo)

---

## 👥 Dinâmica da Apresentação e Dicas Gerais

* **Formato Squads:** A turma fica separada por equipes no laboratório.
* **Perguntas Coletivas (10 min):** O professor faz a pergunta em voz alta. Todas as equipes têm 10 minutos para resolver no notebook (ou papel) e o professor passa olhando os computadores de cada grupo.
* **Sabatina Suave:** Após as rodadas de perguntas gerais, o professor passa de grupo em grupo avaliando o código original e fazendo perguntas diretas sobre a implementação e resultados.
* **Regra de Ouro:** Nas alterações de código, o solver deve exibir os valores de todas as variáveis relevantes e a nova rota/custo obtidos.

---

## 💻 Questões Práticas de Código (Modificações de 10 Minutos)

Aqui estão os trechos exatos de código que vocês podem inserir no Jupyter Notebook caso o professor peça modificações em tempo real.

### Q1. Adicionar uma nova restrição para achar outra solução ótima (Nova Rota)
> **Pergunta:** *"A rota atual é ótima, mas eu quero ver outra. Como você adiciona uma restrição para forçar o modelo a achar um novo caminho (segunda melhor ou outra ótima se houver)?"*

* **Explicação Teórica:** Para proibir que a rota atual (composta pelos arcos ativos $x_{ij} = 1$) seja selecionada novamente, adicionamos uma restrição de **corte de rota** que impede que todos esses arcos sejam escolhidos simultaneamente. Se a rota original tem $n$ arcos, a soma deles na nova solução deve ser no máximo $n-1$.
* **Código Simplificado (5 linhas com print):**
  Crie uma célula temporária, insira o código abaixo, execute-a e depois **reexecute a célula de resolução original**:
  ```python
  c = solver.Constraint(-infinity, num_vertices - 1)
  for (i, j), var in x.items():
      if var.solution_value() > 0.5:
          print(f"Adicionando x[{i},{j}] ao corte")
          c.SetCoefficient(var, 1)
  ```
  *Depois, basta reexecutar a célula original do passo **6. Resolução e solução ótima**.*

---

### Q2. Forçar ou Proibir um Arco Específico
> **Pergunta:** *"Modifique o código para que o caixeiro passe obrigatoriamente de 2 diretamente para 3 (ou proíba que ele faça esse trajeto)."*

* **Explicação Teórica:** Para forçar ou proibir o uso de um arco $x_{ij}$, alteramos os limites (*bounds*) da respectiva variável binária para $[1,1]$ (forçar) ou $[0,0]$ (proibir).
* **Ajuste Mínimo (1 linha no Jupyter):**
  * **Para Forçar o arco 2 $\to$ 3:**
    ```python
    x[(2, 3)].SetBounds(1, 1)
    ```
  * **Para Proibir o arco 2 $\to$ 3:**
    ```python
    x[(2, 3)].SetBounds(0, 0)
    ```
  *Depois, basta **reexecutar a célula original de resolução** (passo 6).*

---

### Q3. Mudar a Função Objetivo para minimizar o número de "arcos caros"
> **Pergunta:** *"Mude a função objetivo para minimizar o número de voos/arcos cuja tarifa (custo) seja estritamente maior que 15, em vez de minimizar o custo total."*

* **Explicação Teórica:** Em vez de multiplicar cada variável $x_{ij}$ pelo seu custo real $c_{ij}$, alteramos os coeficientes do objetivo existente para $1$ nos arcos cujo custo seja $> 15$, e para $0$ nos demais.
* **Ajuste Mínimo (4 linhas no Jupyter):**
  Crie uma nova célula, digite o código abaixo, execute-a e depois **reexecute a célula original de resolução**:
  ```python
  for a in arcos:
      i, j, c = a[0], a[1], a[2]
      objetivo.SetCoefficient(x[(i, j)], 1 if c > 15 else 0)
  ```

---

### Q4. Desativar a volta à origem (Transformar em Caminho Hamiltoniano)
> **Pergunta:** *"Como você alteraria o código para que o caixeiro não precise voltar ao ponto de partida? Ou seja, ele começa no 1 e termina em qualquer outra cidade."*

* **Explicação Teórica:** No Caixeiro Viajante clássico (Ciclo), cada nó possui exatamente 1 arco de entrada e 1 de saída. Se queremos um caminho aberto que inicia em 1 e termina em qualquer outra cidade:
  1. A cidade de origem (1) terá **0** arcos de entrada: $\sum_{i} x_{i1} = 0$.
  2. A cidade final (destino) terá **0** arcos de saída: $\sum_{j} x_{\text{destino}, j} = 0$.
  3. Afrouxamos a restrição de saída para todas as outras cidades de "=" (exatamente 1) para "<=" (0 ou 1, pois a última cidade terá 0 saídas). E zeramos a entrada do nó 1.
* **Ajuste Mínimo (no Jupyter):**
  Crie uma nova célula, execute o código abaixo e **reexecute a célula original de resolução**:
  ```python
  # Origem 1 não pode ter arco de entrada (caminho começa lá)
  for c in solver.constraints():
      if c.name() == 'entrada_1':
          c.SetBounds(0, 0)
  
  # Outros vértices podem ter 0 ou 1 saída (o destino final terá 0)
  for v in vertices:
      if v != 1:
          for c in solver.constraints():
              if c.name() == f'saida_{v}':
                  c.SetBounds(0, 1)
  ```
  > [!WARNING]
  > **Nota de Atenção:** Como o caminho não retorna ao ponto de partida, a lógica de reconstrução da rota na célula de resolução dará um erro `KeyError` no final (pois a última cidade não tem saída cadastrada no dicionário `proximo`). Isso é perfeitamente normal! A lista de arcos utilizados impressa antes do erro ainda representará o caminho correto.


---

## 🧠 Questões Conceituais de Otimização e Formulação

Essas perguntas exigem anotações ou respostas conceituais imediatas.

### Q5. Por que mudar a restrição de demanda de `">="` para `"="` no problema de Corte de Bobinas (ou outros) gera inviabilidade?
> **Pergunta do Professor (Histórico):** *"Por que ao mudar a restrição de demanda de '>= D' para '= D' o modelo apresentou que não há solução viável?"*

* **Resposta Padrão:** O problema de corte trabalha com combinações de padrões inteiros. Ao exigir a igualdade exata ($=$), impedimos que haja qualquer sobra (*surplus*) de itens. 
* **Exemplo prático:** Se a demanda exige 3 bobinas de 40cm, e cada rolo padrão tem 100cm, podemos cortar no máximo 2 bobinas de 40cm por rolo (gerando 20cm de sobra).
  - Usar 1 rolo fornece 2 bobinas (insuficiente).
  - Usar 2 rolos fornece 4 bobinas.
  - Se a restrição for $\geq 3$, a solução é viável (usamos 2 rolos, entregamos 4 e sobramos 1).
  - Se a restrição for $= 3$, a solução torna-se **inviável**, pois não há combinação inteira de rolos que produza *exatamente* 3 bobinas sem gerar excedente.

---

### Q6. Por que as restrições MTZ de eliminação de subciclo são indexadas apenas para $i, j \neq 1$? O que acontece se incluirmos a origem (vértice 1)?
> **Pergunta:** *"Por que a eliminação de subciclos u_i - u_j + n * x_ij <= n - 1 não se aplica ao vértice 1?"*

* **Resposta Padrão:** Porque se aplicarmos a restrição ao vértice 1, o modelo se torna **inviável**, pois o ciclo completo obrigatoriamente contém o vértice 1 como início e fim.
* **Demonstração Matemática:**
  Suponha que temos o ciclo completo de 5 vértices: $1 \to 3 \to 5 \to 4 \to 2 \to 1$. 
  Se a restrição valesse para o vértice 1, o arco final $2 \to 1$ ($x_{21} = 1$) exigiria:
  $$u_2 - u_1 + 5 \cdot x_{21} \leq 4 \implies u_2 - u_1 + 5 \leq 4 \implies u_1 \geq u_2 + 1$$
  Por outro lado, o caminho da origem até o vértice 2 é $1 \to 3 \to 5 \to 4 \to 2$. Como todos esses arcos estão ativos, as restrições MTZ nos obrigam a ter:
  $$u_1 < u_3 < u_5 < u_4 < u_2 \implies u_2 > u_1$$
  Temos uma contradição direta: $u_1 \geq u_2 + 1$ e $u_2 > u_1$. O solver nunca conseguiria fechar a rota voltando ao vértice 1. Por isso, o nó de partida **deve** ser excluído das variáveis $u$ e das restrições de subciclo.

---

### Q7. Por que a remoção das restrições MTZ resulta em subciclos (rotas desconexas)?
> **Pergunta:** *"Se eu apagar as restrições MTZ do código, por que o solver retorna rotas que não cobrem todas as cidades de uma vez?"*

* **Resposta Padrão:** Sem o MTZ, o modelo possui apenas as **restrições de designação/grau** (cada cidade tem exatamente 1 arco entrando e 1 saindo). O solver, para minimizar custos, pode escolher conjuntos de ciclos independentes e desconexos (ex: $1 \to 2 \to 1$ e $3 \to 4 \to 5 \to 3$). Ambos os subciclos satisfazem a regra de "1 entrada e 1 saída" para cada nó individualmente, mas a rota geral não é conectada. O MTZ insere a noção de "tempo de visita" ($u_i$), que exige uma ordem sequencial crescente ao longo dos arcos, quebrando a possibilidade de subciclos isolados.

---

### Q8. Quantidade de soluções viáveis/ótimas no TSP Simétrico vs. Assimétrico
> **Pergunta:** *"Quantos caminhos hamiltonianos possíveis existem no problema do caixeiro viajante se o grafo for simétrico? E se for assimétrico? E qual a diferença?"*

* **Resposta Padrão:**
  - **Grafo Assimétrico (Direcionado):** O custo de ir de $i \to j$ é diferente de $j \to i$ ($c_{ij} \neq c_{ji}$). O número total de soluções viáveis (rotas possíveis) é:
    $$(n - 1)!$$
    *(Para 5 cidades: $(5-1)! = 4! = 24$ rotas).*
  - **Grafo Simétrico (Não direcionado):** O custo de ida e volta é o mesmo ($c_{ij} = c_{ji}$). Cada rota pode ser percorrida em dois sentidos com o mesmo custo (ex: $1 \to 2 \to 3 \to 1$ tem o mesmo custo de $1 \to 3 \to 2 \to 1$). Logo, o número de soluções únicas em termos de custo é reduzido pela metade:
    $$\frac{(n - 1)!}{2}$$
    *(Para 5 cidades: $\frac{24}{2} = 12$ rotas).*

---

## 📊 Análise de Variáveis e Comportamento do Solver

### Q9. Como exibir os valores de TODAS as variáveis do solver (mesmo as que são 0)?
> **Pergunta do Professor (Histórico):** *"O solver tem que apresentar os valores de cada variável, não só da ótima."*

* **Resposta/Código:** No final do notebook, adicione uma célula simples para iterar por todas as variáveis criadas no modelo e exibir seus respectivos valores:
```python
print("--- VALORES DE TODAS AS VARIÁVEIS DECISÃO x[i,j] ---")
for a in arcos:
    i, j = a[0], a[1]
    val = x[(i, j)].solution_value()
    print(f"x[{i},{j}] = {val}  (Ativo? {'SIM' if val > 0.5 else 'NÃO'})")

print("\n--- VALORES DAS VARIÁVEIS DE ORDEM u[i] ---")
print("u[1] = 1 (Origem fixa)")
for i in vertices:
    if i != 1:
        print(f"u[{i}] = {u[i].solution_value()}")
```

---

### Q10. O que representam matematicamente as variáveis $u_i$ na solução ótima?
> **Pergunta:** *"O que significa u[3] = 2 e u[2] = 5 no resultado impresso pelo notebook?"*

* **Resposta Padrão:** As variáveis $u_i$ representam a **ordem de visita seqüencial** da cidade $i$ na rota, assumindo a origem (cidade 1) na posição 1. 
  - Se $u[3] = 2$, significa que a cidade 3 é a **segunda** cidade visitada na rota total.
  - Se $u[2] = 5$, significa que a cidade 2 é a **quinta** cidade visitada na rota total.
  - Se a rota ótima é $1 \to 3 \to 5 \to 4 \to 2 \to 1$, a ordem de visita é:
    1. Cidade 1 (Origem, $u_1 = 1$)
    2. Cidade 3 ($u_3 = 2$)
    3. Cidade 5 ($u_5 = 3$)
    4. Cidade 4 ($u_4 = 4$)
    5. Cidade 2 ($u_2 = 5$)
    O solver ajusta esses valores inteiros respeitando os limites $2 \leq u_i \leq n$.

---

## 💬 Perguntas Individuais / Corpo a Corpo

O que responder na hora que o professor passar na mesa conversando suavemente.

### Q11. "Como os dados são gerados e lidos aqui?"
* **Resposta:** *"Professor, nós lemos os dados de dois arquivos CSV utilizando o Pandas. O arquivo `dados-gerais.csv` nos dá a quantidade total de vértices ($n = 5$). O arquivo `dados-arcos.csv` possui a estrutura clássica de representação de grafos: colunas de origem, destino e custo. Com isso, montamos dinamicamente as variáveis de decisão binárias $x_{ij}$ apenas para os arcos que existem no arquivo."*

### Q12. "Como está configurado o solver de vocês? Qual biblioteca e algoritmo?"
* **Resposta:** *"Estamos utilizando o módulo `pywraplp` do OR-Tools do Google. Instanciamos o solver informando a string `'SCIP'`. O SCIP é um dos solvers de código aberto mais rápidos para Programação Linear Inteira Mista (MILP). Ele resolve o problema usando técnicas de Branch-and-Bound acopladas com planos de corte."*

### Q13. "O que acontece se o grafo de entrada não for completo?"
* **Resposta:** *"O modelo MTZ assume que o grafo é completo. Se faltarem arcos no arquivo `dados-arcos.csv`, nosso script criará apenas as variáveis $x_{ij}$ correspondentes aos arcos presentes. Caso não existam caminhos ligando todos os nós em um ciclo único viável, o solver retornará que o problema é inviável (`pywraplp.Solver.INFEASIBLE`)."*
