# Linter gitlab-ci
> Скрипт для линтовки gitlab-ci pipelines

#### Использование в терминале
Аргументы

1. `-u API_HOST` - URL хоста гитлаб
    > Дефолтное значение: $GITLAB_LINT_API или https://gitlab.com

2. `-id PROJECT_ID` - id проекта
    > Дефолтное значение: $GITLAB_LINT_PROJECT_ID или 11

3. `-t ACCESS_TOKEN` - ключ доступа
    > Дефолтное значение: $GITLAB_LINT_ACCESS_TOKEN или None

4. `-m MASK_1 MASK_2 ... MASK_n` - маска для фильтрации файлов проекта

    1. `-m *.yml *.md` - будет искать файлы, расположенные **НЕ** в папках, \
    с расширением .yml или .md

    2. `-m src/*.yml` - будет искать только те файлы с раширением .yml, \
    которые расположены **В** папке src

    3. `-m egg/foo/blob.yml Dockerfile` - поиск файла blob.yml, \
    расположенного по пути egg/foo/, **или** Dockerfile

    4. `-m **/*.yml` - поиск **ВСЕХ** файлов .yml

    > Дефолтное значение: $GITLAB_LINT_FILE или \*.yml src/\*.yml
---
Пример запроса:

**`$ python ~/main.py -u https://git.adm.selectel.org -id 11 -t 1234 -m *.yml *.md`**

Пример ответа:

```
.gitlab-ci.yml  Syntax is correct
README.md  Invalid configuration format
```
