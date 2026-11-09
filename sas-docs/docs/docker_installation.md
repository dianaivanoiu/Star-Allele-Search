# Docker Installation

## Prerequisites

- Docker Desktop or Docker Engine

Verify installation:

```bash
docker --version
```

## Clone Repository

```bash
git clone https://github.com/dianaivanoiu/Star-Allele-Search.git
cd Star-Allele-Search
```

## Build Image

```bash
docker build -t star-allele-search .
```

## Run Container

```bash
docker run \
  --env-file .env \
  star-allele-search
```

## Verify Container

```bash
docker ps
```

The container should appear in the list of running containers.