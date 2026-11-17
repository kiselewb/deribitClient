import aiohttp
from decimal import Decimal
from app.config import settings


class DeribitClientError(Exception):
    pass


class DeribitClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.DERIBIT_API_URL

    async def get_index_price(self, currency: str) -> Decimal:
        endpoint = f"{self.base_url}/public/get_index_price"
        params = {"index_name": currency}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, params=params) as response:
                    if response.status != 200:
                        raise DeribitClientError(
                            f"Deribit API returned status {response.status}"
                        )

                    data = await response.json()

                    if "error" in data:
                        error_msg = data["error"].get("message", "Unknown error")
                        raise DeribitClientError(f"Deribit API error: {error_msg}")

                    if "result" not in data or "index_price" not in data["result"]:
                        raise DeribitClientError(
                            "Invalid response structure from Deribit API"
                        )

                    index_price = data["result"]["index_price"]

                    return Decimal(str(index_price))

        except aiohttp.ClientError as e:
            raise DeribitClientError(f"Network error while fetching price: {str(e)}")
        except (KeyError, ValueError, TypeError) as e:
            raise DeribitClientError(f"Error parsing Deribit response: {str(e)}")
