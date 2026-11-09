"""Operações compartilhadas: divisão exata, liberação e coalescência."""

from bisect import bisect_left

from .models import Block


class InvariantError(RuntimeError):
    """Estado inválido: interromper a execução, nunca publicar seu resumo."""


class Memory:
    def __init__(self, capacity=4096):
        if type(capacity) is not int or capacity <= 0:
            raise ValueError("A capacidade deve ser um inteiro positivo.")
        self.capacity = capacity
        self.free = [Block(0, capacity)]
        self.active: dict[int, Block] = {}
        self.validate()

    def allocate(self, identifier, size, policy):
        if type(size) is not int or size <= 0 or type(identifier) is not int or identifier <= 0:
            raise ValueError("ID e tamanho devem ser inteiros positivos.")
        if identifier in self.active:
            raise ValueError("Identificador já ativo.")
        chosen, examined = policy(self.free, size)
        if chosen is None:
            self.validate()  # Recusas também passam pela verificação.
            return None, examined
        if chosen not in self.free or chosen.size < size:
            raise InvariantError("Política retornou um bloco inválido.")
        # Localizar a posição para atualizar a lista não é uma nova decisão de
        # seleção. A métrica conta só a busca feita pela função de política.
        index = self.free.index(chosen)
        if chosen.size == size:
            del self.free[index]
        else:
            self.free[index] = Block(chosen.start + size, chosen.size - size)
        self.active[identifier] = Block(chosen.start, size)
        self.validate()
        return chosen.start, examined

    def release(self, identifier):
        if identifier not in self.active:
            raise InvariantError(f"Liberação de ID inativo: {identifier}")
        block = self.active.pop(identifier)
        index = bisect_left(self.free, block)
        start, size = block
        if index > 0 and self.free[index - 1].end == start:
            left = self.free.pop(index - 1)
            index -= 1
            start = left.start
            size += left.size
        if index < len(self.free) and start + size == self.free[index].start:
            size += self.free.pop(index).size
        self.free.insert(index, Block(start, size))
        self.validate()
        return block

    def validate(self):
        """Verificação completa após cada operação, sem usar assert/-O."""
        previous_end = -1
        for block in self.free:
            if block.start <= previous_end:
                raise InvariantError("Lista livre desordenada, sobreposta ou sem coalescência.")
            previous_end = block.end
        if any(type(identifier) is not int or identifier <= 0 for identifier in self.active):
            raise InvariantError("Identificador ativo inválido.")
        # Juntar livres e ocupados deve formar exatamente uma partição de [0,M).
        # Isso verifica simultaneamente conservação, limites e sobreposições.
        cursor = 0
        for start, size in sorted([*self.free, *self.active.values()]):
            if type(start) is not int or type(size) is not int or size <= 0 or start != cursor:
                raise InvariantError("Partição inválida: lacuna, sobreposição, limite ou tamanho.")
            cursor += size
        if cursor != self.capacity:
            raise InvariantError("A soma de livres e ocupados difere da capacidade.")

    def require_drained(self):
        self.validate()
        if self.active or self.free != [Block(0, self.capacity)]:
            raise InvariantError("Drenagem não recuperou a memória integralmente.")
