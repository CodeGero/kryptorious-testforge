"""TestForge CLI — Automated pytest test generation."""

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="testforge")
def main():
    """TestForge — Generate pytest tests from Python source code.

    Point it at any .py file and get a complete test suite.
    Stop writing boilerplate. Start testing.
    """
    pass


@main.command()
@click.argument("source", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output path (default: test_<source>)")
@click.option("--preview/--write", default=True, help="Preview tests before writing")
def generate(source, output, preview):
    """Generate pytest tests from a Python source file.

    \b
    Examples:
        testforge generate my_module.py
        testforge generate src/app.py -o tests/test_app.py
        testforge generate utils.py --preview
    """
    from .generator import generate_tests

    source_path = Path(source)
    console.print()
    console.print(Panel(
        f"[bold]TestForge — Generate[/bold] tests for [cyan]{source_path.name}[/cyan]",
        border_style="blue"
    ))

    try:
        test_code = generate_tests(str(source_path), output_path=output if not preview else None)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    # Count generated tests
    test_count = test_code.count("def test_")
    class_count = test_code.count("class Test")

    if preview:
        console.print()
        console.print(Syntax(test_code, "python", theme="monokai", line_numbers=True))
        console.print()
        console.print(f"[green]Preview:[/green] {test_count} test(s), {class_count} test class(es)")
        console.print()
        console.print("[dim]Run with --write to save.[/dim]")
    else:
        out = output or f"test_{source_path.name}"
        console.print(f"[green]Generated[/green] → {out}")
        console.print(f"  {test_count} test function(s)")
        console.print(f"  {class_count} test class(es)")


@main.command()
@click.argument("source", type=click.Path(exists=True))
def coverage(source):
    """Analyze which functions lack tests.

    \b
    Example:
        testforge coverage my_module.py
    """
    from .generator import analyze_coverage

    source_path = Path(source)
    console.print()
    console.print(Panel(
        f"[bold]TestForge — Coverage[/bold] for [cyan]{source_path.name}[/cyan]",
        border_style="blue"
    ))

    try:
        result = analyze_coverage(str(source_path))
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    pct = result["coverage_pct"]
    color = "green" if pct >= 80 else "yellow" if pct >= 50 else "red"

    console.print(f"\n[bold {color}]{pct}%[/bold {color}] coverage — "
                  f"{len(result['tested'])} tested, {len(result['untested'])} untested")

    if result["untested"]:
        console.print()
        console.print("[yellow]Untested functions:[/yellow]")
        for func in result["untested"]:
            console.print(f"  • [cyan]{func}[/cyan]()")
        console.print()
        console.print("[dim]Run 'testforge generate' to create tests for these.[/dim]")

    if result["tested"]:
        console.print()
        console.print("[green]Already tested:[/green]")
        for func in result["tested"]:
            console.print(f"  • [green]✓[/green] {func}()")


@main.command()
@click.argument("path", type=click.Path(exists=True), default=".")
@click.option("--output", "-o", default=None, help="Output path for conftest.py")
def fixtures(path, output):
    """Generate conftest.py with common pytest fixtures.

    \b
    Example:
        testforge fixtures
        testforge fixtures tests/ -o tests/conftest.py
    """
    from .generator import generate_fixtures

    console.print()
    console.print(Panel(
        f"[bold]TestForge — Fixtures[/bold] for [cyan]{path}[/cyan]",
        border_style="blue"
    ))

    try:
        result = generate_fixtures(path, output_path=output)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    out_path = output or f"{path}/conftest.py"
    console.print(f"[green]Generated[/green] → {out_path}")
    fixture_count = result.count("@pytest.fixture")
    console.print(f"  {fixture_count} fixture(s)")


@main.command()
@click.argument("source", type=click.Path(exists=True))
@click.option("--output", "-o", default=None,
              help="Output directory (default: ./tests_gen)")
def mock(source, output):
    """Generate mock-object tests for a module or all modules in a directory.

    \b
    Examples:
        testforge mock my_module.py
        testforge mock src/ -o tests/
    """
    console.print()
    console.print(Panel(
        f"[bold]TestForge Mock[/bold] — [cyan]{source}[/cyan]",
        border_style="blue"))

    from pathlib import Path as _Path
    from .generator import generate_tests

    src = _Path(source)
    files = [src] if src.is_file() else sorted(
        p for p in src.rglob("*.py")
        if not p.name.startswith("_") and "test" not in p.name)
    out_dir = _Path(output) if output else _Path("tests_gen")
    out_dir.mkdir(parents=True, exist_ok=True)

    made = 0
    for f in files:
        dest = out_dir / f"test_{f.stem}.py"
        code = generate_tests(str(f), output_path=str(dest))
        if code:
            made += 1
    console.print()
    if made:
        console.print(f"[green]✓ Generated {made} test file(s) in {out_dir}[/green]")
    else:
        console.print("[yellow]No source files found to generate from.[/yellow]")


@main.command()
@click.argument("path", type=click.Path(exists=True), default=".")
@click.option("--output", "-o", default=None,
              help="Output directory (default: ./tests_gen)")
def suite(path, output):
    """Generate a full test suite from an entire directory.

    \b
    Example:
        testforge suite src/ -o tests/
    """
    console.print()
    console.print(Panel(
        f"[bold]TestForge Suite[/bold] — [cyan]{path}[/cyan]",
        border_style="blue"))

    from pathlib import Path as _Path
    from .generator import generate_tests

    root = _Path(path)
    files = sorted(
        p for p in root.rglob("*.py")
        if not p.name.startswith("_") and "test" not in p.name)
    out_dir = _Path(output) if output else _Path("tests_gen")
    out_dir.mkdir(parents=True, exist_ok=True)

    made = 0
    console.print()
    for f in files:
        dest = out_dir / f"test_{f.stem}.py"
        code = generate_tests(str(f), output_path=str(dest))
        if code:
            made += 1
            console.print(f"  [green]✓[/green] {dest}")
    console.print()
    if made:
        console.print(f"[bold]Generated {made} test file(s)[/bold] in {out_dir}")
    else:
        console.print("[yellow]No source files found.[/yellow]")


if __name__ == "__main__":
    main()
