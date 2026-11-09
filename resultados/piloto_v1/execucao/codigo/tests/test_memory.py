import random

import pytest

from memsim.memory import InvariantError, Memory
from memsim.models import Block
from memsim.policies import POLICIES, best_fit, first_fit, worst_fit


@pytest.mark.parametrize("policy", POLICIES.values())
def test_exact_split_empty_and_total_failure(policy):
    memory = Memory(10)
    assert memory.allocate(1, 4, policy) == (0, 1)
    assert memory.free == [Block(4, 6)]
    assert memory.allocate(2, 6, policy) == (4, 1)
    assert memory.free == []
    assert memory.allocate(3, 1, policy) == (None, 0)
    assert memory.active == {1: Block(0, 4), 2: Block(4, 6)}
    memory.release(1)
    memory.release(2)
    memory.require_drained()


@pytest.mark.parametrize("order,expected", [([1, 2], [Block(0, 20)]), ([2, 1], [Block(0, 20)]),
                                          ([1, 3, 2], [Block(0, 30)])])
def test_coalescence_left_right_both(order, expected):
    memory = Memory(40)
    for identifier in range(1, 5):
        memory.allocate(identifier, 10, first_fit)
    for identifier in order:
        memory.release(identifier)
    assert memory.free == expected


@pytest.mark.parametrize("policy,chosen_start,remainder,count", [
    (first_fit, 101, 320, 2), (best_fit, 602, 20, 5), (worst_fit, 1104, 420, 5)])
def test_article_valid_example(policy, chosen_start, remainder, count):
    # Separadores de uma unidade mantêm distintos os cinco blocos livres.
    memory = Memory(1704)
    identifier = 1
    freed = []
    for index, size in enumerate([100, 500, 200, 300, 600]):
        memory.allocate(identifier, size, first_fit)
        freed.append(identifier)
        identifier += 1
        if index < 4:
            memory.allocate(identifier, 1, first_fit)
            identifier += 1
    for identifier in freed:
        memory.release(identifier)
    assert [b.size for b in memory.free] == [100, 500, 200, 300, 600]
    assert memory.allocate(100, 180, policy) == (chosen_start, count)
    assert Block(chosen_start + 180, remainder) in memory.free


@pytest.mark.parametrize("policy", POLICIES.values())
def test_tie_lowest_address(policy):
    free = [Block(0, 20), Block(30, 20)]
    assert policy(free, 10)[0] == free[0]


def test_counts_and_best_exact_stop():
    free = [Block(0, 5), Block(10, 12), Block(30, 10), Block(50, 10)]
    assert first_fit(free, 10) == (free[1], 2)
    assert best_fit(free, 10) == (free[2], 3)
    assert worst_fit(free, 10) == (free[1], 4)
    for policy in POLICIES.values():
        assert policy(free, 100) == (None, 4)
        assert policy([], 1) == (None, 0)


@pytest.mark.parametrize("corruption", ["overlap", "gap", "negative", "adjacent", "unsorted", "outside"])
def test_invariants_detect_corruption(corruption):
    memory = Memory(10)
    states = {"overlap": [Block(0, 6), Block(5, 5)], "gap": [Block(0, 3), Block(4, 6)],
              "negative": [Block(0, -1), Block(-1, 11)], "adjacent": [Block(0, 5), Block(5, 5)],
              "unsorted": [Block(6, 4), Block(0, 6)], "outside": [Block(0, 11)]}
    memory.free = states[corruption]
    with pytest.raises(InvariantError):
        memory.validate()


def test_invalid_identifier_and_request():
    memory = Memory(10)
    memory.allocate(1, 3, first_fit)
    with pytest.raises(ValueError):
        memory.allocate(1, 1, first_fit)
    with pytest.raises(ValueError):
        memory.allocate(2, 0, first_fit)
    with pytest.raises(InvariantError):
        memory.release(2)


@pytest.mark.parametrize("policy", POLICIES.values())
def test_random_operations_with_independent_cell_oracle(policy):
    rng, memory, cells = random.Random(721), Memory(64), [None] * 64
    for identifier in range(1, 601):
        if memory.active and rng.random() < 0.48:
            removed = rng.choice(list(memory.active))
            memory.release(removed)
            cells = [None if owner == removed else owner for owner in cells]
        else:
            size = rng.randint(1, 18)
            address, _ = memory.allocate(identifier, size, policy)
            if address is not None:
                assert all(owner is None for owner in cells[address:address + size])
                cells[address:address + size] = [identifier] * size
        actual = [None] * 64
        for owner, block in memory.active.items():
            actual[block.start:block.end] = [owner] * block.size
        assert actual == cells
        free_cells = {i for block in memory.free for i in range(block.start, block.end)}
        assert free_cells == {i for i, owner in enumerate(cells) if owner is None}
