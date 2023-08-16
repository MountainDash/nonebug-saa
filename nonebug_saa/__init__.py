from typing import Union, Optional

from nonebot import require
from nonebot.adapters import Bot, Event
from nonebug.mixin.call_api import ApiContext

require("nonebot_plugin_saa")

from nonebot_plugin_saa import (  # noqa: E402
    MessageFactory,
    PlatformTarget,
    AggregatedMessageFactory,
    extract_target,
)


def should_send_saa(
    ctx: ApiContext,
    msg: Union[MessageFactory, AggregatedMessageFactory],
    bot: Bot,
    *,
    target: Optional[PlatformTarget] = None,
    event: Optional[Event] = None,
    at_sender: bool = False,
    reply: bool = False
):
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
        )
