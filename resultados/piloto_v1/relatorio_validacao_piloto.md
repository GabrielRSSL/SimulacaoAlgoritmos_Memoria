# Relatório de validação e piloto

O piloto completo foi aprovado para prosseguir com o protocolo original, sem alteração de capacidade, distribuições, aquecimento, métricas ou sementes principais. Essa decisão se baseia em testes, auditoria independente, conferência das entradas e inspeção temporal; não equivale a comprovação estatística de estacionariedade.

## Ambiente e conferência do artigo

Execução em Windows, CPython 3.12.14, pytest 9.2.0 e matplotlib 3.11.2. Versões completas e identificação do host estão nos manifests; dependências transitivas constam de `requirements-lock.txt`. O núcleo usa somente biblioteca padrão. Não havia repositório Git; SHA-256 e cópias das fontes identificam a versão usada.

A seção 3 do artigo foi conferida em modo de leitura. Não foi identificada divergência material. A escolha independente da componente de P3, as sementes do piloto e a convenção de geração detalham a implementação, conforme o pedido. O arquivo original foi preservado, com hash registrado em `conferencia_artigo.md`.

## Testes efetivamente executados

A suíte final executada pelo comando `pilot` contém **48 testes aprovados**, em 1,73 s na rodada registrada. Evidências: `resultados/piloto_v1/validacao/pytest.txt`, `pytest.xml` e `test_status.json`.

| Cobertura | Evidência |
| --- | --- |
| Encaixe exato, divisão, ausência de blocos e recusa sem alteração | Casos parametrizados nas três políticas |
| Desempate, quantidade de exames e Best Fit em encaixe exato | Escolhas e contagens conhecidas |
| Exemplo do artigo | Estado válido com separadores; resultados 500/320/2, 200/20/5 e 600/420/5 |
| Coalescência | Vizinhança esquerda, direita e ambos os lados |
| Invariantes | Injeção de sobreposição, lacuna, tamanho negativo, adjacência sem união, desordem e limites |
| Eventos | Liberações simultâneas por ID e antes da chegada; recusa sem liberação futura |
| Janela | Estado do aquecimento preservado; drenagem excluída |
| D ausente | F=0 e execução inteiramente sem D válido, sem imputação de zero |
| Agregação | DP amostral, pareamento, direção/unidade das diferenças e ausências |
| Rastros | Reprodução com semente, suportes, leitura/gravação e fluxos independentes |
| Integração | Exportação, hashes, auditoria, proteção contra sobrescrita |
| Falhas | Violação injetada deixa manifesto failed e logs parciais, sem resumo válido |
| Sequências adicionais | 600 operações por política comparadas com um oráculo de células |

Na primeira rodada de desenvolvimento, 40 testes passaram e sete não conseguiram preparar seus diretórios temporários no sandbox do Windows. A mesma suíte, executada com permissão, passou (47 testes naquela versão). Foi configurado `.pytest_tmp` no projeto; a suíte posterior de 48 testes passou também dentro do ambiente restrito. Isso foi um ajuste de infraestrutura de teste, sem mudança nos parâmetros ou nas regras de simulação. Nenhum resultado experimental foi obtido de uma suíte com falhas.

## Execução do piloto e auditoria

Foram gerados **18 rastros completos**, seis cenários × sementes 1001, 1002 e 1003, antes das políticas. Foram concluídas **54 execuções**, com **648000 tentativas** incluindo aquecimento e **540000 tentativas de coleta**. O lote levou aproximadamente 120,4 s de execução das simulações no host; esse tempo é administrativo e não é uma métrica comparativa das políticas.

Todas as operações passaram pelas invariantes completas. Todas as execuções drenaram para um único bloco [0,4096), sem IDs ativos. O auditor independente reproduziu **todas as 54 execuções**, reconstruindo a lista livre a partir dos ocupados, verificando escolhas, exames, liberações, hashes, causas de recusa, estados e fórmulas dos resumos. O manifesto está em `resultados/piloto_v1/auditoria/manifest.json`.

A soma aceitação+recusa por fragmentação+recusa por espaço total foi 100% em todas as execuções, sem diferença numérica observada no resumo. Não ocorreram instantes de coleta com F=0 neste piloto; D foi válido nos 540000 instantes de coleta. Os casos de F=0 e D ausente foram verificados pelos testes determinísticos, sem apresentá-los como ocorrências experimentais.

## Conferência das distribuições

Todos os tamanhos e permanências ficaram nos suportes configurados. Por cenário, as médias de tamanho entre as três sementes variaram de 31,965 a 32,010 em P1D1; 31,870 a 32,212 em P1D2; 31,976 a 32,000 em P2D1; 31,839 a 32,057 em P2D2; 32,190 a 33,232 em P3D1; e 31,512 a 32,773 em P3D2. São observações, não valores forçados à média teórica 32.

As frequências de pedidos grandes em P3 ficaram entre 9,817% e 10,500%, sem quota fixa de 10%. As médias de permanência em D1 ficaram entre 79,641 e 80,576; em D2, entre 119,528 e 120,437. As correlações descritivas tamanho/permanência variaram aproximadamente entre −0,01142 e 0,01480. Esses diagnósticos não provam independência; a independência de geração é especificada pelos dois fluxos separados no código. Não foram realizados testes de hipóteses das distribuições.

Fonte dos números: `resultados/piloto_v1/rastros/distribuicoes.csv`.

## Avaliação do aquecimento

Foram inspecionados os seis gráficos `piloto_todas_P1D1.png` a `piloto_todas_P3D2.png`, que mostram as três sementes para cada política, e os registros em janelas consecutivas de 500 chegadas. A linha em t=2000 marca o início da coleta. Em P1/P2, o aumento inicial de ocupação e a formação inicial dos espaços livres se concentram nas primeiras janelas; as curvas posteriores oscilam sem uma deriva monotônica comum às três sementes. Em P3, ocupação e D oscilam mais e exigem cautela.

Foi comparada, por execução, a média em t=2000–3999 com t=4000–11999. As diferenças tardio menos inicial variaram de −0,8125 a +1,4875 ponto percentual no atendimento; de −0,03238 a +0,04252 na fração de ocupação; e de −0,04975 a +0,08739 no índice D. Essas variações não são todas desprezíveis. O maior aumento de D ocorreu em P3D1/Best Fit/semente 1003; outras sementes desse mesmo cenário/política apresentaram diferenças de sinal oposto ou menor magnitude. Em P3D2/Worst Fit, a ocupação mudou +0,04162, +0,01705 e −0,01375 entre as janelas nas três sementes. A presença de variação também em trechos tardios e a ausência de um movimento consistente entre réplicas não sustentaram uma mudança obrigatória do aquecimento nesta avaliação descritiva.

Para contextualizar a variabilidade de P3, as médias de ocupação de janelas de 500 chegadas em P3D2/Worst Fit variaram de 0,33003 a 0,53414 na coleta; em P3D1/Best Fit, D variou de 0,32524 a 0,65108. Esses intervalos descrevem oscilações temporais, não intervalos de confiança. Os valores e diferenças completos estão em `analise/tabelas/diagnostico_temporal.csv` e `execucao/series_temporais.csv` do piloto.

**Decisão:** manter aquecimento de 2000, capacidade 4096, distribuições e métricas, prosseguindo para a coleta principal. Não foi identificado erro material de implementação nem um padrão temporal consistente que exija revisão do protocolo. Não se selecionaram parâmetros em função de desempenho favorável a uma política.

**Limitações:** são somente três sementes de piloto; janelas de 500 podem ocultar transientes curtos; as comparações usam períodos de comprimentos distintos e observações dependentes. Não há teste formal de estacionariedade ou prova de que 2000 seja o aquecimento mínimo/suficiente para qualquer carga. A memória das decisões passadas pode durar além da permanência de um processo, portanto a permanência máxima de 180 não foi usada como prova de estabilização. Flutuações em P3 e possível viés residual devem acompanhar a interpretação da coleta. O término sem erro foi utilizado como evidência de integridade, nunca como evidência isolada de estabilidade.

## Congelamento

A decisão registrada em `docs/decisao_piloto.json` referencia este relatório e o manifesto de auditoria. O comando `freeze` preserva o protocolo, configuração e código em `congelamentos/protocolo_v1/` antes da coleta principal. O comando `full` verifica seus hashes e executa novamente a suíte antes de gerar os 180 rastros e iniciar as 540 simulações. Piloto não será misturado às 30 sementes principais.
