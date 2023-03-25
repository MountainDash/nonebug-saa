from typing import Optional

from nonebot.adapters import Bot, Event
from nonebug.mixin.call_api import ApiContext

from nonebot_plugin_saa import MessageFactory, PlatformTarget, extract_target


def should_send_saa(
    ctx: ApiContext,
    msg: MessageFactory,
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
