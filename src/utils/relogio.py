from datetime import datetime, timezone


def agora_utc() -> datetime:
    """Relógio de produção. Injete outra função nos testes."""
    return datetime.now(timezone.utc)
