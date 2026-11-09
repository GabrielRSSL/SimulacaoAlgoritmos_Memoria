# Regras permanentes

- Preservar o artigo original, a pasta `Referencias` e resultados anteriores.
- Manter Python simples, núcleo apenas com biblioteca padrão e comentários em português.
- Tratar `docs/protocolo_v1.md` e `configs/*.json` como protocolo explícito. Não alterar parâmetros para favorecer políticas.
- As políticas recebem a mesma lista livre por endereço e os mesmos rastros previamente salvos. Nunca sortear durante a simulação.
- Verificar invariantes após cada alocação, recusa e liberação, inclusive na drenagem. Falhas não podem gerar resumos válidos.
- Resultados novos precisam de diretório novo; não sobrescrever execuções. Manter hashes e cópia do código/configuração usados.
- Executar `python -m pytest` antes de coleta. Comparações são descritivas e pareadas por cenário/semente; solicitações não são réplicas independentes.
- Métricas excluem aquecimento e drenagem. D é ausente quando F=0; nunca preencher ausências com zero.
- Ao mudar código experimental, gerar novo congelamento e repetir validação/piloto se a mudança afetar resultados.
- Não modificar o artigo nem escrever sua conclusão definitiva sem pedido explícito.
