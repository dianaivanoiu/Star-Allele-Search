# Local Installation

This guide explains how to install and run Star-Allele-Search in a local development environment.

---

## Prerequisites

Ensure the following software is installed:

- Python 3.12
- Git
- Conda (recommended)

Verify your installation:

```bash
python --version
git --version
conda --version
```

---

## Clone the Repository

Clone the repository and move into the project directory:

```bash
git clone https://github.com/dianaivanoiu/Star-Allele-Search.git
cd Star-Allele-Search
```

---

## Create the Conda Environment

Star-Allele-Search provides an environment configuration file to ensure reproducible installation.

Create the environment:

```bash
conda env create -f environment.yaml
```

Activate the environment:

```bash
conda activate Star-allele-search
```

---

## Install Project Dependencies

Install the package in the current environment:

```bash
pip install .
```

The installation uses the project configuration defined in:

```text
pyproject.toml
```

Dependencies are automatically loaded from:

```text
requirements.txt
```

---

## Configure Environment Variables

Several external services require authentication credentials.

Create a file called:

```text
.env
```

in the project root directory.

Example:

```text
PHARMVAR_API_KEY=your_pharmvar_api_key

TERRACIPHER_EMAIL=your_email@example.com
TERRACIPHER_PASSWORD=your_password
```

### Environment Variables

| Variable | Purpose |
|-----------|-----------|
| PHARMVAR_API_KEY | Access to the PharmVar API |
| TERRACIPHER_EMAIL | TerraCipher login email |
| TERRACIPHER_PASSWORD | TerraCipher login password |

The application automatically loads these values using the `python-dotenv` package.

---

## Verify Installation

Confirm that the package can be imported successfully:

```bash
python
```

```python
import star_allele_search
```

Exit Python:

```python
exit()
```

---

## Running Tests

Execute the automated test suite:

```bash
pytest
```

Run tests with coverage analysis:

```bash
pytest --cov=App --cov-report=term-missing --cov-report=html
```

Coverage reports will be written to:

```text
htmlcov/
```

---

## Troubleshooting

### Missing PharmVar API Key

Example error:

```text
401 Unauthorized
```

Verify:

```text
PHARMVAR_API_KEY
```

has been configured correctly in the `.env` file.

---

### Missing TerraCipher Credentials

Example error:

```text
Please set login details to terra
```

Verify:

```text
TERRACIPHER_EMAIL
TERRACIPHER_PASSWORD
```

are present in the `.env` file.

---

### Dependency Installation Issues

Upgrade pip and reinstall dependencies:

```bash
pip install --upgrade pip
pip install .
```

---

## Installed Package Structure

The project is packaged as:

```text
star_allele_search
```

and is built using modern Python packaging through:

```text
pyproject.toml
```

This allows installation using:

```bash
pip install .
```

which provides a reproducible environment across development platforms.