# Gabarito de Questões Avançadas — Caixeiro Viajante (MTZ)

Este documento contém as respostas detalhadas, demonstrações matemáticas e códigos de ajuste para o **Guia de Questões Avançadas** sobre a formulação Miller-Tucker-Zemlin (MTZ).

---

## 💻 1. Questões Práticas de Modificação de Código (Desafios MTZ)

### Q14. Código Prático: Restrição de Precedência de Visitação
> **Pergunta:** *"Suponha que, por exigências operacionais, o caixeiro viaje de tal forma que ele precise visitar a cidade 4 obrigatoriamente ANTES da cidade 2 na rota final (não necessariamente de forma consecutiva). Como adicionar essa restrição no modelo MTZ usando as variáveis u e como ficaria a linha de código correspondente no OR-Tools?"*

* **Explicação Teórica:**
  A variável `u[i]` representa a ordem numérica de visitação da cidade `i` (variando de 2 a n). Se a cidade 4 deve ser visitada antes da cidade 2, a ordem de visitação da cidade 4 deve ser estritamente menor que a da cidade 2. Portanto, a regra matemática é:
  
  **u[4] < u[2]** ou de forma inteira: **u[4] <= u[2] - 1**

* **Ajuste de Código (no OR-Tools):**
  Insira a seguinte linha de código na célula do Jupyter antes de rodar o solver:
  ```python
  # Restrição de Precedência: Cidade 4 deve ser visitada antes da Cidade 2
  solver.Add(u[4] <= u[2] - 1)
  ```
  *(Nota: O método `solver.Add` aceita expressões lógicas diretas. Ao rodar o Solve, o caixeiro buscará a melhor rota que satisfaça u[4] < u[2], por exemplo, a rota 1 -> 4 -> 3 -> 5 -> 2 -> 1, onde u[4]=2 e u[2]=5).*

---

### Q15. Código Prático: Sensibilidade nos Limites das Variáveis u_i
> **Pergunta:** *"O que acontece se alterarmos os limites da variável de ordem u_i no código de 'u_i = solver.IntVar(2, num_vertices, ...)' para 'u_i = solver.IntVar(3, num_vertices, ...)'? O modelo continuará viável e correto para encontrar o ciclo Hamiltoniano? Demonstre como alterar os limites de bounds no código."*

* **Explicação Teórica:**
  O modelo se tornará **inviável (Infeasible)**. 
  
  O vértice 1 (origem) ocupa a posição 1. Os outros `n - 1` nós devem obrigatoriamente preencher as posições de 2 a `n`. Se definirmos o limite inferior de todas as outras variáveis `u_i` como 3, nenhuma cidade poderá ocupar a posição 2 na rota. Como o caixeiro deve visitar as cidades em uma sequência contínua (posição 1 -> posição 2 -> posição 3...), e a posição 2 está proibida pelo limite, o solver não conseguirá fechar a rota e retornará que o problema não tem solução viável.

* **E se o limite superior fosse relaxado para u_i <= n + 5?**
  O modelo continuaria encontrando a solução ótima correta, mas a relaxação linear seria ainda mais fraca (frouxa), o que faria o algoritmo de **Branch-and-Bound** demorar mais nós para resolver o problema caso o grafo fosse grande.

* **Ajuste de Código (mostrando como os bounds são declarados):**
  ```python
  # O correto (2 <= u[i] <= n):
  u[i] = solver.IntVar(2, num_vertices, f'u{i}')

  # O teste incorreto que causa inviabilidade (3 <= u[i] <= n):
  u[i] = solver.IntVar(3, num_vertices, f'u{i}')
  ```

---

### Q16. Código Prático: Fixar a Posição de Visita de uma Cidade Específica
> **Pergunta:** *"Imagine que a cidade 3 seja um centro de distribuição que precisa ser visitado exatamente na terceira posição da rota geral (lembrando que a cidade de origem 1 é a posição 1). Como você modificaria as variáveis u no código do OR-Tools para forçar essa ordem de visitação exata?"*

* **Explicação Teórica:**
  Como a variável `u[3]` representa numericamente a ordem em que a cidade 3 é visitada na sequência da rota, e queremos que ela seja a terceira cidade visitada (origem é a primeira), devemos fixar o valor de `u[3]` em exatamente 3. No OR-Tools, a forma mais eficiente de fixar o valor de uma variável é definir seus limites inferior e superior (*bounds*) como iguais ao valor desejado: `3 <= u[3] <= 3`.

* **Ajuste de Código (no OR-Tools):**
  Insira a seguinte linha de código na célula do Jupyter antes de rodar o solver:
  ```python
  # Fixa a cidade 3 exatamente na terceira posição da rota
  u[3].SetBounds(3, 3)
  ```
  *(Nota: Isso reduz o espaço de busca do solver de forma muito eficiente, pois elimina qualquer ramo do Branch-and-Bound onde u_3 seja diferente de 3).*

---

## 🧠 2. Questões Teóricas de Otimização e Comportamento do Solver

### Q17. Mecânica Algébrica de Corte de Subciclos pelo Branch-and-Bound
> **Pergunta:** *"Como a restrição MTZ dada por 'u_i - u_j + n * x_ij <= n - 1' atua algebricamente para impedir que o solver adote um subciclo de tamanho 3 (por exemplo, a rota isolada 2 -> 3 -> 4 -> 2) quando as variáveis de decisão x_23, x_34 e x_42 assumem valor 1? Demonstre a soma das equações e a contradição gerada."*

* **Resposta Padrão:**
  Se o solver tentar ativar o subciclo `2 -> 3 -> 4 -> 2`, teremos `x_23 = 1`, `x_34 = 1` e `x_42 = 1`. 
  
  Substituindo esses valores nas respectivas restrições MTZ (para n=5):
  
  1. Para o arco 2 -> 3: 
     `u_2 - u_3 + 5 * (1) <= 4  =>  u_2 - u_3 <= -1`
  
  2. Para o arco 3 -> 4: 
     `u_3 - u_4 + 5 * (1) <= 4  =>  u_3 - u_4 <= -1`
  
  3. Para o arco 4 -> 2: 
     `u_4 - u_2 + 5 * (1) <= 4  =>  u_4 - u_2 <= -1`

  Somando os lados esquerdos e direitos destas três inequações:
  `(u_2 - u_3) + (u_3 - u_4) + (u_4 - u_2) <= -1 - 1 - 1`
  
  Cancelando os termos de `u`:
  `0 <= -3`

  **Contradição:** Chegamos à conclusão matemática de que `0 <= -3`, o que é impossível. Portanto, nenhuma atribuição de valores para as variáveis de ordem `u_2`, `u_3` e `u_4` pode satisfazer o modelo se esse subciclo for ativo. O algoritmo Branch-and-Bound detecta essa inconsistência linear e poda esse nó da árvore de busca.

---

### Q18. MTZ aplicado a Grafos Simétricos
> **Pergunta:** *"Se o grafo de entrada for simétrico (custo de ida i -> j é igual ao de volta j -> i), a formulação clássica do MTZ ainda é suficiente para impedir que o solver retorne um subciclo de tamanho 2 (ida e volta isolada, como 2 -> 3 -> 2)? Explique como a inequação se comporta nessa situação."*

* **Resposta Padrão:**
  Sim, o MTZ é suficiente para impedir subciclos de tamanho 2 (ida e volta entre duas cidades sem passar pelas demais).
  
  Se o caixeiro tentasse fazer o ciclo isolado `2 -> 3 -> 2`, as variáveis ativadas seriam `x_23 = 1` e `x_32 = 1`. 
  As restrições MTZ para esses dois arcos seriam:
  * Para 2 -> 3: `u_2 - u_3 + n * (1) <= n - 1  =>  u_2 - u_3 <= -1`
  * Para 3 -> 2: `u_3 - u_2 + n * (1) <= n - 1  =>  u_3 - u_2 <= -1`
  
  Somando as duas inequações:
  `(u_2 - u_3) + (u_3 - u_2) <= -1 - 1  =>  0 <= -2`
  
  Como `0 <= -2` é uma contradição matemática, o solver é impedido de formar esse ciclo curto divisor. O MTZ garante a eliminação de subciclos de qualquer tamanho (de 2 até n-1) tanto em grafos simétricos quanto assimétricos.

---

### Q19. Relaxação Linear e Variáveis Fracionárias no MTZ
> **Pergunta:** *"Ao resolver a relaxação linear do MTZ (onde as variáveis x_ij deixam de ser binárias e passam a ser contínuas no intervalo [0, 1]), o solver SCIP frequentemente encontra soluções com valores fracionários (ex: x_ij = 0.5) que ainda assim satisfazem a desigualdade do MTZ. Por que a relaxação linear do MTZ é considerada 'frouxa' (weak) comparada a outras formulações?"*

* **Resposta Padrão:**
  A relaxação é considerada fraca porque as variáveis de ordem `u_i` são muito permissivas quando `x_ij` assume valores fracionários.
  
  Considere o mesmo subciclo de tamanho 3 (`2 -> 3 -> 4 -> 2`) mas com valores fracionários `x_23 = x_34 = x_42 = 0.5` (o que é comum na relaxação linear). 
  Substituindo na inequação MTZ (com n=5):
  * Para 2 -> 3: `u_2 - u_3 + 5 * (0.5) <= 4  =>  u_2 - u_3 + 2.5 <= 4  =>  u_2 - u_3 <= 1.5`
  
  Somando as três equações com valor 0.5:
  `(u_2 - u_3) + (u_3 - u_4) + (u_4 - u_2) <= 1.5 + 1.5 + 1.5  =>  0 <= 4.5`

  **O problema:** A inequação `0 <= 4.5` é matematicamente **verdadeira**. 
  
  Isso significa que, se as variáveis forem fracionárias, o solver consegue facilmente definir valores reais para as ordens `u` (por exemplo, `u_2 = 3.0`, `u_3 = 3.0`, `u_4 = 3.0` satisfaz todas as restrições perfeitamente) sem gerar contradição. 
  Como o MTZ permite esses subciclos fracionários na relaxação linear, o limite inferior (*lower bound*) do modelo fica muito longe do ótimo real, forçando o algoritmo de **Branch-and-Bound** a fazer muito mais ramificações e buscas para encontrar e provar a solução inteira ótima.
