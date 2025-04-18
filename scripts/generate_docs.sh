#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

DOCS_DIR="docs"
BUILD_DIR="docs/_build"

echo -e "${YELLOW}===== Генерація документації для проєкту =====${NC}"

# Перевірка наявності Sphinx
command -v sphinx-build >/dev/null 2>&1 || {
  echo -e "${RED}Помилка: sphinx-build не встановлено.${NC}"
  echo -e "Встановіть його командою: pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints"
  exit 1
}

# Створення директорії для документації, якщо вона не існує
mkdir -p ${DOCS_DIR}

echo -e "${YELLOW}Запуск Sphinx для генерації документації...${NC}"

# Перевірка, чи є файл конфігурації Sphinx
if [ ! -f "${DOCS_DIR}/conf.py" ]; then
  echo -e "${YELLOW}Файл conf.py не знайдено. Ініціалізуємо Sphinx...${NC}"
  cd ${DOCS_DIR}
  sphinx-quickstart --no-sep --project="Todo API" --author="Your Name" -v "1.0" --language="uk"
  cd ..

  # Оновлення conf.py для використання розширень
  cat >> ${DOCS_DIR}/conf.py << EOF

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
]

html_theme = 'sphinx_rtd_theme'

autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# Виключення деяких попереджень
suppress_warnings = ['app.add_node']
EOF
fi

# Генерація документації для модулів, якщо вони не існують
mkdir -p ${DOCS_DIR}/modules

# Створення файлів для модулів, якщо вони не існують
if [ ! -f "${DOCS_DIR}/modules/models.rst" ]; then
  cat > ${DOCS_DIR}/modules/models.rst << EOF
Models
======

User Model
----------

.. automodule:: app.models.user
   :members:
   :undoc-members:
   :show-inheritance:

Todo Model
----------

.. automodule:: app.models.todo
   :members:
   :undoc-members:
   :show-inheritance:
EOF
fi

if [ ! -f "${DOCS_DIR}/modules/routes.rst" ]; then
  cat > ${DOCS_DIR}/modules/routes.rst << EOF
Routes
======

Authentication Routes
--------------------

.. automodule:: app.routes.auth
   :members:
   :undoc-members:
   :show-inheritance:

Todo Routes
-----------

.. automodule:: app.routes.todos
   :members:
   :undoc-members:
   :show-inheritance:
EOF
fi

if [ ! -f "${DOCS_DIR}/modules/utils.rst" ]; then
  cat > ${DOCS_DIR}/modules/utils.rst << EOF
Utilities
=========

Authentication Utilities
-----------------------

.. automodule:: app.utils.auth
   :members:
   :undoc-members:
   :show-inheritance:
EOF
fi

# Оновлення індексного файлу
if ! grep -q "modules/models" "${DOCS_DIR}/index.rst"; then
  # Додаємо посилання на модулі до індексу
  sed -i '/Contents:/a\\n   modules/models\n   modules/routes\n   modules/utils' ${DOCS_DIR}/index.rst
fi

# Генерація документації
echo -e "${YELLOW}Генеруємо HTML документацію...${NC}"
sphinx-build -b html ${DOCS_DIR} ${BUILD_DIR}

echo -e "${GREEN}===== Документацію успішно згенеровано в директорії ${BUILD_DIR} =====${NC}"
echo -e "${YELLOW}Для перегляду документації відкрийте:${NC}"
echo -e "${BUILD_DIR}/index.html"