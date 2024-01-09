pip install --upgrade build
python -m build
pip install dist/*.whl --force-reinstall
python -c "import ble_hci"
