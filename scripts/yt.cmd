@echo off
REM yt — Windows wrapper. Invokes the stdlib-only Python CLI in the same directory.
REM Usage: yt <command> [args...]
setlocal
set "HERE=%~dp0"
python "%HERE%yt.py" %*
endlocal