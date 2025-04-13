@echo off
echo Checking if RCC exists...

IF EXIST "rcc.exe" (
    echo RCC executable already exists. Skipping download.
) ELSE (
    echo Downloading RCC executable...
    curl -o rcc.exe https://downloads.robocorp.com/rcc/releases/v17.18.0/windows64/rcc.exe
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to download RCC executable.
        exit /b 1
    )
    echo RCC downloaded successfully.
)

echo Pulling repository from GitHub...
rcc.exe pull github.com/MaxWindt/zoom-triad-tool

echo Running the tool...
rcc.exe run

echo Process completed.