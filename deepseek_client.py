"""
deepseek_client.py
------------------
Client utility for generating product descriptions via the DeepSeek API.

The function `generate_product_description` sends a prompt to the DeepSeek
chat-completion endpoint and returns the model's response text.  If the HTTP
request fails for any reason (network error, non-2xx status code, unexpected
response shape, etc.) a safe fallback description is returned instead so that
callers are never left with an empty or error value.
"""

import logging
import os
import json
from typing import Optional

import requests

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration – values are read from environment variables so that no
# credentials are ever hard-coded in source files.
# ---------------------------------------------------------------------------
DEEPSEEK_API_URL: str = os.getenv(
    "DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions"
)
DEEPSEEK_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_TIMEOUT: int = int(os.getenv("DEEPSEEK_TIMEOUT", "15"))


def generate_product_description(name: str, price: float, category: str = "Other") -> str:
    """Generate a short marketing description for a grocery product using DeepSeek.

    Sends the product details to the DeepSeek chat-completion API and returns
    the generated description string.  If the API call fails for any reason the
    function logs the error and returns a sensible fallback description so the
    caller always receives a usable string (HTTP 200 behaviour is preserved).

    Args:
        name:     The product name (e.g. ``"Organic Avocado"``).
        price:    The product price in USD (e.g. ``2.99``).
        category: The product category (e.g. ``"Produce"``).  Defaults to
                  ``"Other"`` when not provided.

    Returns:
        A non-empty description string – either the AI-generated text or a
        pre-defined fallback.
    """
    fallback = (
        f"Enjoy our {name} from the {category} category, "
        f"available at the great price of ${price:.2f}."
    )

    if not DEEPSEEK_API_KEY:
        logger.warning(
            "DEEPSEEK_API_KEY is not set; returning fallback description for '%s'.", name
        )
        return fallback

    prompt = (
        f"Write a short, enticing product description (2-3 sentences) for a grocery store item.\n"
        f"Product name: {name}\n"
        f"Category: {category}\n"
        f"Price: ${price:.2f}\n"
        f"The description should highlight the product's appeal and value."
    )

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "max_tokens": 150,
        "temperature": 0.7,
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=DEEPSEEK_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        description: str = data["choices"][0]["message"]["content"].strip()
        if not description:
            raise ValueError("DeepSeek returned an empty description.")
        return description
    except requests.exceptions.RequestException as exc:
        logger.error("DeepSeek API request failed for product '%s': %s", name, exc)
    except (KeyError, IndexError, ValueError) as exc:
        logger.error(
            "Unexpected DeepSeek API response shape for product '%s': %s", name, exc
        )

    return fallback
