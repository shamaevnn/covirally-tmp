# Coverally-tmp


## First run
1. Create virtual environment and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements.dev.txt
```
2. Install `pre-commit` hooks
```
pre-commit install-hooks
pre-commit install
```
3. Create `.env` file, don't forget to set proper variables
```
cp .env_example .env
```

## Running locally
1. Run all necessary services
```bash
make services
```
2. Apply migrations
```
make migrate
```
3. Run backend on FastAPI
```
make dev
```
4. Check http://0.0.0.0:80/docs, everything should be OK!


## Tests
```
make run_tests
```

## Linter
```
make format
make lint
```
