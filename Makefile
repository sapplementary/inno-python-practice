# Список команд: make help

VENV      := .venv
PYTHON    := $(VENV)/bin/python
ENV_FILE  := .env.local
FORMAT    ?= json
LOG_LEVEL ?= INFO

.PHONY: help install test run clean

help: ## Показать список команд
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "} {printf "  %-10s %s\n", $$1, $$2}'

$(PYTHON):
	python3 -m venv $(VENV)

install: $(PYTHON) ## Создать окружение и установить зависимости
	$(PYTHON) -m pip install -r requirements-dev.txt

test: ## Запустить тесты
	@test -x $(PYTHON) || { echo "Нет окружения: выполните make install"; exit 1; }
	$(PYTHON) -m pytest -v

run: ## Запустить программу: make run FORMAT=json|xml
	@test -x $(PYTHON) || { echo "Нет окружения: выполните make install"; exit 1; }
	@test -f $(ENV_FILE) || { echo "Нет файла $(ENV_FILE): выполните cp .env.example $(ENV_FILE) и заполните его"; exit 1; }
	set -a; . ./$(ENV_FILE); set +a; $(PYTHON) -m src.cli --format $(FORMAT) --log-level $(LOG_LEVEL)

clean: ## Удалить результаты запусков и кэши
	rm -rf output .pytest_cache
	find src tests -name __pycache__ -type d -prune -exec rm -rf {} +