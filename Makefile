PYTHON_VERSION = 3.9.13
VENV_NAME = rag_service
DVC_MODEL_ARTIFACTORY = dvc_models
DOCKER_CONTAINER_LOCAL_NAME = rag_service


venv:
	@echo "Создание виртуального окружения"
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME); \
	pyenv shell $(VENV_NAME); \
	pyenv local $(VENV_NAME)


check-python-version:
	@echo "Проверка версии питона"
	pyenv which python; \
	pyenv which pip


install-poetry:
	@echo "Установка poetry + запрет для poetry создавать внутри виртуальное окружение"
	pip install --upgrade pip poetry; \
	poetry config virtualenvs.create false


dep-install:
	@echo "Установка зависимостей из poetry.lock"
	poetry install


gen-req:
	@echo "Генерация requirements.txt/requirements-dev.txt из poetry"
	mkdir -p requirements; \
	echo "poetry-core>=1.6.1" | tee requirements/requirements.txt requirements/requirements-dev.txt;
# 	echo "--trusted-host nexus3.00.egov.local" >> requirements/requirements.txt
# 	echo "--trusted-host nexus3.00.egov.local" >> requirements/requirements-dev.txt
	poetry export --without-hashes | grep -v "@ file" >> requirements/requirements.txt
	poetry export --with dev --without-hashes | grep -v "@ file" >> requirements/requirements-dev.txt


gen-settings:
	@echo "Генерируем настройки и секреты"
	envsubst < cfg_dev/settings.toml.dev > configs/settings.toml
	envsubst < cfg_dev/.secrets.toml.dev > configs/.secrets.toml

pkg-upd:
	@echo "Обновить версии дефолтных пакетов"
	poetry update

reformat:
	@echo "Переформатирование файлов с кодов, если есть необходимость"
	isort .
	black --line-length 79 .

build:
	@echo "Сборка контейнера $(DOCKER_CONTAINER_LOCAL_NAME)"
	docker build -t $(DOCKER_CONTAINER_LOCAL_NAME) .

up:
	@echo "Подъем контейнера $(DOCKER_CONTAINER_LOCAL_NAME)"
	docker-compose -f docker-compose.local.yml up

docker-connect:
	@echo "Присоединиться к контейнеру $(DOCKER_CONTAINER_LOCAL_NAME) (локально)"
	docker exec -it $(DOCKER_CONTAINER_LOCAL_NAME) sh
