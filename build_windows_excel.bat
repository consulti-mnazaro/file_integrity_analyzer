@echo off
REM Build Script para Windows - Verificador com Excel
REM Execute este script no ambiente Windows

echo BUILD VERIFICADOR INTEGRIDADE - VERSAO EXCEL WINDOWS
echo =====================================================

echo.
echo 📦 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado! Instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

echo ✅ Python encontrado

echo.
echo 📦 Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: pip nao encontrado!
    pause
    exit /b 1
)

echo ✅ pip encontrado

echo.
echo 📦 Instalando dependências básicas...
pip install pyinstaller
if errorlevel 1 (
    echo ERRO: Falha ao instalar PyInstaller
    pause
    exit /b 1
)

echo ✅ PyInstaller instalado

echo.
echo 📦 Instalando dependências Excel (opcionais)...
pip install pandas openpyxl
REM Não falhar se Excel deps não instalarem
echo ✅ Dependências Excel processadas

echo.
echo 🔧 Criando executável...
pyinstaller --onefile --name="VerificadorIntegridade_Excel" --icon=NONE verificador_interativo.py

if errorlevel 1 (
    echo ERRO: Falha ao criar executavel
    pause
    exit /b 1
)

echo ✅ Executável criado!

echo.
echo 📂 Localizando arquivos...
if exist "dist\VerificadorIntegridade_Excel.exe" (
    echo ✅ Executável: dist\VerificadorIntegridade_Excel.exe
    
    REM Copiar arquivos adicionais
    if not exist "dist\extras" mkdir "dist\extras"
    if exist "script.py" copy "script.py" "dist\extras\"
    if exist "README.md" copy "README.md" "dist\extras\"
    if exist "EXCEL_FEATURES.md" copy "EXCEL_FEATURES.md" "dist\extras\"
    
    echo ✅ Arquivos extras copiados para dist\extras\
) else (
    echo ERRO: Executavel nao encontrado!
    pause
    exit /b 1
)

echo.
echo BUILD CONCLUIDO COM SUCESSO!
echo.
echo 📁 Arquivo executável: dist\VerificadorIntegridade_Excel.exe
echo 📁 Arquivos extras: dist\extras\
echo.
echo ⚠️  IMPORTANTE: Este executável inclui auto-instalação de Excel dependencies
echo    Se Excel analysis falhar, o programa automaticamente tentará instalar pandas
echo.
pause
