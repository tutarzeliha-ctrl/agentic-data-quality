import requests


def send_slack_alert(webhook_url: str, quality_score: float, total_rows: int, missing_vals: int) -> bool:
    """Post a data quality summary to a Slack incoming webhook.

    Returns True if Slack accepted the message, False otherwise.
    """
    if not webhook_url:
        return False

    status_emoji = "🟢" if quality_score > 90 else "🟡" if quality_score > 75 else "🔴"

    payload = {
        "text": (
            f"{status_emoji} *Data Quality Alert*\n"
            f"• *Quality Score:* `{quality_score:.2f}%`\n"
            f"• *Total Rows:* `{total_rows}`\n"
            f"• *Missing Values:* `{missing_vals}`"
        )
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Slack webhook failed: {e}")
        return False