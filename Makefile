UVICORN_CMD = uvicorn $(APP_NAME) --host 0.0.0.0 --port 8000

.PHONY: start restart stop

# Inicia o servidor FastAPI
dev:
	@echo "Iniciando servidor FastAPI em modo de desenvolvimento..."
	fastapi dev ./main.py
	
start:
	@echo "Iniciando servidor FastAPI..."
	$(UVICORN_CMD)

test:
	python -m pytest -W ignore::DeprecationWarning -v

test-async:

coverage:
	rm -r -i -v ./htmlcov
	coverage run -m pytest
	coverage report -m
	coverage html
	python -m http.server 8000 --directory htmlcov

create-jwt:
	@echo "Create JWT Token"
	bash ./scripts/generate_jwt.sh

