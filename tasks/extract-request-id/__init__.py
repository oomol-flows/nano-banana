#region generated meta
import typing

class Inputs(typing.TypedDict):
    response: dict

class Outputs(typing.TypedDict):
    request_id: str
#endregion

from oocana import Context

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Extract request_id from the API response.

    Args:
        params: Input parameters containing the API response
        context: OOMOL execution context

    Returns:
        The extracted request_id string
    """
    response = params["response"]

    # Extract request_id from response
    # Common field names: sessionID, request_id, requestId, id, task_id
    request_id = (
        response.get("sessionID") or
        response.get("session_id") or
        response.get("request_id") or
        response.get("requestId") or
        response.get("id") or
        response.get("task_id")
    )

    if not request_id:
        raise ValueError(f"Could not find request_id in response. Available keys: {list(response.keys())}")

    return {"request_id": request_id}
