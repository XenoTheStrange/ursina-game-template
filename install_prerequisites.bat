@echo off
python -m pip install --upgrade pip
python -m pip install virtualenv
python -m virtualenv assets\.winvenv
call assets\.winvenv\Scripts\activate.bat
python -m pip install ursina
python -m pip install argparse
pause
echo ________________
echo done.