import py_compile
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
}


def _iter_python_files(root):
    for path in sorted(root.rglob("*.py")):
        relative_parts = path.relative_to(root).parts
        if any(part in SKIP_DIRS for part in relative_parts):
            continue
        yield path


def main():
    paths = list(_iter_python_files(REPO_ROOT))
    if not paths:
        print("No Python files found.")
        return 1

    with tempfile.TemporaryDirectory(prefix="noesis-pycompile-") as tmpdir:
        tmpdir_path = Path(tmpdir)
        for index, path in enumerate(paths):
            relative_path = path.relative_to(REPO_ROOT)
            cfile = tmpdir_path / f"{index}.pyc"
            py_compile.compile(str(path), cfile=str(cfile), doraise=True)
            print(f"checked {relative_path}")

    print(f"checked {len(paths)} Python files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
