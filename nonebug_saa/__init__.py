from typing import TYPE_CHECKING, Optional, Union

from nonebot import require
from nonebot.adapters import Bot, Event
from nonebug.mixin.call_api import ApiContext

if TYPE_CHECKING:
    from nonebot_plugin_saa import (
        AggregatedMessageFactory,
        MessageFactory,
        PlatformTarget,
    )


def should_send_saa(
    ctx: ApiContext,
    msg: Union["MessageFactory", "AggregatedMessageFactory"],
    bot: Bot,
    *,
    target: Optional["PlatformTarget"] = None,
    event: Optional[Event] = None,
    at_sender: bool = False,
    reply: bool = False,
    exception: Optional[Exception] = None,
):
    require("nonebot_plugin_saa")

    from nonebot_plugin_saa import MessageFactory, extract_target

    if not target and not event:
        raise RuntimeError("either target or event should be supplied")
    if not target:
        assert event
        target = extract_target(event)
    if isinstance(msg, MessageFactory):
        ctx.should_call_api(
            "_saa_send_msg",
            {
                "message_factory": msg,
                "target": target,
                "event": event,
                "at_sender": at_sender,
                "reply": reply,
            },
            None,
            exception,
        )
    else:
        ctx.should_call_api(
            "_saa_send_aggreagated_msg",
            {
                "aggregated_message_factory": msg,
                "target": target,
                "event": event,
            },
            None,
            exception,
        )
