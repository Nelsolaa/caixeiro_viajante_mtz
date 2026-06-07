# Guia de Perguntas — Defesa do Caixeiro Viajante (MTZ)

Este documento foi preparado para auxiliar a equipe (**Nelson, Luiz Carlos e Isaias**) no treinamento para a apresentação e sabatina do projeto de Caixeiro Viajante com Formulação Miller-Tucker-Zemlin (MTZ), utilizando o OR-Tools e Pandas.

Utilize este caderno de exercícios para treinar suas respostas antes da avaliação oficial.

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

### Q1. Adicionar uma nova restrição para achar outra solução ótima (Nova Rota)
> **Pergunta:** *"A rota atual é ótima, mas eu quero ver outra. Como você adiciona uma restrição para forçar o modelo a achar um novo caminho (segunda melhor ou outra ótima se houver)?"*

---

### Q2. Forçar ou Proibir um Arco Específico
> **Pergunta:** *"Modifique o código para que o caixeiro passe obrigatoriamente de 2 diretamente para 3 (ou proíba que ele faça esse trajeto)."*

---

### Q3. Mudar a Função Objetivo para minimizar o número de "arcos caros"
> **Pergunta:** *"Mude a função objetivo para minimizar o número de voos/arcos cuja tarifa (custo) seja estritamente maior que 15, em vez de minimizar o custo total."*

---

### Q4. Desativar a volta à origem (Transformar em Caminho Hamiltoniano)
> **Pergunta:** *"Como você alteraria o código para que o caixeiro não precise voltar ao ponto de partida? Ou seja, ele começa no 1 e termina em qualquer outra cidade."*

---

## 🧠 Questões Conceituais de Otimização e Formulação

### Q5. Por que mudar a restrição de demanda de `">="` para `"="` no problema de Corte de Bobinas (ou outros) gera inviabilidade?
> **Pergunta do Professor (Histórico):** *"Por que ao mudar a restrição de demanda de '>= D' para '= D' o modelo apresentou que não há solução viável?"*

---

### Q6. Por que as restrições MTZ de eliminação de subciclo são indexadas apenas para $i, j \neq 1$? O que acontece se incluirmos a origem (vértice 1)?
> **Pergunta:** *"Por que a eliminação de subciclos u_i - u_j + n * x_ij <= n - 1 não se aplica ao vértice 1?"*

---

### Q7. Por que a remoção das restrições MTZ resulta em subciclos (rotas desconexas)?
> **Pergunta:** *"Se eu apagar as restrições MTZ do código, por que o solver retorna rotas que não cobrem todas as cidades de uma vez?"*

---

### Q8. Quantidade de soluções viáveis/ótimas no TSP Simétrico vs. Assimétrico
> **Pergunta:** *"Quantos caminhos hamiltonianos possíveis existem no problema do caixeiro viajante se o grafo for simétrico? E se for assimétrico? E qual a diferença?"*

---

## 📊 Análise de Variáveis e Comportamento do Solver

### Q9. Como exibir os valores de TODAS as variáveis do solver (mesmo as que são 0)?
> **Pergunta do Professor (Histórico):** *"O solver tem que apresentar os valores de cada variável, não só da ótima."*

---

### Q10. O que representam matematicamente as variáveis $u_i$ na solução ótima?
> **Pergunta:** *"O que significa u[3] = 2 e u[2] = 5 no resultado impresso pelo notebook?"*

---

## 💬 Perguntas Individuais / Corpo a Corpo

### Q11. "Como os dados são gerados e lidos aqui?"
* *Escreva sua resposta de simulação aqui.*

---

### Q12. "Como está configurado o solver de vocês? Qual biblioteca e algoritmo?"
* *Escreva sua resposta de simulação aqui.*

---

### Q13. "O que acontece se o grafo de entrada não for completo?"
* *Escreva sua resposta de simulação aqui.*
