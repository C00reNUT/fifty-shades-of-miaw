format: ## Run Black formatter
	pipenv run black -l 120 fifty_shades

pre-commit:  ## Install checks before commits
	pre-commit install

install:  ## Install dependencies from lockfile
	pipenv install