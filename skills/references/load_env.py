"""
Shared .env loader for all 42: Python scripts.

Searches for .env in this order (first match wins per key):
1. 42-reports/<domain>/.env  (if domain specified)
2. 42-reports/.env           (project-wide reports config)
3. Current working directory (./.env)
4. Output root (references/../.env)
5. Home config (~/.config/42-seo/.env)
6. Legacy seo-agi config (~/.config/seo-agi/.env)

All found .env files are loaded. Later files only fill in MISSING keys
(they never override earlier values or existing shell env vars).

Usage in any 42: script:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "references"))
    from load_env import load_env
    load_env()
    # Now os.environ has all keys from .env

With domain-specific loading:
    load_env(domain="example-com")
    # Also loads 42-reports/example-com/.env
"""

import os
from pathlib import Path


def _find_reports_root() -> Path | None:
    """Find the 42-reports/ directory relative to this file or cwd."""
    # From references/ → output/42-reports/
    candidates = [
        Path(__file__).resolve().parent.parent / "42-reports",
        Path.cwd() / "42-reports",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return None


def _load_single_env(env_file: Path, loaded: dict, verbose: bool = False) -> dict:
    """Load a single .env file, only filling missing keys."""
    new_keys = {}

    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Parse KEY=VALUE
            if "=" not in line:
                continue

            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()

            # Remove surrounding quotes
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]

            # Don't override existing env vars or previously loaded keys
            if key and key not in os.environ and key not in loaded:
                os.environ[key] = value
                loaded[key] = value
                new_keys[key] = value

    if verbose and new_keys:
        import sys
        print(f"  Loaded {len(new_keys)} keys from {env_file}: {', '.join(new_keys.keys())}", file=sys.stderr)

    return new_keys


def load_env(domain: str | None = None, verbose: bool = False) -> dict[str, str]:
    """Load .env files into os.environ. Returns dict of all loaded keys.

    Does NOT override existing environment variables — env vars set in the
    shell take precedence over .env file values. This matches the standard
    dotenv convention.

    Multi-file loading: all found .env files are loaded in priority order.
    Later files only fill in keys that are still missing.

    Args:
        domain: Optional domain slug (e.g., "example-com") to also load
                42-reports/<domain>/.env
        verbose: Print loading details to stderr
    """
    reports_root = _find_reports_root()

    # Build search paths in priority order (highest first)
    search_paths = []

    if domain and reports_root:
        search_paths.append(reports_root / domain / ".env")

    if reports_root:
        search_paths.append(reports_root / ".env")

    search_paths.extend([
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent / ".env",  # output/.env
        Path.home() / ".config" / "42-seo" / ".env",
        Path.home() / ".config" / "seo-agi" / ".env",     # legacy
    ])

    if verbose:
        import sys
        print("Searching for .env files:", file=sys.stderr)
        for p in search_paths:
            exists = "exists" if p.is_file() else "not found"
            print(f"  {p} ({exists})", file=sys.stderr)

    loaded = {}

    for path in search_paths:
        if path.is_file():
            _load_single_env(path, loaded, verbose=verbose)

    if verbose:
        import sys
        if loaded:
            print(f"Total: {len(loaded)} env vars loaded", file=sys.stderr)
        else:
            print("No .env files found.", file=sys.stderr)

    return loaded


# Auto-load when imported (backwards compatible, without domain)
_loaded = load_env()
