import requests
import logger


def send_mailtrap_email(
    to_email: str,
    subject: str,
    text: str = None,
    from_email: str = "hello@digitalace.in",
    from_name: str = "Mailtrap Test",
    category: str = "Integration Test",
) -> dict:
    """
    Send an email using the Mailtrap API.

    Args:
        to_email (str): Recipient email address
        subject (str): Email subject line
        text (str, optional): Email body text. Defaults to None.
        from_email (str, optional): Sender email address. Defaults to "hello@digitalace.in".
        from_name (str, optional): Sender name. Defaults to "Mailtrap Test".
        category (str, optional): Email category. Defaults to "Integration Test".

    Returns:
        dict: API response from Mailtrap
    """
    try:
        url = "https://send.api.mailtrap.io/api/send"

        headers = {
            "Authorization": f"Bearer {'238174090c3100bef072a8186049fcee'}",
            "Content-Type": "application/json",
        }

        payload = {
            "from": {"email": from_email, "name": from_name},
            "to": [{"email": to_email}],
            "subject": subject,
            "text": text or f"Email from {from_name}",
            "category": category,
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        return {"success": True, "response": response.json()}

    except requests.exceptions.RequestException as e:
        logger.error(f"Mailtrap API error: {str(e)}")
        return {"success": False, "error": str(e)}
