.PHONY: init

init:
	uv venv --python 3.12
	uv pip compile pyproject.toml --output-file requirements.txt
	source .venv/bin/activate && uv sync && uv pip install -r requirements.txt

.PHONY: run

run:
	uv run python main.py