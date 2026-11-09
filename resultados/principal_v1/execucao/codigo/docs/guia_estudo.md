# Guia para compreender e explicar a simulação

A memória simulada é uma reta de endereços inteiros, não a RAM usada pelo Python. Um bloco `(inicio, tamanho)` representa `[inicio, inicio+tamanho)`. `Memory.free` contém os intervalos livres por endereço; `Memory.active` associa cada ID aceito a um único intervalo. O calendário de eventos e essas estruturas administrativas ficam fora das 4096 unidades simuladas.

As políticas recebem apenas a lista livre e o tamanho pedido. First Fit retorna o primeiro suficiente. Best Fit procura o menor suficiente e pode parar em encaixe exato. Worst Fit procura o maior suficiente em toda a lista. Os empates preservam o primeiro endereço porque a lista já está ordenada. As funções retornam o objeto bloco e o número de entradas examinadas, inclusive em falhas. O método comum de alocação ocupa o começo desse bloco, reduz ou remove o intervalo livre e verifica a memória.

Ao liberar, a região volta à lista no lugar correspondente ao endereço. Se o fim do vizinho esquerdo coincidir com seu início, ambos se unem; depois se verifica o vizinho direito. Não é preciso mover nenhuma região ocupada. Isso é coalescência, diferente de compactação.

## Exemplo passo a passo

Para aprender, use capacidade 10 e First Fit, com aquecimento de uma chegada. Este exemplo é um caso didático, não um resultado dos cenários experimentais.

| Instante | Operação | Livres após a tentativa | Ocupados | Resultado |
| --- | --- | --- | --- | --- |
| 0 | ID 1 pede 6 e permanece 5 | [6,10) | ID 1 em [0,6) | Aceito; aquecimento |
| 1 | ID 2 pede 5 e permanece 1 | [6,10) | ID 1 em [0,6) | Recusa por espaço total: F=4<5 |
| 2 | ID 3 pede 4 e permanece 8 | Nenhum | ID 1 em [0,6), ID 3 em [6,10) | Aceito; F=0 e D ausente |
| 5 | Liberação de ID 1 | [0,6) | ID 3 em [6,10) | Drenagem, fora das métricas |
| 10 | Liberação de ID 3 | [0,10) | Nenhum | Coalescência e recuperação integral |

A recusa de ID 2 não produz liberação no instante 2. ID 1 permanece ativo ao entrar na coleta. Nas duas tentativas da coleta, a aceitação é 50%, o volume atendido é 4/9×100≈44,44%, a ocupação média é (0,6+1)/2=0,8 e a média de D usa somente o instante 1, em que D=0. Não se acrescenta a memória vazia da drenagem à média.

Para visualizar fragmentação, considere os intervalos livres [0,4) e [6,10), separados por uma alocação [4,6). Pedido de 5 falha: F=8≥5, mas B=4<5. Se F fosse menor que 5, a causa seria insuficiência total. As causas descrevem o instante da falha e podem decorrer de decisões anteriores das políticas.

## Por que compartilhar os rastros

Os arquivos de entrada fixam cada ID, chegada, tamanho e permanência. Os mesmos valores são lidos por todas as políticas. Se cada política sorteasse durante a execução, uma recusa poderia mudar a sequência de sorteios e a comparação deixaria de controlar a carga. Mesmo com entradas idênticas, as escolhas de endereço alteram a geometria e podem levar a conjuntos diferentes de aceites. Por isso, ocupação efetiva também pode diferir.

## Como ler as medidas

Atendimento por quantidade conta processos abstratos; atendimento por volume soma unidades. Um algoritmo pode aceitar muitos pedidos pequenos e ainda perder volume relevante ao recusar grandes pedidos de P3. As duas recusas usam como denominador todas as 10000 chegadas da coleta. Aceites mais ambas as recusas devem somar 100%.

F é todo o espaço livre; B é o maior intervalo; U é a fração ocupada; D=1−B/F descreve a fração do espaço livre fora do maior intervalo. Um D elevado não diz que os blocos menores são inúteis: eles ainda podem atender pedidos pequenos. F=0 implica D indefinido. A média de D é condicionada aos instantes válidos, cuja quantidade é exportada.

“Blocos examinados” conta a procura por um bloco. Uma tentativa recusada pode examinar todos os blocos; uma lista vazia custa zero nesse indicador. Ordenação, união, cálculo de métricas, gravação de CSV e verificações têm custo computacional, mas ficam fora dessa medida. Logo, a comparação não permite afirmar que um programa seja tantas vezes mais rápido em CPU.

## Como interpretar a análise

Cada cenário possui 30 réplicas, uma por semente. Cada réplica fornece uma média temporal; a tabela final apresenta média e desvio-padrão dessas 30 médias. A dependência temporal impede considerar 300000 chegadas como réplicas independentes. Diferenças pareadas preservam a semente, por exemplo atendimento de First Fit menos Best Fit: +0,5 significa 0,5 ponto percentual a mais para First Fit. Para busca, +2 significa dois blocos a mais por tentativa.

`search_max` é o pior caso observado em uma execução. A média dos 30 máximos difere do máximo global. DP descreve a dispersão entre sementes; não é intervalo de confiança nem prova de significância. Os gráficos temporais mostram janelas de 500 instantes da semente 1 previamente escolhida; não substituem a análise das 30 réplicas.

## Arquivos para a redação

Comece pelo relatório técnico, pelas tabelas de atendimento, estado, cobertura de D, busca e diferenças pareadas. Use SVG para gráficos vetoriais e PNG para pré-visualização. Consulte o protocolo congelado e os relatórios de validação/piloto para a seção de métodos. Preserve os CSVs, manifests e código como material de reprodução. Nenhum desses arquivos substitui a discussão crítica nem escreve a conclusão definitiva do artigo.
