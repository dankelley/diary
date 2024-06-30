python3 setup.py test
python3 setup.py sdist
python3 setup.py bdist_wheel --universal
sudo -H pip3 install dist/diary-0.0.1.tar.gz --upgrade

