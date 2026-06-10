# 📝 Caderno de Simulado Final — Questões de Itens (A e B) [SEM GABARITO]

Este simulado contém as mesmas questões estruturadas em dois itens da prova de Modelagem em Programação Matemática (Unifor). Use este arquivo para testar os seus conhecimentos antes de verificar as respostas oficiais.

Tente preencher cada item à mão ou no computador.

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
  
  *(Escreva a equação/restrição linear aqui)*

* **Item B) Implementação no OR-Tools:**
  ```python
  # Escreva o código aqui
  
  ```

---

## <a name="questão-2"></a> 2. Questão 2: Forçar ou Proibir um Arco Específico
> **Problema:** *"Ajuste o modelo para que o caixeiro seja obrigado a viajar diretamente da cidade 2 para a cidade 3. Em seguida, mostre como proibir essa viagem direta."*

* **Item A) Modelagem Matemática:**
  
  *(Escreva as equações para forçar e proibir aqui)*

* **Item B) Implementação no OR-Tools:**
  ```python
  # Escreva o código aqui para forçar e para proibir
  
  ```

---

## <a name="questão-3"></a> 3. Questão 3: Minimizar a Quantidade de Arcos Caros
> **Problema:** *"Altere o objetivo do modelo. Em vez de minimizar o custo financeiro total, minimize a quantidade de trechos viajados cujo custo seja estritamente maior que 15."*

* **Item A) Modelagem Matemática:**
  
  *(Escreva o objetivo matemático modificado e a definição dos coeficientes aqui)*

* **Item B) Implementação no OR-Tools:**
  ```python
  # Escreva o código de redefinição da função objetivo aqui
  
  ```

---

## <a name="questão-4"></a> 4. Questão 4: Transformar em Caminho Aberto (Sem retornar ao início)
> **Problema:** *"Altere o modelo para que o caixeiro realize um caminho aberto que inicia na cidade 1 e termina em qualquer outra cidade, sem a necessidade de retornar à cidade 1."*

* **Item A) Modelagem Matemática:**
  
  *(Escreva as novas equações das restrições de grau aqui)*

* **Item B) Implementação no OR-Tools:**
  ```python
  # Escreva o código para alterar os limites (bounds) das restrições aqui
  
  ```

---

## <a name="questão-5"></a> 5. Questão 5: Precedência de Visitação (Visitar cidade i antes da cidade j)
> **Problema:** *"O caixeiro precisa obrigatoriamente visitar a cidade 4 antes de visitar a cidade 2 na rota final (não necessariamente de forma consecutiva). Como modelar e programar essa restrição?"*

* **Item A) Modelagem Matemática:**
  
  *(Escreva a relação linear para a variável de ordem u aqui)*

* **Item B) Implementação no OR-Tools:**
  ```python
  # Escreva o código simplificado para adicionar a restrição aqui
  
  ```

---

## <a name="questão-6"></a> 6. Questão 6: Fixar uma Cidade em uma Posição Específica da Rota
> **Problema:** *"A cidade 3 deve ser visitada obrigatoriamente como a terceira cidade da rota (lembrando que a origem 1 ocupa a primeira posição). Como fixar essa posição?"*

* **Item A) Modelagem Matemática:**
  
  *(Escreva a equação para fixar a ordem da cidade 3 aqui)*

* **Item B) Implementação no OR-Tools:**
  ```python
  # Escreva o código (usando SetBounds ou solver.Add) aqui
  
  ```

---

## <a name="questão-7"></a> 7. Questão 7: Ativação Condicional de Arcos (Se passar por A, deve passar por B)
> **Problema:** *"Se o caixeiro utilizar o arco 2 -> 3 (ir de 2 diretamente para 3), ele é obrigado a também utilizar o arco 4 -> 5 na mesma rota. Como modelar essa condicional?"*

* **Item A) Modelagem Matemática:**
  
  *(Escreva a inequação linear de implicação de variáveis binárias aqui)*

* **Item B) Implementação no OR-Tools:**
  ```python
  # Escreva o código da restrição condicional aqui
  
  ```
