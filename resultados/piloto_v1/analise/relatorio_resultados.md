# Relatório descritivo da simulação

Piloto: 54 execuções válidas, 18 rastros e 10000 tentativas de coleta por execução. Capacidade 4096; aquecimento 2000; drenagem verificada e excluída das médias.

## Atendimento

Média ± desvio-padrão amostral entre execuções. NA indica ausência.

| Cenário | Algoritmo | Atendimento por quantidade (%) | Atendimento por volume (%) | Recusa por fragmentação (%) | Recusa por espaço total (%) |
| --- | --- | --- | --- | --- | --- |
| P1D1 | Best Fit | 100.000 ± 0.000 | 100.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P1D1 | First Fit | 100.000 ± 0.000 | 100.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P1D1 | Worst Fit | 100.000 ± 0.000 | 100.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P1D2 | Best Fit | 94.930 ± 0.286 | 93.452 ± 0.337 | 5.070 ± 0.286 | 0.000 ± 0.000 |
| P1D2 | First Fit | 93.123 ± 0.440 | 90.953 ± 0.512 | 6.877 ± 0.440 | 0.000 ± 0.000 |
| P1D2 | Worst Fit | 87.560 ± 0.331 | 83.344 ± 0.348 | 12.440 ± 0.331 | 0.000 ± 0.000 |
| P2D1 | Best Fit | 100.000 ± 0.000 | 100.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P2D1 | First Fit | 100.000 ± 0.000 | 100.000 ± 0.000 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| P2D1 | Worst Fit | 99.917 ± 0.012 | 99.841 ± 0.021 | 0.083 ± 0.012 | 0.000 ± 0.000 |
| P2D2 | Best Fit | 95.273 ± 0.115 | 91.947 ± 0.141 | 4.727 ± 0.115 | 0.000 ± 0.000 |
| P2D2 | First Fit | 93.870 ± 0.246 | 89.561 ± 0.357 | 6.130 ± 0.246 | 0.000 ± 0.000 |
| P2D2 | Worst Fit | 88.177 ± 0.187 | 79.618 ± 0.222 | 11.823 ± 0.187 | 0.000 ± 0.000 |
| P3D1 | Best Fit | 99.477 ± 0.031 | 95.948 ± 0.262 | 0.517 ± 0.023 | 0.007 ± 0.012 |
| P3D1 | First Fit | 99.487 ± 0.055 | 96.078 ± 0.387 | 0.507 ± 0.067 | 0.007 ± 0.012 |
| P3D1 | Worst Fit | 96.893 ± 0.428 | 76.434 ± 2.579 | 3.107 ± 0.428 | 0.000 ± 0.000 |
| P3D2 | Best Fit | 97.273 ± 0.168 | 78.745 ± 0.936 | 2.683 ± 0.191 | 0.043 ± 0.035 |
| P3D2 | First Fit | 97.303 ± 0.278 | 79.320 ± 1.708 | 2.677 ± 0.287 | 0.020 ± 0.010 |
| P3D2 | Worst Fit | 92.817 ± 0.497 | 45.415 ± 2.865 | 7.183 ± 0.497 | 0.000 ± 0.000 |

## Organização do espaço livre

Média ± desvio-padrão amostral entre execuções. NA indica ausência.

| Cenário | Algoritmo | Ocupação U (fração) | Memória livre F (unidades) | Maior bloco B (unidades) | Número de blocos livres (blocos) | Dispersão D nos instantes válidos (índice) |
| --- | --- | --- | --- | --- | --- | --- |
| P1D1 | Best Fit | 0.624 ± 0.001 | 1538.778 ± 4.062 | 1029.588 ± 18.446 | 32.129 ± 0.160 | 0.327 ± 0.010 |
| P1D1 | First Fit | 0.624 ± 0.001 | 1538.778 ± 4.062 | 998.436 ± 7.640 | 33.225 ± 0.095 | 0.350 ± 0.003 |
| P1D1 | Worst Fit | 0.624 ± 0.001 | 1538.778 ± 4.062 | 88.028 ± 1.233 | 29.658 ± 0.424 | 0.943 ± 0.001 |
| P1D2 | Best Fit | 0.878 ± 0.001 | 500.298 ± 5.827 | 83.874 ± 6.592 | 44.492 ± 0.175 | 0.836 ± 0.010 |
| P1D2 | First Fit | 0.855 ± 0.001 | 594.525 ± 2.652 | 72.778 ± 2.520 | 46.736 ± 0.537 | 0.881 ± 0.004 |
| P1D2 | Worst Fit | 0.784 ± 0.003 | 885.013 ± 11.854 | 43.380 ± 0.269 | 44.449 ± 0.050 | 0.951 ± 0.000 |
| P2D1 | Best Fit | 0.626 ± 0.003 | 1532.626 ± 13.220 | 918.725 ± 11.000 | 28.199 ± 0.430 | 0.397 ± 0.004 |
| P2D1 | First Fit | 0.626 ± 0.003 | 1532.626 ± 13.220 | 930.156 ± 3.350 | 32.369 ± 0.201 | 0.395 ± 0.001 |
| P2D1 | Worst Fit | 0.625 ± 0.003 | 1536.837 ± 13.044 | 99.435 ± 1.367 | 28.199 ± 0.393 | 0.935 ± 0.001 |
| P2D2 | Best Fit | 0.860 ± 0.002 | 571.874 ± 6.358 | 100.860 ± 1.746 | 38.056 ± 0.035 | 0.826 ± 0.003 |
| P2D2 | First Fit | 0.838 ± 0.001 | 664.322 ± 5.296 | 95.750 ± 1.140 | 45.620 ± 0.120 | 0.861 ± 0.003 |
| P2D2 | Worst Fit | 0.745 ± 0.001 | 1046.453 ± 2.239 | 54.892 ± 0.433 | 41.044 ± 0.238 | 0.948 ± 0.000 |
| P3D1 | Best Fit | 0.612 ± 0.014 | 1590.612 ± 59.004 | 776.656 ± 88.554 | 21.237 ± 0.125 | 0.522 ± 0.034 |
| P3D1 | First Fit | 0.613 ± 0.012 | 1584.950 ± 49.469 | 921.703 ± 69.310 | 26.315 ± 0.287 | 0.444 ± 0.024 |
| P3D1 | Worst Fit | 0.485 ± 0.007 | 2108.898 ± 29.391 | 312.789 ± 13.594 | 19.652 ± 0.274 | 0.850 ± 0.009 |
| P3D2 | Best Fit | 0.738 ± 0.011 | 1073.354 ± 43.601 | 353.688 ± 5.615 | 27.940 ± 0.377 | 0.658 ± 0.008 |
| P3D2 | First Fit | 0.745 ± 0.004 | 1044.815 ± 14.502 | 435.264 ± 12.124 | 37.426 ± 0.361 | 0.605 ± 0.011 |
| P3D2 | Worst Fit | 0.429 ± 0.020 | 2338.359 ± 80.946 | 229.168 ± 2.478 | 27.092 ± 0.156 | 0.901 ± 0.005 |

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
| P1D1 | Best Fit | 29.759 ± 0.207 | 43.000 ± 1.000 |
| P1D1 | First Fit | 16.950 ± 0.080 | 42.000 ± 1.000 |
| P1D1 | Worst Fit | 29.658 ± 0.424 | 41.000 ± 1.000 |
| P1D2 | Best Fit | 40.638 ± 0.144 | 56.333 ± 1.155 |
| P1D2 | First Fit | 24.928 ± 0.268 | 58.000 ± 1.000 |
| P1D2 | Worst Fit | 44.464 ± 0.050 | 54.333 ± 0.577 |
| P2D1 | Best Fit | 24.489 ± 0.392 | 38.000 ± 1.000 |
| P2D1 | First Fit | 15.988 ± 0.155 | 40.333 ± 0.577 |
| P2D1 | Worst Fit | 28.199 ± 0.393 | 37.333 ± 0.577 |
| P2D2 | Best Fit | 31.740 ± 0.050 | 49.667 ± 1.155 |
| P2D2 | First Fit | 23.327 ± 0.030 | 58.667 ± 0.577 |
| P2D2 | Worst Fit | 41.053 ± 0.238 | 51.667 ± 2.082 |
| P3D1 | Best Fit | 16.206 ± 0.197 | 32.000 ± 1.000 |
| P3D1 | First Fit | 12.283 ± 0.098 | 35.667 ± 1.155 |
| P3D1 | Worst Fit | 19.652 ± 0.274 | 29.000 ± 1.000 |
| P3D2 | Best Fit | 19.901 ± 0.390 | 41.667 ± 1.528 |
| P3D2 | First Fit | 17.454 ± 0.142 | 48.667 ± 1.528 |
| P3D2 | Worst Fit | 27.092 ± 0.156 | 37.333 ± 1.155 |

O máximo de cada execução consta em `search_max`. A média desses máximos aparece na tabela de busca; a coluna `maximum` do resumo agregado, para essa métrica, é o máximo global do grupo. Essas três grandezas não são intercambiáveis.

## Comparações descritivas por cenário

**P1D1.** First Fit: 100.000% por quantidade, 100.000% por volume e 16.950 blocos examinados por tentativa; Best Fit: 100.000% por quantidade, 100.000% por volume e 29.759 blocos examinados por tentativa; Worst Fit: 100.000% por quantidade, 100.000% por volume e 29.658 blocos examinados por tentativa.

**P1D2.** First Fit: 93.123% por quantidade, 90.953% por volume e 24.928 blocos examinados por tentativa; Best Fit: 94.930% por quantidade, 93.452% por volume e 40.638 blocos examinados por tentativa; Worst Fit: 87.560% por quantidade, 83.344% por volume e 44.464 blocos examinados por tentativa.

**P2D1.** First Fit: 100.000% por quantidade, 100.000% por volume e 15.988 blocos examinados por tentativa; Best Fit: 100.000% por quantidade, 100.000% por volume e 24.489 blocos examinados por tentativa; Worst Fit: 99.917% por quantidade, 99.841% por volume e 28.199 blocos examinados por tentativa.

**P2D2.** First Fit: 93.870% por quantidade, 89.561% por volume e 23.327 blocos examinados por tentativa; Best Fit: 95.273% por quantidade, 91.947% por volume e 31.740 blocos examinados por tentativa; Worst Fit: 88.177% por quantidade, 79.618% por volume e 41.053 blocos examinados por tentativa.

**P3D1.** First Fit: 99.487% por quantidade, 96.078% por volume e 12.283 blocos examinados por tentativa; Best Fit: 99.477% por quantidade, 95.948% por volume e 16.206 blocos examinados por tentativa; Worst Fit: 96.893% por quantidade, 76.434% por volume e 19.652 blocos examinados por tentativa.

**P3D2.** First Fit: 97.303% por quantidade, 79.320% por volume e 17.454 blocos examinados por tentativa; Best Fit: 97.273% por quantidade, 78.745% por volume e 19.901 blocos examinados por tentativa; Worst Fit: 92.817% por quantidade, 45.415% por volume e 27.092 blocos examinados por tentativa.

## Diferenças pareadas e leitura

As diferenças são First Fit menos Best Fit, First Fit menos Worst Fit e Best Fit menos Worst Fit. Valores positivos indicam maior valor da métrica no primeiro algoritmo. Para atendimento isso significa mais atendimento; para recusas e busca, mais recusas ou mais blocos examinados. Ocupação e D exigem interpretação conjunta com atendimento e tamanhos. Diferenças de métricas em % são expressas em pontos percentuais. As tabelas preservam cada diferença por semente e o desvio-padrão das diferenças, não a diferença dos desvios-padrão.

## Método de agregação e limitações

Cada execução é resumida primeiro. Cada semente tem peso igual na média do cenário; o desvio-padrão é amostral (denominador n−1). Os eventos sucessivos compartilham o estado e não são tratados como observações independentes. Não foram realizados testes inferenciais nem calculados intervalos de confiança.

D é definido somente quando F>0. Execuções sem D válido permanecem ausentes e são excluídas apenas da agregação dessa métrica; `n_valid` e `n_runs` expõem o denominador. Diferenças de D exigem ambos os valores presentes; caso contrário, o par permanece ausente. Um único valor não permite desvio-padrão amostral. Não se imputam zeros.

D mede a distribuição do espaço livre e não uma fração definitivamente perdida. Blocos examinados medem somente a busca, não tempo de CPU. A demanda nominal de 62,5% em D1 e 93,75% em D2 é carga oferecida teórica. As distribuições são sintéticas, com tamanhos e permanências independentes, capacidade única e pedidos recusados descartados. Os conjuntos aceitos podem divergir entre políticas. Os resultados não representam aplicações reais nem estabelecem superioridade universal.

As séries ilustrativas usam a semente 1001, definida antes da execução. As janelas temporais têm 500 chegadas; servem à descrição e não são réplicas adicionais. A avaliação do aquecimento está no relatório específico do piloto. O artigo original não foi alterado.
