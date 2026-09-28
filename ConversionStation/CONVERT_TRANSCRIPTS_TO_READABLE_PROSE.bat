@echo off
setlocal
pushd "%~dp0"

set "PYTHON=%CD%\.venv\Scripts\python.exe"
set "CONVERTER=%CD%\ReadableProseConverter\readable_prose_converter.py"

if not exist "%PYTHON%" (
  echo [Readable Prose] ConversionStation is not set up yet.
  echo Run SETUP.bat first.
  popd
  exit /b 1
)

if not exist "%CONVERTER%" (
  echo [Readable Prose] Converter not found: %CONVERTER%
  popd
  exit /b 1
)

set "SOURCE=%~1"
if not defined SOURCE set /p "SOURCE=Transcript library folder: "
if not exist "%SOURCE%" (
  echo [Readable Prose] Source folder not found: %SOURCE%
  popd
  exit /b 1
)

set "OUTPUT=%~2"
if not defined OUTPUT set "OUTPUT=%CD%\Workspace\READABLE_PROSE"

echo.
echo [Readable Prose] Source: %SOURCE%
echo [Readable Prose] Output: %OUTPUT%
echo [Readable Prose] Local punctuation: enabled
echo.

"%PYTHON%" -u "%CONVERTER%" --src "%SOURCE%" --out "%OUTPUT%" --punctuate
set "RESULT=%ERRORLEVEL%"

if not "%RESULT%"=="0" (
  echo.
  echo [Readable Prose] Conversion failed with exit code %RESULT%.
) else (
  echo.
  echo [Readable Prose] Complete: %OUTPUT%
)

popd
exit /b %RESULT%
