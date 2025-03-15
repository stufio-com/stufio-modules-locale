# stufio-modules-locale/README.md

# Stufio Modules Locale

## Overview

The `stufio-modules-locale` module provides functionality for managing locales and translations within the Stufio framework. It includes APIs for CRUD operations on locales and translations, migration scripts for MongoDB, and caching mechanisms using Redis.

## Features

- **Locale Management**: Create, read, update, and delete locales.
- **Translation Management**: Manage translations with module name, key, value, locale, and optional details.
- **API Endpoints**: Access locales and translations through RESTful API endpoints.
- **Caching**: Cache translations in Redis for efficient retrieval in public API methods.
- **Migration Scripts**: Initialize MongoDB collections and create default locales.

## Installation

To install the module, include it in your project dependencies. You can do this by adding the following line to your `pyproject.toml`:

```toml
dependencies = [
    "stufio-modules-locale>=0.1.0",
]
```

## Usage

### API Endpoints

- **Locales API**: 
  - `GET /locales`: Retrieve all locales.
  - `POST /locales`: Create a new locale.
  - `GET /locales/{locale_id}`: Retrieve a specific locale.
  - `PUT /locales/{locale_id}`: Update a specific locale.
  - `DELETE /locales/{locale_id}`: Delete a specific locale.

- **Translations API**: 
  - `GET /translations`: Retrieve all translations.
  - `POST /translations`: Create a new translation.
  - `GET /translations/{translation_id}`: Retrieve a specific translation.
  - `PUT /translations/{translation_id}`: Update a specific translation.
  - `DELETE /translations/{translation_id}`: Delete a specific translation.
  - `GET /translations/{locale}`: Retrieve translations by locale.

### Migration Scripts

Migration scripts are executed automatically when the module is initialized. Here's what each script does:

- **v20250501/01_init_collections.py**: Creates the necessary MongoDB collections for locales and translations.
- **v20250501/02_create_indexes.py**: Sets up indexes on locale code and translation keys for optimized query performance.
- **v20250501/03_create_default_locales.py**: Initializes the system with default locales (en-US, fr-FR, de-DE, es-ES).

No manual execution is required as the Stufio framework handles the migration process automatically.

## License

This project is licensed under the MIT License. See the LICENSE.txt file for more details.