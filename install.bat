pip install --upgrade build
python -m build
for %%w in (dist\*.whl) do pip install %%w --force-reinstall
python -c "import max_ble_hci"
