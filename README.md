# Star-Allele-Search

[![Tests](https://github.com/dianaivanoiu/Star-Allele-Search/actions/workflows/tests.yml/badge.svg)](https://github.com/dianaivanoiu/Star-Allele-Search/actions/workflows/tests.yml)

[![codecov](https://codecov.io/gh/dianaivanoiu/Star-Allele-Search/graph/badge.svg)](https://codecov.io/gh/dianaivanoiu/Star-Allele-Search)

---

This project is a Django web application where the user can search for information about.....

## Installation

### 1. Get the project
Clone the repository and move into its directory 

```bash
git clone https://github.com/dianaivanoiu/Star-Allele-Search.git
cd Star-allele-search
```

This project uses a fully controlled and reproducible Conda environment

### 2. Create the Conda environment

```bash
conda env create -f environment.yml
```

### 3. Activate the environment

```bash
conda activate Star-allele-search
```

### 4. Install the project

```bash
pip install -e .

### 5. To load the webapp, run:

```python
python App/manage.py runserver
```