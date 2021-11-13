# Development

## Setup
Make sure to have `python3` and `pipenv` installed.

Install virtual python environment with all needed packages for development with:
`pipenv shell`

Inside this environment install the pre-commit hooks with:
`pre-commit install`
With every commit python code style will now be enforced.
The commit hooks may be skipped by running:
`git commit --no-verify`
