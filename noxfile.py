import nox

nox.options.sessions = ["lint"]


PYTHON_VERSIONS = ["3.9"]


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    session.install(".[lint]")
    session.run("ruff", "check")


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    session.install(".[test]")
    session.run("pytest", "--cov=file_manager", "tests/")
