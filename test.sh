cd test
nosetests --with-coverage --cover-package app --cover-package test && cd .. && flake8 --exclude build --max-line-length 89 --ignore=F401
