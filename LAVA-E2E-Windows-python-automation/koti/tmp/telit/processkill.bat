FOR /F "tokens=4 delims= " %%P IN ('netstat -a -n -o ^| findstr :45679') DO @ECHO TaskKill.exe /PID %%P

FOR /F "tokens=4 delims= " %%P IN ('netstat -a -n -o ^| findstr :45679') DO  TaskKill.exe /f /PID %%P