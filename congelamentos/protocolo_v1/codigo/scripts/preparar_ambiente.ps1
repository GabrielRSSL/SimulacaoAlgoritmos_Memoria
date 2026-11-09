param([string]$Python = "python")
$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
$lockFile = Join-Path $projectRoot 'requirements-lock.txt'
if (-not (Test-Path -LiteralPath $venvPython)) {
    & $Python -m venv --without-pip (Join-Path $projectRoot '.venv')
    if ($LASTEXITCODE -ne 0) { throw 'Não foi possível criar .venv. Informe -Python com um interpretador instalado.' }
}
& $venvPython -c 'import pip' 2>$null
if ($LASTEXITCODE -eq 0) {
    & $venvPython -m pip install -r $lockFile
} else {
    # O Python empacotado usado neste computador não fornece ensurepip.
    # Seu pip pode instalar diretamente no ambiente local, sem alterar a base.
    & $Python -m pip --python $venvPython install -r $lockFile
}
if ($LASTEXITCODE -ne 0) { throw 'Falha na instalação das dependências.' }
& $venvPython -c 'import sys, pytest, matplotlib; print(sys.version); print("pytest", pytest.__version__); print("matplotlib", matplotlib.__version__)'
if ($LASTEXITCODE -ne 0) { throw 'Falha na verificação do ambiente.' }
