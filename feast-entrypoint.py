import os
import re
import sys
from pathlib import Path


REPO = Path("/opt/feast/feature_repo")
TEMPLATE = REPO / "feature_store.yaml.template"
OUTPUT = REPO / "feature_store.yaml"
PLACEHOLDER = re.compile(r"\$\{([A-Z][A-Z0-9_]*)\}")


def render_config() -> None:
    template = TEMPLATE.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        value = os.environ.get(name)
        if not value:
            raise SystemExit(f"Required environment variable {name} is not set")
        return value

    OUTPUT.write_text(PLACEHOLDER.sub(replace, template), encoding="utf-8")


if __name__ == "__main__":
    render_config()
    os.execvp(sys.argv[1], sys.argv[1:])
