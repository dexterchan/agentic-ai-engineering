.PHONY: init

init:
	uv venv --python 3.12
	source .venv/bin/activate && uv sync && uv pip install -r requirements.txt

.PHONY: run

run:
	uv run python main.py