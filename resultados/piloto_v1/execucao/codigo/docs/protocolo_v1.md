# Protocolo experimental versão 1.0

Data de especificação: 8 de novembro de 2026. Estudo: **Análise comparativa dos algoritmos First Fit, Best Fit e Worst Fit na alocação contígua de memória**. Este documento registra o protocolo antes da coleta principal; o congelamento adiciona data UTC, configuração, código, dependências e hashes. O artigo original permanece intacto.

## Pergunta e modelo

Como as três políticas influenciam atendimento, fragmentação externa e esforço de busca em diferentes cenários? Simula-se uma região abstrata de 4096 unidades inteiras, inicialmente livre, com intervalos semiabertos [início, início+tamanho). Não se mede a RAM do simulador. Não há paginação, swapping, compactação, alinhamento, cabeçalhos, reservas, escalonamento ou crescimento da memória.

A lista livre permanece ordenada por endereço. As três políticas recebem a mesma lista, sem índices para antecipar falhas. First Fit para no primeiro bloco suficiente; Best Fit escolhe o menor suficiente e só para antes do fim se encontrar encaixe exato; Worst Fit examina a lista inteira e escolhe o maior suficiente. Empates usam o menor endereço. Lista vazia implica zero exames.

A alocação ocupa exatamente o início do bloco escolhido e conserva a sobra positiva. A liberação insere a região e une imediatamente vizinhos livres à esquerda e à direita. Regiões ocupadas nunca se movem; coalescência não é compactação. Localizar a posição do objeto escolhido para atualizar a lista é administração da estrutura, excluída do indicador de busca.

## Entradas e gerador

Os seis cenários são P1D1, P1D2, P2D1, P2D2, P3D1 e P3D2. Todas as uniformes são discretas e inclusivas.

| Perfil | Tamanho | Média teórica |
| --- | --- | --- |
| P1 | U[16,48] | 32 |
| P2 | U[1,63] | 32 |
| P3 | Com probabilidade 0,9: U[1,16]; caso contrário: U[220,267] | 32 |

Em P3 a escolha de componente é refeita independentemente para cada solicitação, sem impor proporção exata. D1 usa U[40,120], média 80; D2 usa U[60,180], média 120. Tamanhos e permanências têm fluxos pseudoaleatórios distintos. A demanda nominal oferecida é 32×80=2560 (62,5%) em D1 e 32×120=3840 (93,75%) em D2; não se trata de ocupação observada.

Usa-se `random.Random` da biblioteca padrão CPython (Mersenne Twister). Para cada combinação cenário/semente, dois fluxos são inicializados com o inteiro big-endian obtido dos 32 bytes de SHA-256 do texto UTF-8 `memsim-v1|{cenario}|{semente}|{fluxo}`. Os nomes de fluxo são `tamanho` e `permanencia`. A versão efetiva do Python é registrada; não se promete identidade entre versões futuras do gerador de inteiros. Os CSVs preservados são a entrada autoritativa para reprodução exata. Não se usa `hash()` do Python. O cenário integra a derivação, portanto não se assume pareamento entre cenários.

Todos os rastros do lote são salvos e identificados por SHA-256 antes de qualquer execução. Nenhum sorteio ocorre durante a simulação. Os três algoritmos compartilham o rastro completo de cada cenário/semente, mas podem aceitar conjuntos distintos.

## Eventos, réplicas e janela

Cada rastro contém 12000 solicitações: IDs 1 a 12000, chegadas 0 a 11999, uma por instante. Em cada instante processam-se as liberações por ID crescente, depois a chegada e então o estado posterior. Aceites liberam em chegada+permanência. Recusas não aguardam, não se repetem e não geram liberações futuras.

Instantes 0–1999 são aquecimento; 2000–11999 são coleta, com 10000 observações temporais por execução. A memória não é reiniciada na fronteira. A drenagem libera todos os aceites restantes e verifica recuperação integral, mas não compõe as médias.

Piloto: sementes 1001, 1002 e 1003, seis cenários, três políticas, 18 rastros e 54 execuções. Principal: sementes 1 a 30, seis cenários, três políticas, 180 rastros e 540 execuções. Não há parada por recusa. Piloto e principal ficam em diretórios distintos.

## Métricas por execução

Todas as métricas experimentais usam somente a coleta. Seja N=10000, A o número de aceites, V o volume solicitado e VA o volume aceito.

| Métrica | Fórmula ou regra |
| --- | --- |
| Atendimento por quantidade | 100 A/N |
| Atendimento por volume | 100 VA/V |
| Recusa por fragmentação | Antes da tentativa, após liberações: F≥s e B<s. Percentual 100 Rf/N |
| Recusa por espaço total | Antes da tentativa: F<s. Percentual 100 Re/N |
| Ocupação | U=1−F/4096, após a tentativa |
| Dispersão | D=1−B/F, após a tentativa, somente se F>0 |
| Estado | Médias de F, B, quantidade de blocos livres e U |
| Cobertura de D | Número e proporção de instantes válidos; número e proporção com F=0 |
| Busca | Média e máximo de blocos examinados nas tentativas, aceitas e recusadas |

A+Rf+Re=N. Quando não há blocos livres, B=0. Quando F=0, D é ausente, nunca zero; sua média usa apenas instantes válidos. Se não existir instante válido, a média da execução permanece ausente. O esforço não inclui atualização da lista, liberação, coalescência, métricas ou invariantes. Não é tempo de CPU. D não é percentual de memória definitivamente inutilizável.

## Validação e avaliação do piloto

Testes determinísticos incluem o exemplo do artigo, encaixe exato, divisão, desempates, recusas, coalescência, eventos simultâneos, continuidade do aquecimento, ausência de D, contagens e drenagem. O exemplo usa separadores ocupados para que os blocos de 100, 500, 200, 300 e 600 não sejam vizinhos livres. Para pedido 180, First Fit escolhe 500 (sobra 320, 2 exames), Best Fit 200 (sobra 20, 5 exames), Worst Fit 600 (sobra 420, 5 exames).

Após cada operação, verifica-se a partição completa: tamanhos positivos, limites, ausência de sobreposições/lacunas, conservação de capacidade, ordem e coalescência. Cada ID ativo tem uma região; o calendário contém exatamente os ativos, uma vez cada, com instante de liberação e tamanho coerentes com o rastro. Falhas encerram o lote, incluem cenário/semente/política/evento e impedem a publicação do resumo agregado. Logs interrompidos conservam sufixo `.parcial` e manifesto `failed`.

O auditor independente reconstrói os livres a partir dos ocupados nos logs; usa um oráculo declarativo para escolhas e contagens, confere entrada compartilhada, liberações, fórmulas e resumos. Não reutiliza os seletores nem o acumulador de métricas.

O piloto inspeciona suportes e momentos observados dos rastros, correlação descritiva tamanho/permanência, frequência observada da componente grande, gráficos de todas as três sementes em janelas de 500 chegadas e comparação descritiva das janelas 2000–3999 e 4000–11999. Não se define teste inferencial ou limiar automático de estabilidade. A inspeção deve registrar possíveis tendências, variação e limitações; o término sem erro não comprova estabilidade. Uma avaliação escrita decide se há problema material. Havendo necessidade de mudar parâmetros, a coleta principal aguarda decisão do usuário. Não havendo problema material, manter parâmetros e prosseguir.

## Agregação e gráficos

Calcular primeiro cada execução; depois média e desvio-padrão amostral entre as 30 sementes, com peso igual por execução. Ausência de D exclui apenas aquela média da agregação de D; expor `n_valid` e `n_runs`. Se menos de duas médias forem válidas, o DP é ausente. Uma diferença pareada de D só existe se ambas as execuções possuírem D válido.

Diferenças: First Fit−Best Fit, First Fit−Worst Fit e Best Fit−Worst Fit na mesma semente e cenário. Positivo significa maior valor no primeiro algoritmo. Métricas percentuais geram diferenças em pontos percentuais. Não se confunde desvio-padrão das diferenças com diferença dos desvios-padrão. Os 10000 eventos não são réplicas independentes.

O máximo de busca pertence a cada execução; sua agregação apresenta média dos máximos. O maior valor da coluna `maximum` desse grupo é o máximo global, uma terceira grandeza. Barras de erro dos gráficos são DP entre sementes, não intervalos de confiança. Séries ilustrativas da coleta usam a semente 1, previamente escolhida. No piloto, a ilustrativa é 1001, além das curvas das três sementes para diagnóstico.

Resultados são descritivos: não se executam testes inferenciais, não se alega significância, não se extrapolam cargas artificiais para aplicações reais e não se declara política universalmente superior.

## Preservação

Cada lote usa pasta nova. CSVs em UTF-8, ponto decimal, vírgula separadora; campos ausentes ficam vazios. Logs grandes usam gzip. Preservam-se entradas, configuração, código, versões, ambiente, hashes, logs, resumos individuais/agregados, diferenças, PNGs, SVGs e relatórios. Se Git existir, registrar commit e alterações; neste diretório inicialmente não havia repositório Git. O congelamento precede a geração e execução da coleta principal.
