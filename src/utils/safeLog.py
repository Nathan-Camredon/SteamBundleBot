import re

_SECRET_PARAM = re.compile(r"(key|token|api_key)=[^&\s'\"]+", re.IGNORECASE)
_WEBHOOK = re.compile(r"(https://discord(?:app)?\.com/api/webhooks/)\S+", re.IGNORECASE)


def redact(message: object) -> str:
    """
    Masque les secrets (clé API Steam, token de webhook Discord) dans un message
    avant de l'afficher dans les logs.
    """
    text = str(message)
    text = _SECRET_PARAM.sub(r"\1=***", text)
    return _WEBHOOK.sub(r"\1***", text)
