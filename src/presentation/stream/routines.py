from pydantic import ValidationError

from src.container import CONTAINER
from src.domain.entities.result import Result
from src.domain.entities.trigger import Trigger


async def on_trigger(event: bytes) -> None:
    """Обработать триггер."""
    launcher = CONTAINER.stage_launcher()
    logger = CONTAINER.logger()

    try:
        logger.info("Validating the trigger event...", extra={"event": event})
        trigger = Trigger.from_bytes(event)

    except ValidationError:
        logger.exception("Failed to validate the trigger event", extra={"event": event})
        return

    try:
        logger.info("Launching the trigger event...", extra={"trigger": trigger})
        await launcher.start(trigger)

    except Exception:
        logger.exception("An unexpected exception occurred", extra={"trigger": trigger})
        return


async def on_result(event: bytes) -> None:
    """Обработать результат."""
    launcher = CONTAINER.stage_launcher()
    logger = CONTAINER.logger()

    try:
        logger.info("Validating the result event...", extra={"event": event})
        result = Result.from_bytes(event)

    except ValidationError:
        logger.exception("Failed to validate the result event", extra={"result": result})
        return

    try:
        logger.info("Launching the result event...", extra={"result": result})
        await launcher.resume(result)

    except Exception:
        logger.exception("An unexpected exception occurred", extra={"result": result})
        return
