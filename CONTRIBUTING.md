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

## Versioning and Release Automation

### Bumping the Version

Use Hatch to bump the version automatically. This updates the version in `src/ebo_app_factory/__about__.py`:

- **Patch release (e.g., 0.1.4 → 0.1.5):**
  ```sh
  hatch version patch
  ```
- **Minor release (e.g., 0.1.4 → 0.2.0):**
  ```sh
  hatch version minor
  ```
- **Major release (e.g., 0.1.4 → 1.0.0):**
  ```sh
  hatch version major
  ```
- **Set a specific version:**
  ```sh
  hatch version 0.1.7
  ```

Commit the version bump:

```sh
git add src/ebo_app_factory/__about__.py
git commit -m "Bump version to x.y.z"
```

### GitHub Flow for Automated Release

1. **Push your changes to GitHub:**

   ```sh
   git push origin main
   ```

2. **Tag the new release (replace `x.y.z` with your version):**

   ```sh
   git tag v0.1.5
   git push origin v0.1.5
   ```

3. **GitHub Actions will automatically build and upload the release**  
   (see `.github/workflows/build.yml` for details).

---

## Example Workflow

```sh
git clone https://github.com/clivegross/ebo-app-factory.git
cd ebo-app-factory
pip install hatch
hatch shell
hatch test
hatch build
hatch version patch   # or minor/major
git add src/ebo_app_factory/__about__.py
git commit -m "Bump version to x.y.z"
git push origin main
git tag vX.Y.Z
git push origin vX.Y.Z
```

---

# License

`ebo-app-factory` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
