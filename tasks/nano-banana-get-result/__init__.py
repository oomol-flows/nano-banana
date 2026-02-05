#region generated meta
import typing
class Inputs(typing.TypedDict):
    session_id: str
    poll_interval: int | None
    max_attempts: int | None
class Outputs(typing.TypedDict):
    images: typing.NotRequired[list[str]]
#endregion

from oocana import Context
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import asyncio

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Retrieve the result of a Nano Banana image editing request with polling.

    Args:
        params: Input parameters containing the request ID and polling config
        context: OOMOL execution context

    Returns:
        API response containing the edited image result and status
    """
    session_id = params["session_id"]
    poll_interval = params.get("poll_interval") or 3
    max_attempts = params.get("max_attempts") or 60

    api_url = f"https://fusion-api.oomol.com/v1/fal-nano-banana/result/{session_id}"

    # Get OOMOL token from context
    api_token = await context.oomol_token()

    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }

    # Configure session with retry strategy for SSL and connection errors
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    attempt = 0

    try:
        while attempt < max_attempts:
            attempt += 1
            progress = min(10 + (attempt / max_attempts * 85), 95)
            context.report_progress(int(progress))

            # Retry logic for SSL errors
            for retry_attempt in range(3):
                try:
                    response = session.get(
                        api_url,
                        headers=headers,
                        timeout=60.0
                    )
                    break
                except requests.exceptions.SSLError as ssl_error:
                    if retry_attempt < 2:
                        # Wait before retrying on SSL error
                        await asyncio.sleep(1 * (retry_attempt + 1))
                        continue
                    else:
                        raise ssl_error

            response.raise_for_status()
            result = response.json()

            # Check if processing is complete
            state = result.get("state", "")

            # If completed or failed, extract and return image URLs
            if state in ["completed", "success", "failed", "error"]:
                context.report_progress(100)
                # Extract image URLs from result.data.images
                images_data = result.get("data", {}).get("images", [])
                image_urls = [img.get("url") for img in images_data if img.get("url")]
                return {"images": image_urls}

            # If still processing, wait and retry
            if state == "processing":
                if attempt < max_attempts:
                    await asyncio.sleep(poll_interval)
                continue

            # Unknown state, try to extract images anyway
            context.report_progress(100)
            images_data = result.get("data", {}).get("images", [])
            image_urls = [img.get("url") for img in images_data if img.get("url")]
            return {"images": image_urls}

        # Max attempts reached
        raise Exception(f"Polling timeout: Maximum attempts ({max_attempts}) reached. Last state: {result.get('state', 'unknown')}")

    except requests.exceptions.RequestException as e:
        error_message = f"API request failed: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                error_message += f"\nDetails: {error_detail}"
            except:
                error_message += f"\nStatus code: {e.response.status_code}"

        raise Exception(error_message)
