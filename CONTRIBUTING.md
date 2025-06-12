# Contributing

## Development Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/clivegross/ebo-app-factory.git
   cd ebo-app-factory
   ```

2. **Install [Hatch](https://hatch.pypa.io/):**

   ```sh
   pip install hatch
   ```

3. **(Optional) Add Hatch to your PATH** if you see a warning about it not being recognized.

4. **Enter a development shell:**
   ```sh
   hatch shell
   ```
   This will activate a virtual environment with all dependencies installed.

---

## Running Tests

- **Run all tests:**
  ```sh
  hatch test
  ```
  For verbose output:
  ```sh
  hatch test -- -v
  ```
- **Run a specific test file:**

  ```sh
  hatch test -- tests/test_modbus_builder.py
  ```

- **See print output in tests:**
  ```sh
  hatch test -- -s
  ```

---

## Building the Package

- **Build a distributable package (wheel and sdist):**
  ```sh
  hatch build
  ```
  The built files will appear in the `dist/` directory.

---

## Installing Locally for Development

- **Install the package in "editable" mode:**
  ```sh
  pip install -e .
  ```
  Or, from within a Hatch shell:
  ```sh
  hatch shell
  pip install -e .
  ```

---

## Formatting and Linting

If you use tools like `black`, `ruff`, or `flake8`, add them to your `pyproject.toml` and run them via Hatch:

```sh
hatch run black src/ tests/
hatch run ruff src/ tests/
```

---

## Example Workflow

```sh
git clone https://github.com/clivegross/ebo-app-factory.git
cd ebo-app-factory
pip install hatch
hatch shell
hatch test
hatch build
```

---

# License

`ebo-app-factory` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
