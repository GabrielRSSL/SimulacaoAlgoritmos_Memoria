# Verificação dos comandos de uso

Os comandos foram executados no PowerShell a partir da raiz do projeto. Todos usaram o interpretador local `.venv/Scripts/python.exe`; o registro final da auditoria principal está em seu manifesto, gerado após o término bem-sucedido.

| Comando ou operação | Verificação efetiva |
| --- | --- |
| `scripts/preparar_ambiente.ps1` | Dependências conferidas; Python 3.12.14, pytest 9.2.0 e matplotlib 3.11.2 importados |
| `python -m pip install -r requirements-lock.txt` | Executado pelo instalador; todas as versões fixadas satisfeitas |
| `python -X utf8 -m pytest -q` | Suíte aprovada; a versão final tem 48 testes |
| `python -X utf8 -m memsim --help` | Todos os subcomandos listados |
| `memsim traces --config configs/piloto.json --out resultados/rastros_avulsos_v1` | 18 rastros independentes gerados e preservados |
| `memsim run ... --scenario P1D1 --seed 1001 --algorithm first_fit` | Uma execução completa em `resultados/execucao_avulsa_v1`; verificação de uso, excluída do piloto e da principal |
| `memsim pilot --config configs/piloto.json --out resultados/piloto_v1` | 48 testes, 18 rastros e 54 execuções; tabelas, gráficos e relatório gerados |
| `memsim audit --input resultados/piloto_v1/execucao --out resultados/piloto_v1/auditoria` | 54 execuções verificadas independentemente |
| `memsim freeze ... --out congelamentos/protocolo_v1` | Protocolo congelado após decisão documentada e antes dos rastros principais |
| `memsim full --config configs/principal.json --frozen congelamentos/protocolo_v1 --out resultados/principal_v1` | 48 testes, 180 rastros e 540 execuções; coleta completa |
| `memsim audit --input resultados/principal_v1/execucao --out resultados/principal_v1/auditoria` | 540 execuções verificadas independentemente, sem divergências |
| `memsim analyze --input resultados/principal_v1/execucao --out resultados/analise_regenerada_v1` | Análise regenerada sem novas simulações; 21 CSVs, Markdown e PNGs idênticos por SHA-256 |

O comando de auditoria da principal terminou com código de saída zero; `resultados/principal_v1/auditoria/manifest.json` registra status `complete` e 540 execuções auditadas. O índice `ENTREGA.md` reúne a entrega observada.

As execuções avulsas são verificações de comandos. Não acrescentam sementes à análise, não são misturadas ao piloto e não aumentam o número de rastros principais. A configuração e a cópia do código de cada lote permitem identificar também a versão anterior da verificação avulsa.

Os comandos completos para repetir estão no README. Use diretórios novos: a rejeição de sobrescrita faz parte da proteção dos resultados, e foi coberta por teste de integração.
