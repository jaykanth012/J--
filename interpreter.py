"""A tiny, safe first interpreter for the proposed J-- language (v0.1)."""
from __future__ import annotations
import ast
import re
import sys
from pathlib import Path

PRINT_RE = re.compile(r'^print\s*\((.*)\)\s*;\s*$')

class JDashError(Exception):
    """An error in a J-- source program."""

def execute(source: str) -> list[str]:
    """Run supported J-- statements. Python source is never evaluated."""
    output = []
    for line_number, raw_line in enumerate(source.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("//"):
            continue
        match = PRINT_RE.fullmatch(line)
        if not match:
            raise JDashError(
                f'Line {line_number}: invalid syntax. Expected print("text"); or a // comment.'
            )
        try:
            value = ast.literal_eval(match.group(1).strip())
        except (SyntaxError, ValueError) as exc:
            raise JDashError(
                f"Line {line_number}: print() currently accepts a quoted string only."
            ) from exc
        if not isinstance(value, str):
            raise JDashError(
                f"Line {line_number}: print() currently accepts a quoted string only."
            )
        output.append(value)
    return output

def run_file(filename: str | Path) -> int:
    path = Path(filename)
    try:
        for line in execute(path.read_text(encoding="utf-8")):
            print(line)
    except FileNotFoundError:
        print(f"J-- error: file not found: {path}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"J-- error: could not read {path} as UTF-8 text", file=sys.stderr)
        return 1
    except JDashError as exc:
        print(f"J-- error: {exc}", file=sys.stderr)
        return 1
    return 0

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <program.j>", file=sys.stderr)
        return 2
    return run_file(sys.argv[1])

if __name__ == "__main__":
    raise SystemExit(main())
