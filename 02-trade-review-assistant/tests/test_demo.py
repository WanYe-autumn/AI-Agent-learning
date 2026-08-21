def add(a: float, b: float) -> float:
    return a + b

def test_add() -> None:
    result = add(2, 3)

    assert result == 5