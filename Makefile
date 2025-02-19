UVICORN_CMD = uvicorn $(APP_NAME) --host 0.0.0.0 --port 8000

.PHONY: start restart stop

# Inicia o servidor FastAPI
dev:
	@echo "Iniciando servidor FastAPI em modo de desenvolvimento..."
	fastapi dev ./main.py
start:
	@echo "Iniciando servidor FastAPI..."
	$(UVICORN_CMD)