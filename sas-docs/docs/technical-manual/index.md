# Technical Manual

## Introduction

Star-Allele-Search is a pharmacogenomics application developed to retrieve, validate and annotate pharmacogenomic star allele information.

The application integrates information from multiple external resources, including PharmVar and ClinPGx, to provide allele-specific information, phenotype annotations and clinical guideline recommendations.

---

## System Architecture

The software follows a modular architecture.

```text
User Input
     │
     ▼
 Star Allele Search
     │
 ┌───┴─────────┐
 │             │
 ▼             ▼
PharmVar      HGNC
Lookup      Validation
 │             │
 └─────┬───────┘
       ▼
Phenotype Processing
       ▼
Guideline Retrieval
       ▼
Results
```

---

## Project Structure

```text
Star-Allele-Search
│
├── App
│   ├── pharmvar_json.py
│   ├── fetch_guidelines.py
│   ├── clinpgx_summary_annotation.py
│   ├── hgnc_id.py
│   └── vv_validation.py
│
├── tests
│
├── docs
│
├── environment.yaml
├── pyproject.toml
├── requirements.txt
└── README.md
```

### App

Contains application source code.

### tests

Contains automated unit tests and functional tests.

### docs

Contains MkDocs documentation used to generate the project website.

### pyproject.toml

Defines build and package configuration.

### environment.yaml

Defines the Conda environment used during development.

---

## Core Modules

### pharmvar_json.py

Responsible for retrieving star allele information from the PharmVar API.

Main responsibilities include:

- Connecting to PharmVar
- Retrieving allele definitions
- Parsing JSON responses
- Formatting allele information

### fetch_guidelines.py

Responsible for retrieving pharmacogenomic guideline information.

Main responsibilities include:

- Connecting to ClinPGx resources
- Retrieving guideline annotations
- Parsing recommendation data

### clinpgx_summary_annotation.py

Processes ClinPGx annotations and generates structured summaries.

### hgnc_id.py

Validates gene names using HGNC nomenclature.

### vv_validation.py

Performs validation checks on user input prior to processing.

---

## Testing

Automated testing is implemented using PyTest.

Tests are stored in the repository test directory.

### Run Tests

```bash
pytest
```

### Run Coverage

```bash
pytest --cov=App
```

Coverage reports are used to assess the effectiveness of the automated test suite.

Both happy-path and exception handling behaviour are tested.    

---

## Continuous Integration

GitHub Actions is used to automate project testing.

The workflow performs the following tasks:

1. Creates a clean environment.
2. Installs project dependencies.
3. Executes the automated test suite.
4. Generates coverage metrics.
5. Reports build success or failure.

Documentation is automatically deployed using GitHub Pages.

---

## Logging

Logging is used throughout the application to record operational events and errors.

Log levels include:

- DEBUG
- INFO
- WARNING
- ERROR

Logs can be used to troubleshoot API failures and unexpected behaviour.

---

## Exception Handling

The application uses exception handling to ensure failures are reported gracefully.

Examples include:

- Invalid user input
- Network failures
- API errors
- JSON parsing failures

Exceptions are logged to aid debugging and maintenance.