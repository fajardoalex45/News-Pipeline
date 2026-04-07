# News ETL Pipeline - AI Agent Instructions

## Architecture Overview
This is a containerized ETL pipeline that extracts news from NewsAPI, transforms JSON data into clean CSV, and loads into PostgreSQL. The pipeline follows extract-transform-load pattern with intermediate data persistence.

**Key Components:**
- `extract.py`: Fetches news via NewsAPI, saves raw JSON to `data/landing/`
- `transform.py`: Cleans data (flattens nested fields, handles nulls, filters invalid articles), saves CSV to `data/processed/`
- `load.py`: Loads processed CSV into PostgreSQL table `news_articles`
- `main.py`: Orchestrates pipeline with smoke tests at each stage

**Data Flow:**
1. API fetch → `data/landing/*.json`
2. JSON cleaning → `data/processed/cleaned_news.csv`
3. CSV load → PostgreSQL `news_articles` table

## Critical Workflows

### Local Development
- **Environment Setup**: Create `.env` with `NEWS_API_KEY`, `DB_USER`, `DB_PASSWORD`, `DB_HOST=localhost`, `DB_NAME=news_db`, `DB_PORT=5432`
- **Run Pipeline**: `python main.py` (includes smoke tests for API connectivity and DB availability)
- **Run Tests**: `python -m unittest discover tests/` (uses mocking for external API calls)
- **Debug Data**: Check `data/landing/` for raw API responses, `data/processed/` for cleaned CSV

### Containerized Deployment
- **Build & Run**: `docker-compose up --build` (starts Postgres on port 5433, runs ETL pipeline)
- **DB Access**: Connect to `localhost:5433` with credentials from `.env`
- **Volume Persistence**: Postgres data persists in `postgres_data` volume

## Project Conventions

### Error Handling
- **Granular Exceptions**: Catch specific `requests` exceptions (HTTPError, Timeout, ConnectionError) with targeted error messages
- **Smoke Tests**: Always verify connectivity before operations (API in extract, DB in load)
- **Early Returns**: Abort pipeline on failures with descriptive print statements

### Data Processing
- **Null Handling**: Fill `author` with 'Anonymous', `description` with 'No description provided'
- **Date Standardization**: Convert `publishedAt` to `'%Y-%m-%d %H:%M:%S'` format
- **Content Filtering**: Remove articles where `title == "[Removed]"`
- **Source Flattening**: Extract `source['name']` to `source_name` column

### Testing Patterns
- **Mock External Calls**: Use `unittest.mock.patch` for API requests in `test_extract.py`
- **Data-Driven Tests**: Test transformation logic with realistic mock DataFrames
- **File Assertions**: Verify file creation/deletion in persistence tests

### Code Structure
- **Class-Based Design**: Each ETL stage is a class (NewsExtractor, NewsTransformer, NewsLoader)
- **Separation of Concerns**: Extract logic from I/O (e.g., `transform_logic()` method for testable transformations)
- **Path Construction**: Use `os.path.join()` for cross-platform compatibility
- **Intermediate Saves**: Persist data between stages to enable debugging and recovery

## Dependencies & Environment
- **Python 3.12** with packages from `requirements.txt` (includes `psycopg2-binary` for Postgres)
- **PostgreSQL 15** via Docker Compose
- **NewsAPI** integration with rate limiting awareness (429 errors)
- **Docker Build**: Requires system deps (`libpq-dev`, `gcc`) for `psycopg2` compilation

## Key Files for Reference
- `main.py`: Pipeline orchestration and error flow
- `extract.py`: API integration patterns and error handling
- `transform.py`: Data cleaning logic and pandas operations
- `tests/test_extract.py`: Mocking examples for external dependencies
- `docker-compose.yml`: Service dependencies and environment mapping</content>
<parameter name="filePath">/Users/alexfajardo/Developer/news_project_etl/.github/copilot-instructions.md