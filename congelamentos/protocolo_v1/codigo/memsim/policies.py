"""Somente a escolha do bloco varia; nenhuma política consulta métricas."""

from .models import Block


def first_fit(free: list[Block], size: int) -> tuple[Block | None, int]:
    for examined, block in enumerate(free, 1):
        if block.size >= size:
            return block, examined
    return None, len(free)


def best_fit(free: list[Block], size: int) -> tuple[Block | None, int]:
    chosen = None
    for examined, block in enumerate(free, 1):
        # Como a lista está por endereço, não substituir no empate preserva
        # o menor endereço. Um encaixe exato já é a melhor escolha possível.
        if block.size == size:
            return block, examined
        if block.size >= size and (chosen is None or block.size < chosen.size):
            chosen = block
    return chosen, len(free)


def worst_fit(free: list[Block], size: int) -> tuple[Block | None, int]:
    chosen = None
    for block in free:
        if block.size >= size and (chosen is None or block.size > chosen.size):
            chosen = block
    return chosen, len(free)


POLICIES = {"first_fit": first_fit, "best_fit": best_fit, "worst_fit": worst_fit}
LABELS = {"first_fit": "First Fit", "best_fit": "Best Fit", "worst_fit": "Worst Fit"}
