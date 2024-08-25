python -m pip install virtualenv
python -m virtualenv ./assets/.venv
source assets/.venv/bin/activate
python -m pip install --upgrade pip
python -m pip install git+https://github.com/pokepetter/ursina.git
python -m pip install argparse
pause
echo ________________
echo done.
