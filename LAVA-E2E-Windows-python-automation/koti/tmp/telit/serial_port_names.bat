@echo off
setlocal

:: wmic /format:list strips trailing spaces (at least for path win32_pnpentity)
for /f "tokens=1* delims==" %%I in ('wmic path win32_pnpentity get caption /format:list ^| find "COM"') do (
    call :setCOM "%%~J"
)

:: display all COM* variables
set COM

:: end main batch
goto :EOF

:setCOM <WMIC_output_line>
:: sets COM#=line
setlocal
set "str=%~1"
set "num=%str:*(COM=%"
set "num=%num:)=%"
set str=%str:(COM=&rem.%
endlocal & set "COM%num%=%str%"
goto :EOF