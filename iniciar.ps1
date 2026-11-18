$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
function Check-Exit { if ($LASTEXITCODE -ne 0) { throw 'Falló el comando anterior. Revisa el mensaje.' } }
if (!(Test-Path '.venv/Scripts/python.exe')) { py -3 -m venv .venv; Check-Exit }
& ./.venv/Scripts/python.exe -m pip install -r requirements.txt
Check-Exit
& ./.venv/Scripts/python.exe manage.py migrate
Check-Exit
& ./.venv/Scripts/python.exe manage.py crear_roles
Check-Exit
& ./.venv/Scripts/python.exe manage.py runserver
Check-Exit
