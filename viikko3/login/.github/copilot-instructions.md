# Project Guidelines

## Build and Test

- Use Python 3.14 or newer; the required version is declared in `pyproject.toml` and `.python-version`.
- Install or synchronize dependencies with `uv sync`.
- Start the Flask application from the project root with `uv run python src/index.py`. It listens on `http://localhost:5001`.
- The end-to-end tests use Robot Framework Browser and require the application server to be running in another terminal. On a new environment, initialize the browser dependencies with `uv run rfbrowser init`.
- Run all browser tests headlessly with `uv run robot --variable HEADLESS:true src/tests`.
- Run one suite with `uv run robot --variable HEADLESS:true src/tests/login.robot`.
- Run one test case with `uv run robot --variable HEADLESS:true --test "Login With Correct Credentials" src/tests/login.robot`.
- No lint command or linter configuration is defined in `pyproject.toml`.

## Architecture

- `src/index.py` is the development entry point; it imports the Flask app from `src/app.py` and starts it on port 5001.
- `src/app.py` owns HTTP routes, redirects, flashed error messages, and template rendering. The templates in `src/templates/` define the user-facing pages and form field IDs used by the browser tests.
- `src/services/user_service.py` contains validation, registration, and credential-checking rules. It depends on the repository abstraction and raises `UserInputError` or `AuthenticationError` for expected failures.
- `src/repositories/user_repository.py` is an in-memory repository. The module-level `user_repository` and `user_service` instances are shared by the running process, so all data is lost on restart.
- `src/entities/user.py` contains the simple `User` domain object. There is no database or session-based authorization; the login flow redirects to the main page after checking credentials.
- `src/tests/` contains black-box browser suites. `resource.robot` provides shared Browser setup, URLs, and page assertions; `AppLibrary.py` resets application state and seeds users through HTTP.

## Conventions

- Run commands from this project directory so `src/` is the application and test source root.
- Browser tests assume a server at `localhost:5001`, use Chromium, and default to a visible browser with a 500 ms delay. Pass `--variable HEADLESS:true` for CI or unattended runs.
- Each browser test resets the in-memory repository through `POST /tests/reset`; preserve this endpoint's behavior when changing test setup.
- Form failures are handled by catching expected service exceptions in the route handlers, flashing the exception message, and redirecting back to the relevant form.
- When changing form markup, preserve the `id` attributes (`username`, `password`, and `password_confirmation`) and button/link text used as selectors in the Robot suites.
- Keep the service/repository boundary intact: business validation belongs in `UserService`, while storage and duplicate-username checks belong in `UserRepository`.
