@echo off
echo =======================================================
echo  Pushing AI-Expense-Budget-Manager to GitHub
echo  Repository: https://github.com/RaviSingh48/AI-Expense-Budget-Manager
echo =======================================================
echo.

cd /d "%~dp0"

echo Running: git push -u origin main
echo.
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo =======================================================
    echo  [SUCCESS] Successfully pushed to GitHub!
    echo  View your repository at:
    echo  https://github.com/RaviSingh48/AI-Expense-Budget-Manager
    echo =======================================================
) else (
    echo.
    echo =======================================================
    echo  [INFO] If you see an authentication prompt above,
    echo  please sign in with your GitHub account (RaviSingh48)
    echo  or use a GitHub Personal Access Token (PAT).
    echo =======================================================
)

echo.
pause
