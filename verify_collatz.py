"""Independently check captured collatz.py stdout without importing collatz.py.

Usage: python3 verify_collatz.py <captured_stdout_file>
"""

import json
import sys


def reference_sequence(start: int) -> list[int]:
    # Bitwise formulation, deliberately different from collatz.py's // and %.
    values = [start]
    n = start
    while n != 1:
        n = (n >> 1) if not (n & 1) else (n << 1) + n + 1
        values.append(n)
    return values


def main() -> None:
    with open(sys.argv[1], encoding="utf-8") as f:
        text = f.read()

    assert text.endswith("\n"), "stdout does not end with a newline"
    lines = text.split("\n")[:-1]
    *number_lines, total_line = lines

    values = [int(line) for line in number_lines]
    assert all(str(v) == line for v, line in zip(values, number_lines)), "non-canonical integer line"

    assert values[0] == 27, "sequence does not start at 27"
    assert values[-1] == 1, "sequence does not end at 1"
    assert values.count(1) == 1, "1 appears before the final value"
    for a, b in zip(values, values[1:]):
        expected = a // 2 if a % 2 == 0 else 3 * a + 1
        assert b == expected, f"bad transition {a} -> {b}"

    reference = reference_sequence(27)
    assert values == reference, "printed sequence differs from bitwise reference"

    value_count = len(values)
    transition_count = sum(1 for _ in zip(values, values[1:]))
    assert transition_count == value_count - 1
    assert total_line == f"Total steps: {transition_count}", f"bad total line: {total_line!r}"

    print(json.dumps({
        "stdout_lines": len(lines),
        "value_count": value_count,
        "transition_count": transition_count,
        "reference_value_count": len(reference),
        "max_value": max(values),
        "total_line": total_line,
        "all_checks_passed": True,
    }))


if __name__ == "__main__":
    main()
