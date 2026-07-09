# testforge

> Generate pytest tests from Python source code. Stop writing boilerplate.

[![PyPI](https://img.shields.io/pypi/v/kryptorious-testforge)](https://pypi.org/project/kryptorious-testforge/) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Part of the [Kryptorious developer toolkit](https://kryptorious.gumroad.com/l/jbvet) — 31 open-source tools, one $9 lifetime license.

## Install

```bash
pip install kryptorious-testforge
```

## Quickstart

```bash
printf "def add(a,b):\n    return a+b\n" > mod.py
testforge generate mod.py --output test_mod.py
# -> creates test_mod.py importing add()
```

## Commands

| Command | Description |
|---------|-------------|
| `testforge generate app.py --output tests/test_app.py` | Generate a test file from a source module. |
| `testforge suite src/` | Generate tests for every .py file in a directory. |
| `testforge fixtures` | Generate conftest.py with common fixtures. |
| `testforge coverage` | Show which functions lack tests. |



## License

MIT — free for personal and commercial use. The $9 lifetime license adds DevFlow Premium (multi-environment CI/CD, approval gates, infrastructure-as-code). Get it at [kryptorious.gumroad.com/l/jbvet](https://kryptorious.gumroad.com/l/jbvet).
