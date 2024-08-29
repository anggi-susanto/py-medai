# Makefile

# Variables
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
FLASK_APP := main.py
FLASK := $(PYTHON) -m flask

# Default target
all: run

# Create virtual environment
$(VENV):
	python3 -m venv $(VENV)

# Install dependencies
install: $(VENV)
	$(PIP) install -r requirements.txt

# Run Flask with hot reloading
run: $(VENV)
	FLASK_APP=$(FLASK_APP) FLASK_ENV=development FLASK_DEBUG=1 $(FLASK) run

# Initialize the database (creates migrations directory)
db-init: $(VENV)
	FLASK_APP=$(FLASK_APP) $(FLASK) db init

# Create a new migration
db-migrate: $(VENV)
	FLASK_APP=$(FLASK_APP) $(FLASK) db migrate -m "Migration message"

# Apply migrations
db-upgrade: $(VENV)
	FLASK_APP=$(FLASK_APP) $(FLASK) db upgrade

# Rollback the last migration
db-downgrade: $(VENV)
	FLASK_APP=$(FLASK_APP) $(FLASK) db downgrade

# Clean up environment (optional)
clean:
	rm -rf $(VENV)

# Freeze current dependencies to requirements.txt
freeze:
	$(PIP) freeze > requirements.txt

.PHONY: all install run clean freeze db-init db-migrate db-upgrade db-downgrade