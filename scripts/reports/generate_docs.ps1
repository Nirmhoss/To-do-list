# PowerShell script to generate documentation

$DOCS_DIR = "docs"
$BUILD_DIR = "docs\_build"

Write-Host "===== Генерація документації для проєкту =====" -ForegroundColor Yellow

# Check if Sphinx is installed
try {
    sphinx-build --version | Out-Null
}
catch {
    Write-Host "Помилка: sphinx-build не встановлено." -ForegroundColor Red
    Write-Host "Встановіть його командою: pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints"
    exit 1
}

# Create documentation directory if it doesn't exist
if (-not (Test-Path $DOCS_DIR)) {
    New-Item -ItemType Directory -Path $DOCS_DIR | Out-Null
}

Write-Host "Запуск Sphinx для генерації документації..." -ForegroundColor Yellow

# Check if Sphinx config file exists
if (-not (Test-Path "$DOCS_DIR\conf.py")) {
    Write-Host "Файл conf.py не знайдено. Ініціалізуємо Sphinx..." -ForegroundColor Yellow

    Set-Location $DOCS_DIR
    sphinx-quickstart --no-sep --project="Todo API" --author="Your Name" -v "1.0" --language="uk"
    Set-Location ..

    # Update conf.py to use extensions
    $confAppend = @"

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

# Exclude some warnings
suppress_warnings = ['app.add_node']
"@

    Add-Content -Path "$DOCS_DIR\conf.py" -Value $confAppend
}

# Create modules directory if it doesn't exist
if (-not (Test-Path "$DOCS_DIR\modules")) {
    New-Item -ItemType Directory -Path "$DOCS_DIR\modules" | Out-Null
}

# Create module files if they don't exist
if (-not (Test-Path "$DOCS_DIR\modules\models.rst")) {
    $modelsContent = @"
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
"@
    Set-Content -Path "$DOCS_DIR\modules\models.rst" -Value $modelsContent
}

if (-not (Test-Path "$DOCS_DIR\modules\routes.rst")) {
    $routesContent = @"
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
"@
    Set-Content -Path "$DOCS_DIR\modules\routes.rst" -Value $routesContent
}

if (-not (Test-Path "$DOCS_DIR\modules\utils.rst")) {
    $utilsContent = @"
Utilities
=========

Authentication Utilities
-----------------------

.. automodule:: app.utils.auth
   :members:
   :undoc-members:
   :show-inheritance:
"@
    Set-Content -Path "$DOCS_DIR\modules\utils.rst" -Value $utilsContent
}

# Update index file if needed
$indexContent = Get-Content "$DOCS_DIR\index.rst" -Raw
if (-not ($indexContent -match "modules/models")) {
    $indexContent = $indexContent -replace "Contents:", "Contents:`n`n   modules/models`n   modules/routes`n   modules/utils"
    Set-Content -Path "$DOCS_DIR\index.rst" -Value $indexContent
}

# Generate documentation
Write-Host "Генеруємо HTML документацію..." -ForegroundColor Yellow
sphinx-build -b html $DOCS_DIR $BUILD_DIR

Write-Host "===== Документацію успішно згенеровано в директорії $BUILD_DIR =====" -ForegroundColor Green
Write-Host "Для перегляду документації відкрийте:" -ForegroundColor Yellow
Write-Host "$BUILD_DIR\index.html"