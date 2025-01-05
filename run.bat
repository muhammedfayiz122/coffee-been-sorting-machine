@echo off

:: Ask if the user has a virtual environment
set /p has_venv="Do you have a virtual environment already set up? (y/n): "
if /i "%has_venv%"=="y" (
    set /p venv_name="Enter the name of your virtual environment folder: "
    if exist "%venv_name%/Scripts/activate.bat" (
        echo Activating the virtual environment: %venv_name%
        call "%venv_name%/Scripts/activate.bat"
    ) else (
        echo Virtual environment not found. Please check the path and try again.
        pause
        exit /b
    )
) else (
    set /p create_venv="Do you want to create a new virtual environment? (y/n): "
    if /i "%create_venv%"=="y" (
        echo Creating a new virtual environment...
        python -m venv venv
        if exist "venv/Scripts/activate.bat" (
            echo Activating the new virtual environment...
            call "venv/Scripts/activate.bat"
        ) else (
            echo Failed to create or locate the virtual environment.
            pause
            exit /b
        )
    ) else (
        echo Skipping virtual environment setup.
    )
)

:: Install dependencies
echo Now installing dependencies...
pip install -r requirements.txt

:: Run the Python script
echo Now running the Python script...
python src/predict.py

pause
