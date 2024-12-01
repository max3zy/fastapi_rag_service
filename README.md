# rag-service

Разработка предполагается исключительно на `Linux`


Как развернуть приложение?

1. Install `pyenv`
```bash
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

exec "$SHELL"
```


2. Установка необходимой версии python 3.9.13
```bash
pyenv install 3.9.13
```

3. Создание окружения
Для единообразия и простоты предлагается называть окружение в pyenv,
так же как и сам сервис
```bash
make venv
```

4. Активация созданного окружения make не хочет обновлять консоль, 
поэтому активацию приходится делать отдельной командой
```bash
pyenv activate 
```

5. Проверка версии питона
```bash
make check-python-version
```

6. Установка poetry (установка всех зависимостей будет происходить через poetry, чтобы было меньше проблем с зависимостями)
Так же запрещаем poetry создавать окружение внутри проекта
Иначе `poetry` будет постоянно намереваться создавать окружение внутри проекта
```bash
make install-poetry
```

7. Установка зависимостей из poetry.lock
```bash
make dep-install
```

8. Обновить версии пакетов
Если какие-то пакеты нужно оставить с определенными версиями, то
    (пример)
`poetry add  "uvicorn==0.17.5"`
а затем, массовое обновление версий библиотек
```bash 
make pkg-upd 
```

9. Генерация зависимостей (requirements.txt/requirements-dev.txt)
```bash 
make gen-req
```

10. Генерация настроек проекта
```bash
make gen-settings
```

11. После всех шагов необходимо добавить в git index
```bash
git add poetry.lock
git add requirements/requirements.txt
git add requirements/requirements-dev.txt 
```

12. Выбрать новосозданный интерпретатор питона из окружения rag_service для работы с проектом

13. Создание `pre-commit` хука
Важно чтобы проект уже версионировался git'ом
```bash
echo "make reformat" > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```