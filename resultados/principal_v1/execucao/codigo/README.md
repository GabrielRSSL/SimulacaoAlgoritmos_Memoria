# Comparação de First Fit, Best Fit e Worst Fit

Projeto de simulação para apoiar o artigo **Análise comparativa dos algoritmos First Fit, Best Fit e Worst Fit na alocação contígua de memória**. O núcleo usa somente a biblioteca padrão do Python; pytest valida e matplotlib gera gráficos. Não há interface gráfica, aplicação web ou medição de RAM real.

O protocolo usa capacidade 4096, seis cenários, 30 sementes e 12000 chegadas por rastro, com 2000 de aquecimento e 10000 de coleta. As três políticas compartilham entradas salvas previamente e operações de divisão/liberação. O artigo original e `Referencias/` são preservados.

## Comece por aqui

- `docs/guia_estudo.md`: explicação do código, métricas e exemplo passo a passo.
- `docs/protocolo_v1.md`: especificação completa anterior à coleta.
- `docs/conferencia_artigo.md`: conferência da seção 3 e hash do original.
- `docs/dicionario_dados.md`: significado dos CSVs, ausências e unidades.
- `docs/relatorio_validacao_piloto.md`: execução efetiva da validação e decisão do piloto, produzido após a análise.
- `ENTREGA.md`: índice da entrega efetiva, números executados e comandos verificados, produzido ao terminar.

## Ambiente e instalação

Execute os comandos a partir deste diretório no PowerShell. O ambiente local `.venv` utiliza **CPython 3.12.14**, pytest **9.2.0** e matplotlib **3.11.2**. `requirements.txt` fixa as dependências diretas; `requirements-lock.txt` registra também as transitivas. Não é necessário ativar a venv.

```powershell
.\scripts\preparar_ambiente.ps1
& .\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
& .\.venv\Scripts\python.exe -X utf8 -m pytest -q
& .\.venv\Scripts\python.exe -X utf8 -m memsim --help
```

Nesta máquina, `python` aponta para um alias do Windows sem interpretador instalado. Já foi criado um ambiente local a partir do Python empacotado disponível. Em outro computador, o script pode receber `-Python` seguido do caminho de um Python 3.12 com pip. O script cria a venv com `--without-pip` e usa o pip da base se necessário, pois a distribuição empacotada desta máquina não fornece `ensurepip`. A `.venv` depende da instalação-base e não deve ser copiada como ambiente portátil; recrie-a e instale o lock em outra máquina.

O pytest usa `.pytest_tmp` dentro do projeto para seus temporários, pois o diretório temporário padrão do ambiente restrito do Windows não permitia criar as pastas dos testes. Essa pasta é exclusiva dos testes e pode ser recriada pelo pytest.

## Comandos de reprodução

**Cada saída precisa de um nome novo.** Se uma pasta de saída já existir, o comando recusa sobrescrevê-la. Os caminhos abaixo identificam a primeira execução; em uma repetição troque os sufixos `_v1` por outro identificador em todos os argumentos correspondentes.

Gerar rastros independentemente e executar uma combinação (esta verificação avulsa não entra na coleta principal):

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m memsim traces --config configs/piloto.json --out resultados/rastros_avulsos_v1
& .\.venv\Scripts\python.exe -X utf8 -m memsim run --config configs/piloto.json --traces resultados/rastros_avulsos_v1 --out resultados/execucao_avulsa_v1 --scenario P1D1 --seed 1001 --algorithm first_fit
```

O comando `run` também aceita os mesmos filtros com `configs/principal.json` e os rastros da principal. Sem filtros, executa todo o conjunto da configuração informada. Para a coleta oficial, prefira `full`, que exige congelamento.

Executar piloto completo (testes, 18 rastros, 54 execuções e análise) e auditar seus registros:

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m memsim pilot --config configs/piloto.json --out resultados/piloto_v1
& .\.venv\Scripts\python.exe -X utf8 -m memsim audit --input resultados/piloto_v1/execucao --out resultados/piloto_v1/auditoria
```

Antes da principal, leia o diagnóstico e registre a decisão fundamentada em `docs/decisao_piloto.json`. O arquivo entregue contém a avaliação efetiva desta execução. O congelamento exige piloto completo, testes aprovados e `prosseguir: true`; o programa não considera término sem falhas uma comprovação de estabilidade. Se houver problema material que exija alteração de parâmetros, documente e decida antes de coletar.

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m memsim freeze --config configs/principal.json --pilot resultados/piloto_v1 --assessment docs/decisao_piloto.json --out congelamentos/protocolo_v1
& .\.venv\Scripts\python.exe -X utf8 -m memsim full --config configs/principal.json --frozen congelamentos/protocolo_v1 --out resultados/principal_v1
& .\.venv\Scripts\python.exe -X utf8 -m memsim audit --input resultados/principal_v1/execucao --out resultados/principal_v1/auditoria
```

Regenerar tabelas, gráficos e relatório usando os resumos existentes, sem simular novamente:

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m memsim analyze --input resultados/principal_v1/execucao --out resultados/analise_regenerada_v1
```

Todos os comandos têm saída no terminal. O manifesto informa se o lote está `running`, `complete` ou `failed`. Em caso de falha, não reutilize a pasta como se fosse completa: corrija a causa e execute com novo identificador. O tempo real registrado é administrativo e não é comparado como medida de desempenho dos algoritmos.

## Organização do código

| Arquivo | Função |
| --- | --- |
| `memsim/models.py` | Blocos semiabertos e solicitações imutáveis |
| `memsim/memory.py` | Lista livre, alocações, divisão, coalescência e invariantes |
| `memsim/policies.py` | Escolha de bloco e contagem de exames |
| `memsim/traces.py` | Sorteios independentes, persistência e validação de entradas |
| `memsim/simulation.py` | Ordem dos eventos, recusa, aquecimento, coleta e drenagem |
| `memsim/metrics.py` | Fórmulas por execução |
| `memsim/runner.py` | Lotes, logs gzip, piloto, testes e congelamento |
| `memsim/storage.py` | CSV/JSON, hashes, ambiente e cópia do código |
| `memsim/analysis.py` | Médias/DP, diferenças pareadas, tabelas e gráficos |
| `memsim/audit.py` | Reprodução independente dos registros e conferência das fórmulas |
| `memsim/__main__.py` | Interface de linha de comando |
| `tests/` | Casos determinísticos, oráculo de células e integração |
| `configs/` | Configurações explícitas de piloto e principal |

## Onde estão os resultados

Para cada lote, `rastros/` guarda entradas completas e diagnósticos das distribuições; `execucao/execucoes/` guarda tentativas/liberações comprimidas e resumo individual. `execucao/resumo_execucoes.csv` é a base da agregação. `execucao/series_temporais.csv` conserva janelas de 500 chegadas, inclusive aquecimento, sem drenagem.

Em `analise/`, `relatorio_resultados.md` apresenta os resultados descritivos; `tabelas/` contém CSVs e Markdown; `graficos/` contém PNG e SVG. O congelamento está em `congelamentos/protocolo_v1/`. Cada lote preserva uma cópia das fontes e seus hashes em `execucao/codigo/`, além de ambiente, dependências e hashes de registros no manifesto.

Para a redação do artigo, use as tabelas de atendimento, estado, cobertura de D e busca, as diferenças pareadas, os gráficos SVG e o relatório técnico. Mantenha o protocolo congelado e a validação/piloto como evidência metodológica. A conclusão definitiva do artigo não é gerada por este projeto.

## Limites de interpretação

As unidades e cargas são abstratas. D mede dispersão do espaço livre, não memória definitivamente perdida. Blocos examinados não são tempo de CPU. Médias e desvios-padrão são calculados entre sementes, depois de resumir cada execução; não se tratam chegadas como réplicas independentes. Barras de erro são DP, não intervalos de confiança. Não há testes inferenciais, alegações de significância ou classificação universal das políticas. A cobertura dos instantes válidos de D é sempre informada, e ausências nunca são preenchidas com zero.
