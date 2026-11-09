# Síntese técnica dos resultados principais

Esta síntese descreve as 540 execuções completas das sementes 1 a 30, separadas do piloto. Foram realizadas 6.480.000 tentativas, das quais 5.400.000 pertencem à coleta. Os valores abaixo são médias entre 30 execuções por cenário e política. Os desvios-padrão e todas as diferenças pareadas estão nas tabelas de `resultados/principal_v1/analise/`. Não foram realizados testes inferenciais nem redigida a conclusão definitiva do artigo.

Todas as 540 execuções principais foram posteriormente auditadas por reprodução independente dos registros, sem divergências nas políticas, contagens, estados ou fórmulas. As 54 execuções do piloto também passaram pela auditoria.

## Atendimento por quantidade

| Cenário | First Fit (%) | Best Fit (%) | Worst Fit (%) |
| --- | --- | --- | --- |
| P1D1 | 100,000 | 100,000 | 99,998 |
| P1D2 | 93,350 | 95,083 | 87,789 |
| P2D1 | 100,000 | 100,000 | 99,913 |
| P2D2 | 93,764 | 95,215 | 88,009 |
| P3D1 | 99,556 | 99,509 | 97,263 |
| P3D2 | 97,408 | 97,323 | 92,917 |

Em P1D1 e P2D1, First Fit e Best Fit aceitaram todas as solicitações da coleta em todas as sementes. Worst Fit teve recusas raras: médias de aproximadamente 0,00167% em P1D1 e 0,087% em P2D1, classificadas como fragmentação. A baixa variação desses cenários é um resultado observado e não foi removida da análise.

Em P1D2, a diferença pareada First Fit−Best Fit no atendimento foi **−1,733 ± 0,137 ponto percentual**; em P2D2, **−1,451 ± 0,177 ponto percentual**. Nesses dois cenários de permanência maior, Best Fit apresentou maior atendimento médio que First Fit e Worst Fit. O símbolo ± representa DP amostral das diferenças por semente, não intervalo de confiança.

Nos perfis mistos, First Fit apresentou atendimento médio ligeiramente maior que Best Fit: diferença pareada **+0,0477 ± 0,0456 ponto percentual** em P3D1 e **+0,0847 ± 0,0910 ponto percentual** em P3D2. A direção mudou em relação a P1D2/P2D2; a magnitude e a variabilidade devem ser apresentadas, sem alegar significância estatística.

## Quantidade e volume descrevem efeitos diferentes

Em P3D2, First Fit aceitou em média **97,408% dos pedidos** e **80,019% do volume**; Best Fit, **97,323%** e **79,013%**; Worst Fit, **92,917%** e **45,776%**. O atendimento por quantidade, isoladamente, ocultaria perdas de volume importantes nesse perfil de pedidos grandes ocasionais.

A diferença pareada de volume First Fit−Best Fit foi **+1,006 ± 0,697 ponto percentual** em P3D2. Em P1D2 e P2D2, a mesma diferença foi negativa: **−2,385 ± 0,176** e **−2,476 ± 0,272 pontos percentuais**, respectivamente. Esses números são observações das cargas sintéticas especificadas, não medições de aplicações reais.

## Espaço livre e causas de recusa

A fragmentação predominou entre as recusas. Em P1/P2, todas as recusas observadas na coleta foram dessa causa; em P3, também houve recusas por insuficiência de espaço total em First Fit e Best Fit. Em P3D2, estas últimas corresponderam a aproximadamente **0,022%** e **0,048%** de todas as tentativas, respectivamente. A causa descreve a situação imediata após as liberações e não elimina a influência das decisões passadas.

Em P1D1, Worst Fit apresentou D médio de **0,943**, apesar de atendimento de aproximadamente **99,998%**. Isso ilustra por que D elevado não significa memória definitivamente inutilizável. Em P3D2/Worst Fit, a ocupação média foi aproximadamente **0,428**, a memória livre média **2343,726 unidades** e o maior bloco livre médio **230,909 unidades**; houve em média **7,083% de recusas por fragmentação**. As médias de F e B são descritivas e não representam o estado de cada recusa individual, que está preservado nos logs.

Não houve instante de coleta com F=0 nas 540 execuções principais. Assim, cada execução teve 10000 valores válidos de D e cobertura igual a 100%. O tratamento de F=0 permanece implementado e foi verificado nos testes, sem atribuir esses casos didáticos à coleta.

## Busca

First Fit teve o menor número médio de blocos examinados nos seis cenários. Em P1D2, as médias foram **25,136** para First Fit, **40,912** para Best Fit e **44,551** para Worst Fit. Em P3D2, foram **17,406**, **19,895** e **26,982**, respectivamente.

Esse indicador mede apenas a seleção do bloco, incluindo tentativas recusadas. Não mede tempo de CPU nem inclui os custos de ordenação, coalescência, gravação ou validação. O máximo global observado na coleta foi **61 blocos examinados em uma tentativa**. Ele difere da média dos máximos de cada execução, apresentada separadamente nas tabelas.

## Limites e reprodução

As fontes são `resumo_execucoes.csv`, `resumo_cenario_algoritmo.csv` e as tabelas de diferenças pareadas. As tabelas Markdown arredondam geralmente para três casas; o CSV conserva a precisão numérica exportada. Um DP exibido como 0,000 pode ser pequeno e arredondado; consulte o CSV antes de afirmar que ele é exatamente zero.

Foram preservadas 30 sementes por cenário; a semente 1 foi usada para as séries ilustrativas conforme definido antes da coleta. Regenerar a análise a partir dos resumos produziu os mesmos hashes para os **21 arquivos CSV, Markdown e PNG** comparados. SVGs também foram regenerados; datas e identificadores internos de renderização podem mudar, portanto não se exige identidade binária desses arquivos.

A avaliação do aquecimento, com apenas três sementes de piloto, não comprova estacionariedade. As conclusões devem permanecer limitadas a capacidade 4096, às distribuições sintéticas, à independência dos sorteios e ao descarte imediato das recusas. Os conjuntos aceitos diferem entre políticas. Não se pode generalizar o resultado para qualquer carga, implementação ou sistema operacional real.
