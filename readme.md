# Deribit Client

A FastAPI application for tracking cryptocurrency prices from the Deribit exchange, with prices fetched automatically via Celery.

## Features

- 🔄 Automatic retrieval of cryptocurrency prices every minute (BTC_USD, ETH_USD)
- 📊 Storage of historical price data with Unix timestamps
- 🚀 Fast asynchronous API on FastAPI
- 📈 Price filtering by date range
- 🐳 Full containerisation with Docker Compose
- ✅ Comprehensive unit tests
- 🔧 Database migrations with Alembic

## Technology stack

- **Backend framework**: FastAPI
- **Task queue**: Celery + Redis
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (async)
- **HTTP client**: aiohttp
- **Testing**: pytest + pytest-asyncio
- **Containerisation**: Docker + Docker Compose
- **Migrations**: Alembic

## Architecture

The application follows the principles of a clean, layered architecture:

```
app/
├── api/              # API endpoints and dependencies
├── clients/          # External API clients (Deribit)
├── database/         # Database configuration and manager
├── models/           # SQLAlchemy ORM models
├── repositories/     # Data access layer
├── schemas/          # Pydantic schemas for validation
├── services/         # Business logic layer
├── tasks/            # Tasks and Celery configuration
└── migrations/       # Alembic database migrations
```

## Installation

### 1. Cloning the repository

```bash
git clone <repository-url>
cd deribitClient
```

### 2. Creating an environment file

```bash
cp .env.example .env
```

### 3. Configuring environment variables

Edit the `.env` file if you need to change the default values:

```env
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=crypto_prices

REDIS_HOST=redis
REDIS_PORT=6379

DERIBIT_API_URL=https://www.deribit.com/api/v2

CELERY_BEAT_SCHEDULE_INTERVAL=60
```
## Running the application

### Using Docker Compose

**Building and running all services:**

```bash
docker-compose up -d --build
```

This will start:
- The PostgreSQL database
- The Redis message broker
- Database migrations (the `init` service)
- The FastAPI application (port 8000)
- The Celery worker
- The Celery Beat scheduler

## API Documentation

### Available endpoints

#### 1. Retrieving all prices

Retrieves all stored prices for a specific ticker, with optional filtering.

```http
GET /prices?ticker={TICKER}&limit={LIMIT}&offset={OFFSET}&date_from={DATE}&date_to={DATE}
```

**Query parameters:**
- `ticker` (required): `BTC_USD` or `ETH_USD`
- `limit` (optional): Number of records to return (1–1,000, default: 100)
- `offset` (optional): Number of records to skip (default: 0)
- `date_from` (optional): Date filter (ISO 8601 format)
- `date_to` (optional): Date-to filter (ISO 8601 format)

**Example:**
```bash
curl ‘http://localhost:8000/prices?ticker=BTC_USD&limit=10’
```

**Response:**
```json
{
  ‘data’: [
    {
      ‘id’: 1,
      ‘ticker’: ‘BTC_USD’,
      ‘price’: ‘45230.50’,
      ‘created_at’: ‘2026-01-21T12:00:00Z’
    }
  ],
  ‘total’: 100
}
```

#### 2. Retrieving the latest price

Retrieving the most up-to-date price for a specific ticker.

```http
GET /prices/latest?ticker={TICKER}
```

**Query parameters:**
- `ticker` (required): `BTC_USD` or `ETH_USD`

**Example:**
```bash
curl ‘http://localhost:8000/prices/latest?ticker=BTC_USD’
```

**Response:**
```json
{
  ‘id’: 150,
  ‘ticker’: ‘BTC_USD’,
  ‘price’: ‘45230.50’,
  ‘created_at’: ‘2026-01-21T12:00:00Z’
}
```

#### 3. Creating a price (Manual entry)

Manually adding a price entry.

```http
POST /prices
```

**Request body:**
```json
{
  ‘ticker’: ‘BTC_USD’,
  ‘price’: ‘45230.50’
}
```

**Example:**
```bash
curl -X POST ‘http://localhost:8000/prices’ \
  -H ‘Content-Type: application/json’ \
  -d '{‘ticker’: ‘BTC_USD’, “price”: ‘45230.50’}'
```

**Response:**
```json
{
  ‘id’: 151,
  ‘ticker’: ‘BTC_USD’,
  ‘price’: ‘45230.50’,
  ‘created_at’: ‘2026-01-21T12:01:00Z’
}
```

### Examples of filtering by date

Retrieving prices from a specific date:
```bash
curl ‘http://localhost:8000/prices?ticker=BTC_USD&date_from=2026-01-20T00:00:00Z’
```

Retrieving prices for a range of dates:
```bash
curl ‘http://localhost:8000/prices?ticker=BTC_USD&date_from=2026-01-20T00:00:00Z&date_to=2026-01-21T23:59:59Z’
```

## Solution Design

### 1. Layered Architecture

**Solution**: Implement a clean layered architecture with a clear separation of responsibilities.

**Rationale**:
- **API layer** (`app/api/`): Handles HTTP requests, validation and responses. Controllers remain thin, delegating business logic to services.
- **Service layer** (`app/services/`): Contains business logic and coordinates operations between repositories. Provides a clean interface for the API layer.
- **Repository layer** (`app/repositories/`): Abstracts database operations, making it easier to change data sources or add caching.
- **Models layer** (`app/models/`): Defines the database schema using the SQLAlchemy ORM.
- **Schemas layer** (`app/schemas/`): Uses Pydantic for validating and serialising requests and responses.

**Advantages**:
- Clear separation of responsibilities
- Each layer can be tested independently
- Flexibility to accommodate changes (e.g. changing the database)
- A maintainable and scalable codebase

### 2. The Async/Await Pattern

**Solution**: Use asynchronous programming throughout the application (FastAPI, SQLAlchemy, aiohttp).

**Rationale**:
- FastAPI is built on ASGI (Starlette) and is inherently asynchronous
- Database operations via `asyncpg` provide better performance under concurrent load
- `aiohttp` for non-blocking HTTP requests to the Deribit API
- Celery tasks correctly wrap asynchronous operations

**Benefits**:
- Better resource utilisation and scalability
- Higher throughput for I/O-bound operations
- Non-blocking API endpoints

### 3. Dependency injection

**Solution**: Use FastAPI’s dependency injection system for database sessions and other dependencies.

**Rationale**:
- The `DBManager` context manager encapsulates the session lifecycle
- Dependencies are injected via `Depends()`, simplifying testing
- Automatic transaction management (commit/rollback)

**Implementation**:
```python
async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]
```

**Advantages**:
- Easy to mock dependencies in tests
- Clear separation of concerns
- Automatic resource cleanup

### 4. The Repository Pattern

**Solution**: Implement the Repository pattern to abstract data access.

**Rationale**:
- Encapsulates all database queries within repository classes
- A single source of truth for data operations
- Makes it easier to add caching, logging or change the database

**Example**:
```python
class PricesRepository(BaseRepository):
    async def get_latest(self, ticker: str) -> PriceResponse | None:
        query = (
            select(self.model)
            .where(self.model.ticker == ticker)
            .order_by(self.model.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
```

**Advantages**:
- Testability without a database
- Consistent data access patterns
- Easy to optimise queries in one place

### 5. Storing Unix Timestamps

**Solution**: Store timestamps as Unix timestamps (BigInteger) in the database, and convert them to datetime for API responses.

**Rationale**:
- More efficient storage
- No time zone issues in the database
- Fast comparisons and indexing
- Simple filtering by date ranges

**Implementation**:
```python
created_at: Mapped[int] = mapped_column(
    BigInteger,
    server_default=func.extract(‘epoch’, func.now()).cast(BigInteger),
    nullable=False,
)
```

**Schema conversion**:
```python
@field_validator(‘created_at’, mode="before")
@classmethod
def convert_unix_to_datetime(cls, v):
    if isinstance(v, int):
        return datetime.fromtimestamp(v, tz=timezone.utc)
    return v
```

**Advantages**:
- Storage independent of time zones
- Efficient indexing and filtering
- Consistent representation across different systems

### 6. Celery with Redis

**Solution**: Use Celery with Redis as a message broker and results backend for periodically fetching prices.

**Rationale**:
- Celery Beat ensures reliable scheduling of periodic tasks
- Redis is lightweight, fast and well-suited to this use case
- Separation of responsibilities: the API handles requests, whilst Celery handles background tasks
- Tasks can be retried in the event of failures

**Configuration**:
```python
celery_app.conf.beat_schedule = {
    ‘fetch-crypto-prices-every-minute’: {
        ‘task’: ‘app.tasks.tasks.fetch_and_save_prices’,
        ‘schedule’: settings.CELERY_BEAT_SCHEDULE_INTERVAL,
    },
}
```

**Advantages**:
- Reliable task scheduling
- Independent scaling of the API and workers
- Built-in retry mechanism
- Task monitoring and management

### 7. Null Pool for Celery tasks

**Solution**: Use `NullPool` for the SQLAlchemy engine in Celery tasks.

**Rationale**:
- Celery workers are long-running processes
- Connection pooling can cause issues with stale connections
- Each task creates a fresh connection, preventing connection leaks

**Implementation**:
```python
engine_null_pool = create_async_engine(
    url=settings.DB_URL, poolclass=NullPool, echo=False
)
async_session_maker_null_pool = async_sessionmaker(
    bind=engine_null_pool, expire_on_commit=False
)
```

**Advantages**:
- No issues with stale connections
- Predictable resource usage
- Simpler connection lifecycle