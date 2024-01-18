set -e
pip3 install --upgrade build 
python3 -m build
pip3 install dist/*.whl --force-reinstall
python3 -c "import max_ble_hci"
set +e