#! /bin/bash
coverage run --source=bongo_solver -m pytest -v tests/ && coverage report -m
