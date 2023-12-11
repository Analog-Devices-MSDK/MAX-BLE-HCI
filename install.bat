git pull
pip install --upgrade build
python -m build
pip install dist\*.whl --force-reinstall
pip3 install -r requirements.txt
python3 -c "import ble_test_suite"
