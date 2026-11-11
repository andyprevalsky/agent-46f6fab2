"""Print the Collatz sequence starting at 27 and the number of steps to reach 1."""


def collatz(start: int) -> list[int]:
    if start < 1:
        raise ValueError("start must be a positive integer")
    sequence = [start]
    n = start
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        sequence.append(n)
    return sequence


def main() -> None:
    sequence = collatz(27)
    for value in sequence:
        print(value)
    # Steps are transitions between values, one fewer than the number of values.
    print(f"Total steps: {len(sequence) - 1}")


if __name__ == "__main__":
    main()
