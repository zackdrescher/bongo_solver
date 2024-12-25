echo "Running ruff:"
ruff check

echo "Running mypy:"
mypy .

echo "Running pytest:"
coverage run -m pytest

echo "Running coverage:"
coverage report