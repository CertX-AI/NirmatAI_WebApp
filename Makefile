###########
# Commands#
###########

# Create directories and run the Ansible playbook with the specified environment variables
run:
	mkdir -p htmlcov
	ansible-playbook webapp_config.yml \
	-e "container_state=started"

run-dev:
	mkdir -p htmlcov
	ansible-playbook webapp_config.yml \
	-e "container_state=started" \
	-e "development_config_only=true"

# Stop the Ansible playbook and set the container state to 'absent'
stop:
	@echo "Stopping the playbook..."
	ansible-playbook webapp_config.yml \
	-e "container_state=absent"

##########
# Checks #
##########

# Ensures the podman container named dev exists.
# If not, prompts the user to create it.
dev-exists:
	@echo "Checking that the container dev exists..."
	@podman container exists dev || \
	(echo "Container dev does not exist. Please create it." && exit 1)
	@echo "Container dev exists."


# Ensures the podman container named dev is running.
# If not running, attempts to start the container, then checks again.
dev-running:
	@echo "Checking that the container dev is running..."
	@podman container exists dev || (echo "Container dev does not exist. Please create it." && exit 1)
	@podman container inspect dev | jq -r '.[0].State.Status' | grep running || (echo "Container dev is not running. Please start it." && exit 1)
	@echo "Container dev is running."

#####################
# Linting and Tests #
#####################

# Runs ansible-lint inside the dev container.
ansible-lint:
	@echo "Running ansible-lint..."
	@podman exec dev ansible-lint -v webapp_config.yml

# Runs ruff for linting Python code inside the dev container.
format-check:
	@echo "Running ruff-lint..."
	@podman exec dev ruff check

# Runs ruff for linting Python code inside the dev container.
format-check-fix:
	@echo "Running ruff-lint..."
	@podman exec dev ruff check --fix

# Runs mypy for type checking inside the dev container.
type-check:
	@echo "Running mypy"
	@podman exec dev mypy .

##################
# Documentation  #
##################

# Builds Sphinx documentation inside the $(POD_NAME)_dev container.
build-docs:
	@echo "Building documentation..."
	@podman exec dev sphinx-build docs/source docs/build

##############
# Unit Tests #
##############

test-check:
	@echo "Running unit tests..."
	@podman exec dev python -m pytest nirmatai_webapp

test-coverage-check:
	@echo "Running unit tests with coverage report..."
	@podman exec dev python -m pytest nirmatai_webapp --cov-report=html

##############
# Pre-commit #
##############

# Runs all pre-commit hooks across all files.
pre-commit:
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files
