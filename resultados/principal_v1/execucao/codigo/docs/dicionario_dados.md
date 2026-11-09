# Dicionário dos dados exportados

Todos os CSVs são UTF-8, separados por vírgula, com ponto decimal e cabeçalho. Vazios representam ausências, não zeros. Inteiros referem-se a unidades abstratas. Os logs são CSV comprimidos com gzip (`gzip.open(caminho, 'rt', encoding='utf-8', newline='')` e `csv.DictReader`). Não é necessário descompactar previamente. JSON usa `null` para ausências.

## Rastros

`rastros/P1D1/seed_0001.csv` (estrutura repetida por cenário/semente).

| Campo | Definição |
| --- | --- |
| id | Inteiro único no rastro, 1–12000 |
| arrival | Instante inteiro de chegada, 0–11999 |
| size | Unidades contíguas solicitadas |
| duration | Permanência; liberação prevista em arrival+duration se aceito |

O cenário e a semente constam do caminho e do manifesto. `rastros/distribuicoes.csv` contém n, médias, DP amostrais, mínimos/máximos de tamanho e permanência, fração de grandes em P3 e correlação de Pearson descritiva tamanho/permanência. Em P1/P2, `large_fraction` é ausente. Não são testes inferenciais nem resultados das políticas.

## Tentativas

`execucao/execucoes/{cenario}/seed_{semente}/{algoritmo}/tentativas.csv.gz`, 12000 linhas por execução.

| Campo | Definição |
| --- | --- |
| scenario, seed, algorithm | Contexto; algoritmos first_fit, best_fit e worst_fit |
| phase | aquecimento ou coleta |
| time, id, size, duration | Campos do rastro; time equivale a arrival |
| result | aceita ou recusada |
| cause | Vazio em aceites; fragmentacao ou espaco_total em recusas |
| address | Início da alocação aceita; vazio em recusa |
| examined | Quantidade de blocos examinados na seleção, incluindo recusas |
| free_before, largest_before | F e B após liberações e antes da tentativa |
| free, largest, holes | F, B e quantidade de blocos livres após a tentativa |
| occupancy | U=1−F/M, fração no intervalo [0,1] |
| dispersion | D=1−B/F; vazio quando F=0 |

## Liberações

`liberacoes.csv.gz`, uma linha por solicitação aceita em todo o rastro. Recusas nunca aparecem.

| Campo | Definição |
| --- | --- |
| scenario, seed, algorithm | Mesmo contexto das tentativas |
| phase | aquecimento, coleta ou drenagem, conforme instante da liberação |
| time, id | Instante efetivo e identificador liberado |
| address, size | Região devolvida |
| free, largest, holes, occupancy, dispersion | Estado imediatamente após essa liberação e sua coalescência |

No mesmo instante, as linhas de liberações estão por ID crescente. As liberações do instante antecedem sua tentativa. A drenagem começa depois da última chegada; ela não participa de médias experimentais.

## Resumo de execução

`resumo.json` por execução e `execucao/resumo_execucoes.csv` com todos os resumos válidos do lote.

| Campo | Definição |
| --- | --- |
| scenario, seed, algorithm | Chave única da execução |
| n | Tentativas na coleta, 10000 no protocolo |
| accepted | Aceites na coleta |
| requested_volume, accepted_volume | Soma de size solicitado e aceito na coleta |
| fragmentation_count, space_count | Recusas por cada causa na coleta |
| acceptance_pct, volume_pct | Atendimento por quantidade e volume, em % |
| fragmentation_pct, space_pct | Recusas/total de tentativas de coleta ×100 |
| free_mean, largest_mean, holes_mean | Médias temporais de F, B e número de blocos |
| occupancy_mean | Média temporal de U, em fração, não % |
| dispersion_mean | Média de D apenas nos instantes válidos; ausente se nenhum |
| dispersion_valid_count, dispersion_valid_fraction | Número e fração de instantes com F>0 |
| zero_free_count, zero_free_fraction | Número e fração de instantes com F=0 |
| search_mean | Média de examined na coleta |
| search_max | Máximo de examined nesta execução, somente na coleta |
| attempts_all, accepted_all | Tentativas e aceites incluindo aquecimento; dados administrativos |
| effective_releases | Liberações efetivas incluindo aquecimento, coleta e drenagem |
| drainage_releases | Quantidade de liberações apenas na drenagem |
| drained | true se recuperou um único bloco [0,M) e nenhum ID ativo |
| trace_sha256 | Identificador do rastro usado; igual entre as três políticas |

`series_temporais.csv` repete os indicadores por janelas de 500 chegadas, com `phase`, `bin_start` e `bin_end` inclusivos, sem drenagem. São diagnósticos e ilustrações, não novas réplicas. Neste protocolo as fronteiras de fase coincidem com as janelas.

## Agregados e pareamento

`analise/tabelas/resumo_cenario_algoritmo.csv` usa formato longo, uma linha por cenário/algoritmo/métrica:

| Campo | Definição |
| --- | --- |
| metric, unit | Indicador do resumo e sua unidade |
| n_runs | Número total de réplicas disponíveis no grupo |
| n_valid | Número de valores presentes para a métrica |
| mean | Média aritmética entre réplicas válidas, peso igual |
| sd | DP amostral entre réplicas válidas; vazio se menos de duas |
| minimum, maximum | Menor/maior valor da métrica entre as réplicas |

Para `search_max`, `mean` é a média dos máximos por execução e `maximum` é o máximo global do grupo. Para `search_mean`, `maximum` é a maior média por execução, não o maior exame individual.

`diferencas_pareadas_por_semente.csv`: scenario, seed, comparison, metric, unit, difference. A convenção `_minus_` significa primeiro menos segundo. Unidades percentuais viram p.p.; proporções U e cobertura continuam frações. Ausência em qualquer lado implica diferença ausente.

`diferencas_pareadas_resumo.csv`: scenario, comparison, metric, unit, n_pairs, n_valid, mean, sd, minimum, maximum. `n_pairs` inclui pares com diferença ausente; `n_valid` informa os efetivamente agregados.

`diagnostico_temporal.csv`: compara médias de 2000–3999 (`early`) e 4000–11999 (`late`) por execução; `late_minus_early` é a diferença. Agrega janelas com peso n, ou número de D válidos para dispersão. Não constitui teste de estacionariedade.

## Manifests e auditoria

Manifests JSON registram status running/complete/failed, datas UTC, versão do Python e bibliotecas, ambiente, config_hash, code_hash, hashes SHA-256 de entradas/saídas e seleção de cenário/semente/algoritmo. `codigo/` conserva fontes e `hashes.json`; `congelamentos/` preserva o protocolo anterior à coleta. Sem Git, commit/status são nulos, e os hashes identificam o código. Caminhos absolutos no manifesto documentam o host original; ao transferir o projeto, o caminho de rastros pode precisar ser atualizado em uma cópia do manifesto, preservando o original.

`auditoria/execucoes_auditadas.csv` informa as execuções verificadas por reprodução independente dos logs. `validacao/pytest.txt`, `pytest.xml` e `test_status.json` documentam os testes executados. Saídas `.parcial` e lotes `failed` não são resultados experimentais válidos.
