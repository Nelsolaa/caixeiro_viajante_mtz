Modelagem em Programa¸c˜ao Matem´atica
Projeto - AV3
Software utilizado:
OR-Tools.
Exemplos e documenta¸c˜ao:
https://developers.google.com/optimization/
Proposta de projeto:
(i) formar equipes de at´e 3 pessoas;
(ii) implementar o modelo gen´erico de Programa¸c˜ao Linear Inteira de MillerTucker-Zemlin (MTZ) para resolver o Problema do Caixeiro Viajante.
(iii) qualquer outro modelo diferente desse ser´a desconsiderado.
(iv) a modelagem ser´a sujeita a perguntas e modifica¸c˜oes no dia da avalia¸c˜ao;
(v) as ´unicas bibliotecas a serem utilizadas para a realiza¸c˜ao do projeto s˜ao o OR-Tools e o Pandas;
(vi) deve ser utilizada a mesma sintaxe do OR-Tools empregada nas
aulas.
Problema do Caixeiro Viajante
O Problema do Caixeiro Viajante (PCV), conhecido internacionalmente como
Traveling Salesman Problem (TSP), consiste em determinar a rota de menor
custo que permite a um viajante visitar um conjunto de cidades exatamente
uma vez e retornar `a cidade de origem.
Formalmente, dado um conjunto de cidades e os custos (ou distˆancias)
entre cada par de cidades, o objetivo ´e encontrar um ciclo Hamiltoniano de
custo m´ınimo. Seja D = (V, A) um grafo direcionado completo, onde V representa as cidades e cada arco (i, j) ∈ A possui um custo associado cij . O
problema pode ser descrito como a busca por uma permuta¸c˜ao das cidades
que minimize o custo total do percurso.
1
O PCV ´e um dos problemas cl´assicos da otimiza¸c˜ao combinat´oria e pertence `a classe dos problemas NP-dif´ıceis. Sua importˆancia pr´atica abrange
´areas como log´ıstica, planejamento de rotas, manufatura e redes de comunica¸c˜ao.
O objetivo deste projeto ´e desenvolver uma modelagem de Programa¸c˜ao
Linear Inteira para o Problema do Caixeiro Viajante (PCV) utilizando a
formula¸c˜ao de Miller-Tucker-Zemlin (MTZ). Vocˆe deve compreender a estrutura matem´atica do problema e implementar um modelo gen´erico utilizando
o OR-Tools.
Formato da entrada
• arquivo dados-gerais.csv com o n´umero de v´ertices de entrada na
coluna chamada num vertices;
• arquivo dados-arcos.csv com 3 colunas: origem (que representa a
origem do arco), destino (que representa o destino do arco), e custo
(que representa o custo do arco). O formato desse arquivo est´a na aula
do dia 25/05;
• o grafo de entrada deve ser completo, isto ´e, para cada v´ertice i ∈ V ,
deve-se ter um arco para outro v´ertice j ∈ V − {i}.
2