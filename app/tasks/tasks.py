import asyncio
import logging

from app.tasks.celery_app import celery_app
from app.clients.deribit_client import DeribitClient, DeribitClientError
from app.database.database import async_session_maker_null_pool
from app.repositories.prices import PricesRepository
from app.schemas.prices import PriceCreate


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@celery_app.task(
    name="app.tasks.tasks.fetch_and_save_prices",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def fetch_and_save_prices(self):
    try:
        asyncio.run(_fetch_and_save_prices_async())
    except Exception as exc:
        logger.error(f"Task failed: {exc}", exc_info=True)
        raise self.retry(exc=exc)


async def _fetch_and_save_prices_async():
    client = DeribitClient()

    try:
        logger.info("Fetching prices from Deribit API...")
        btc_price = await client.get_index_price("btc_usd")
        eth_price = await client.get_index_price("eth_usd")

        logger.info(f"✓ Fetched - BTC: ${btc_price:,.2f}, ETH: ${eth_price:,.2f}")

        async with async_session_maker_null_pool() as session:
            repository = PricesRepository(session)

            await repository.add(PriceCreate(ticker="BTC_USD", price=btc_price))
            await repository.add(PriceCreate(ticker="ETH_USD", price=eth_price))

            await session.commit()

        logger.info("✓ Successfully saved prices to database")

    except DeribitClientError as e:
        logger.error(f"✗ Deribit API error: {e}")
        raise
    except Exception as e:
        logger.error(f"✗ Database error: {e}")
        raise
