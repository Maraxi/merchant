# Development

## Setup
Make sure to have `python3` and `pipenv` installed.

Install the virtual python environment with all needed packages for development with:
`pipenv shell`
Tests and all other relevant commands should always be run from inside this shell to ensure the needed packages are installed.

Install the package in editable mode with pipenv:
`pipenv install -e .`

Install the pre-commit hooks with:
`pre-commit install`
Code style and correctness will now be checked before every commit.

The unit tests are excluded from pre-commmit hooks but can be run with
`pytest`

Run all tests locally with
`tox`

Tox is also automatically run as a github action on different operating systems after every push.
