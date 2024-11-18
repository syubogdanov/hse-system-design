from pydantic import ValidationError

from src.container import CONTAINER
from src.domain.entities.trigger import Trigger


async def process(event: bytes) -> None:
    """Обработать сообщение."""
    launcher = CONTAINER.task_launcher()
    logger = CONTAINER.logger()

    try:
        logger.info("Validating the event...", extra={"event": event})
        trigger = Trigger.from_bytes(event)

    except ValidationError:
        logger.exception("Failed to validate the event", extra={"event": event})
        return

    try:
        logger.info("Launching the trigger...", extra={"trigger": trigger})
        await launcher.launch(trigger)

    except Exception:
        logger.exception("An unexpected exception occurred", extra={"trigger": trigger})
        return
