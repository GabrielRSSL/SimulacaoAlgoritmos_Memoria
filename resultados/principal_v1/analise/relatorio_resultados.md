# Relatório descritivo da simulação

Coleta principal completa: 540 execuções válidas, 180 rastros e 10000 tentativas de coleta por execução. Capacidade 4096; aquecimento 2000; drenagem verificada e excluída das médias.

## Atendimento

Média ± desvio-padrão amostral entre execuções. NA indica ausência.

| Cenário | Algoritmo | Atendimento por quantidade (%) | Atendimento por volume (%) | Recusa por fragmentação (%) | Recusa por espaço total (%) |
| --- | --- | --- | --- | --- | --- |
| P1D1 | Best Fit | 100.000 ± 0.000 | 100.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P1D1 | First Fit | 100.000 ± 0.000 | 100.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P1D1 | Worst Fit | 99.998 ± 0.005 | 99.998 ± 0.008 | 0.002 ± 0.005 | 0.000 ± 0.000 |
| P1D2 | Best Fit | 95.083 ± 0.229 | 93.588 ± 0.289 | 4.917 ± 0.229 | 0.000 ± 0.000 |
| P1D2 | First Fit | 93.350 ± 0.219 | 91.203 ± 0.261 | 6.650 ± 0.219 | 0.000 ± 0.000 |
| P1D2 | Worst Fit | 87.789 ± 0.267 | 83.649 ± 0.328 | 12.211 ± 0.267 | 0.000 ± 0.000 |
| P2D1 | Best Fit | 100.000 ± 0.000 | 100.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P2D1 | First Fit | 100.000 ± 0.000 | 100.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P2D1 | Worst Fit | 99.913 ± 0.035 | 99.836 ± 0.066 | 0.087 ± 0.035 | 0.000 ± 0.000 |
| P2D2 | Best Fit | 95.215 ± 0.293 | 91.883 ± 0.454 | 4.785 ± 0.293 | 0.000 ± 0.000 |
| P2D2 | First Fit | 93.764 ± 0.368 | 89.408 ± 0.556 | 6.236 ± 0.368 | 0.000 ± 0.000 |
| P2D2 | Worst Fit | 88.009 ± 0.302 | 79.398 ± 0.414 | 11.991 ± 0.302 | 0.000 ± 0.000 |
| P3D1 | Best Fit | 99.509 ± 0.121 | 96.147 ± 0.851 | 0.487 ± 0.122 | 0.004 ± 0.008 |
| P3D1 | First Fit | 99.556 ± 0.104 | 96.553 ± 0.716 | 0.443 ± 0.104 | 0.001 ± 0.004 |
| P3D1 | Worst Fit | 97.263 ± 0.325 | 78.728 ± 2.006 | 2.737 ± 0.325 | 0.000 ± 0.000 |
| P3D2 | Best Fit | 97.323 ± 0.238 | 79.013 ± 1.489 | 2.629 ± 0.243 | 0.048 ± 0.036 |
| P3D2 | First Fit | 97.408 ± 0.229 | 80.019 ± 1.426 | 2.571 ± 0.220 | 0.022 ± 0.031 |
| P3D2 | Worst Fit | 92.917 ± 0.336 | 45.776 ± 1.891 | 7.083 ± 0.336 | 0.000 ± 0.000 |

## Organização do espaço livre

Média ± desvio-padrão amostral entre execuções. NA indica ausência.

| Cenário | Algoritmo | Ocupação U (fração) | Memória livre F (unidades) | Maior bloco B (unidades) | Número de blocos livres (blocos) | Dispersão D nos instantes válidos (índice) |
| --- | --- | --- | --- | --- | --- | --- |
| P1D1 | Best Fit | 0.625 ± 0.003 | 1537.044 ± 11.818 | 1031.479 ± 17.167 | 32.157 ± 0.292 | 0.326 ± 0.009 |
| P1D1 | First Fit | 0.625 ± 0.003 | 1537.044 ± 11.818 | 1005.727 ± 14.646 | 33.316 ± 0.328 | 0.345 ± 0.005 |
| P1D1 | Worst Fit | 0.625 ± 0.003 | 1537.097 ± 11.794 | 87.834 ± 1.562 | 29.646 ± 0.374 | 0.943 ± 0.001 |
| P1D2 | Best Fit | 0.877 ± 0.001 | 504.214 ± 5.911 | 85.036 ± 2.646 | 44.758 ± 0.420 | 0.835 ± 0.004 |
| P1D2 | First Fit | 0.855 ± 0.001 | 595.387 ± 5.662 | 73.418 ± 2.284 | 47.152 ± 0.430 | 0.880 ± 0.003 |
| P1D2 | Worst Fit | 0.784 ± 0.001 | 884.942 ± 6.008 | 43.396 ± 0.195 | 44.536 ± 0.291 | 0.951 ± 0.000 |
| P2D1 | Best Fit | 0.625 ± 0.004 | 1534.981 ± 18.091 | 919.332 ± 27.800 | 28.038 ± 0.231 | 0.397 ± 0.012 |
| P2D1 | First Fit | 0.625 ± 0.004 | 1534.981 ± 18.091 | 932.119 ± 23.300 | 32.033 ± 0.239 | 0.393 ± 0.009 |
| P2D1 | Worst Fit | 0.624 ± 0.004 | 1539.153 ± 17.271 | 100.564 ± 1.736 | 27.992 ± 0.329 | 0.935 ± 0.001 |
| P2D2 | Best Fit | 0.862 ± 0.003 | 567.280 ± 11.904 | 101.410 ± 3.830 | 37.923 ± 0.306 | 0.824 ± 0.004 |
| P2D2 | First Fit | 0.838 ± 0.002 | 662.625 ± 7.176 | 95.825 ± 3.646 | 45.511 ± 0.331 | 0.861 ± 0.004 |
| P2D2 | Worst Fit | 0.745 ± 0.003 | 1045.778 ± 11.608 | 54.660 ± 0.403 | 41.102 ± 0.348 | 0.948 ± 0.001 |
| P3D1 | Best Fit | 0.597 ± 0.014 | 1650.313 ± 55.664 | 829.118 ± 58.830 | 21.049 ± 0.195 | 0.508 ± 0.021 |
| P3D1 | First Fit | 0.599 ± 0.014 | 1640.558 ± 57.345 | 972.115 ± 59.410 | 26.266 ± 0.233 | 0.435 ± 0.017 |
| P3D1 | Worst Fit | 0.489 ± 0.008 | 2095.010 ± 34.028 | 323.191 ± 8.004 | 19.407 ± 0.137 | 0.844 ± 0.004 |
| P3D2 | Best Fit | 0.737 ± 0.008 | 1075.375 ± 31.389 | 353.424 ± 20.532 | 27.917 ± 0.403 | 0.659 ± 0.012 |
| P3D2 | First Fit | 0.745 ± 0.007 | 1042.715 ± 30.371 | 448.316 ± 22.718 | 37.453 ± 0.432 | 0.593 ± 0.012 |
| P3D2 | Worst Fit | 0.428 ± 0.016 | 2343.726 ± 63.960 | 230.909 ± 4.736 | 26.982 ± 0.224 | 0.900 ± 0.005 |

## Cobertura da dispersão

Média ± desvio-padrão amostral entre execuções. NA indica ausência.

| Cenário | Algoritmo | Instantes com D válido (instantes) | Proporção com D válido (fração) | Instantes com F=0 (instantes) | Proporção com F=0 (fração) |
| --- | --- | --- | --- | --- | --- |
| P1D1 | Best Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P1D1 | First Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P1D1 | Worst Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P1D2 | Best Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P1D2 | First Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P1D2 | Worst Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P2D1 | Best Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P2D1 | First Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P2D1 | Worst Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P2D2 | Best Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P2D2 | First Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P2D2 | Worst Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P3D1 | Best Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P3D1 | First Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P3D1 | Worst Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P3D2 | Best Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P3D2 | First Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P3D2 | Worst Fit | 10000.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |

## Busca

Média ± desvio-padrão amostral entre execuções. NA indica ausência.

| Cenário | Algoritmo | Esforço médio de busca (blocos/tentativa) | Máximo de busca de cada execução (blocos) |
| --- | --- | --- | --- |
| P1D1 | Best Fit | 29.819 ± 0.305 | 42.900 ± 1.296 |
| P1D1 | First Fit | 17.035 ± 0.185 | 41.933 ± 1.143 |
| P1D1 | Worst Fit | 29.646 ± 0.374 | 39.733 ± 1.081 |
| P1D2 | Best Fit | 40.912 ± 0.419 | 56.933 ± 1.617 |
| P1D2 | First Fit | 25.136 ± 0.243 | 57.733 ± 1.507 |
| P1D2 | Worst Fit | 44.551 ± 0.291 | 54.933 ± 1.048 |
| P2D1 | Best Fit | 24.338 ± 0.215 | 38.900 ± 1.296 |
| P2D1 | First Fit | 15.916 ± 0.131 | 41.233 ± 1.006 |
| P2D1 | Worst Fit | 27.992 ± 0.329 | 38.467 ± 1.383 |
| P2D2 | Best Fit | 31.806 ± 0.276 | 51.200 ± 1.669 |
| P2D2 | First Fit | 23.405 ± 0.221 | 56.000 ± 1.259 |
| P2D2 | Worst Fit | 41.111 ± 0.348 | 51.333 ± 1.470 |
| P3D1 | Best Fit | 15.928 ± 0.243 | 32.333 ± 1.028 |
| P3D1 | First Fit | 12.278 ± 0.150 | 35.733 ± 1.230 |
| P3D1 | Worst Fit | 19.408 ± 0.137 | 28.267 ± 0.828 |
| P3D2 | Best Fit | 19.895 ± 0.330 | 41.533 ± 1.852 |
| P3D2 | First Fit | 17.406 ± 0.235 | 49.400 ± 1.567 |
| P3D2 | Worst Fit | 26.982 ± 0.224 | 37.433 ± 1.501 |

O máximo de cada execução consta em `search_max`. A média desses máximos aparece na tabela de busca; a coluna `maximum` do resumo agregado, para essa métrica, é o máximo global do grupo. Essas três grandezas não são intercambiáveis.

## Comparações descritivas por cenário

**P1D1.** First Fit: 100.000% por quantidade, 100.000% por volume e 17.035 blocos examinados por tentativa; Best Fit: 100.000% por quantidade, 100.000% por volume e 29.819 blocos examinados por tentativa; Worst Fit: 99.998% por quantidade, 99.998% por volume e 29.646 blocos examinados por tentativa.

**P1D2.** First Fit: 93.350% por quantidade, 91.203% por volume e 25.136 blocos examinados por tentativa; Best Fit: 95.083% por quantidade, 93.588% por volume e 40.912 blocos examinados por tentativa; Worst Fit: 87.789% por quantidade, 83.649% por volume e 44.551 blocos examinados por tentativa.

**P2D1.** First Fit: 100.000% por quantidade, 100.000% por volume e 15.916 blocos examinados por tentativa; Best Fit: 100.000% por quantidade, 100.000% por volume e 24.338 blocos examinados por tentativa; Worst Fit: 99.913% por quantidade, 99.836% por volume e 27.992 blocos examinados por tentativa.

**P2D2.** First Fit: 93.764% por quantidade, 89.408% por volume e 23.405 blocos examinados por tentativa; Best Fit: 95.215% por quantidade, 91.883% por volume e 31.806 blocos examinados por tentativa; Worst Fit: 88.009% por quantidade, 79.398% por volume e 41.111 blocos examinados por tentativa.

**P3D1.** First Fit: 99.556% por quantidade, 96.553% por volume e 12.278 blocos examinados por tentativa; Best Fit: 99.509% por quantidade, 96.147% por volume e 15.928 blocos examinados por tentativa; Worst Fit: 97.263% por quantidade, 78.728% por volume e 19.408 blocos examinados por tentativa.

**P3D2.** First Fit: 97.408% por quantidade, 80.019% por volume e 17.406 blocos examinados por tentativa; Best Fit: 97.323% por quantidade, 79.013% por volume e 19.895 blocos examinados por tentativa; Worst Fit: 92.917% por quantidade, 45.776% por volume e 26.982 blocos examinados por tentativa.

## Diferenças pareadas e leitura

As diferenças são First Fit menos Best Fit, First Fit menos Worst Fit e Best Fit menos Worst Fit. Valores positivos indicam maior valor da métrica no primeiro algoritmo. Para atendimento isso significa mais atendimento; para recusas e busca, mais recusas ou mais blocos examinados. Ocupação e D exigem interpretação conjunta com atendimento e tamanhos. Diferenças de métricas em % são expressas em pontos percentuais. As tabelas preservam cada diferença por semente e o desvio-padrão das diferenças, não a diferença dos desvios-padrão.

## Método de agregação e limitações

Cada execução é resumida primeiro. Cada semente tem peso igual na média do cenário; o desvio-padrão é amostral (denominador n−1). Os eventos sucessivos compartilham o estado e não são tratados como observações independentes. Não foram realizados testes inferenciais nem calculados intervalos de confiança.

D é definido somente quando F>0. Execuções sem D válido permanecem ausentes e são excluídas apenas da agregação dessa métrica; `n_valid` e `n_runs` expõem o denominador. Diferenças de D exigem ambos os valores presentes; caso contrário, o par permanece ausente. Um único valor não permite desvio-padrão amostral. Não se imputam zeros.

D mede a distribuição do espaço livre e não uma fração definitivamente perdida. Blocos examinados medem somente a busca, não tempo de CPU. A demanda nominal de 62,5% em D1 e 93,75% em D2 é carga oferecida teórica. As distribuições são sintéticas, com tamanhos e permanências independentes, capacidade única e pedidos recusados descartados. Os conjuntos aceitos podem divergir entre políticas. Os resultados não representam aplicações reais nem estabelecem superioridade universal.

As séries ilustrativas usam a semente 1, definida antes da execução. As janelas temporais têm 500 chegadas; servem à descrição e não são réplicas adicionais. A avaliação do aquecimento está no relatório específico do piloto. O artigo original não foi alterado.
