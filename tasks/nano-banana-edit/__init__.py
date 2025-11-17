#region generated meta
import typing
class Inputs(typing.TypedDict):
    image_urls: list[str]
    prompt: str
class Outputs(typing.TypedDict):
    result: typing.NotRequired[dict]
#endregion

from oocana import Context
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import asyncio

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Edit images using Nano Banana AI model via OOMOL Fusion API.

    Args:
        params: Input parameters containing image URLs and prompt
        context: OOMOL execution context

    Returns:
        API response containing the edited image result
    """
    api_url = "https://fusion-api.oomol.com/v1/fal-nano-banana-edit/submit"

    # Get OOMOL token from context (no need for manual API key input)
    api_token = await context.oomol_token()

    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }

    payload = {
        "imageURLs": params["image_urls"],
        "prompt": params["prompt"]
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

    try:
        context.report_progress(10)

        # Retry logic for SSL errors
        for retry_attempt in range(3):
            try:
                response = session.post(
                    api_url,
                    headers=headers,
                    json=payload,
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

        context.report_progress(80)

        response.raise_for_status()

        result = response.json()

        context.report_progress(100)

        return {"result": result}

    except requests.exceptions.RequestException as e:
        error_message = f"API request failed: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                error_message += f"\nDetails: {error_detail}"
            except:
                error_message += f"\nStatus code: {e.response.status_code}"

        raise Exception(error_message)
