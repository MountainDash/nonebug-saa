from typing import Optional

import pytest
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def saa_patch(mocker: MockerFixture):
    import nonebot
    from nonebot.adapters import Bot, Event
    from nonebot_plugin_saa.utils import auto_select_bot
    from nonebot_plugin_saa import (
        MessageFactory,
        PlatformTarget,
        AggregatedMessageFactory,
    )

    async def _do_send_ms_fact(
        self: MessageFactory,
        bot: Bot,
        target: PlatformTarget,
        event: Optional[Event],
        at_sender: bool,
        reply: bool,
    ):
        await bot.call_api(
            "_saa_send_msg",
            message_factory=self,
            target=target,
            event=event,
            at_sender=at_sender,
            reply=reply,
        )

    mocker.patch.object(MessageFactory, "_do_send", _do_send_ms_fact)

    async def _do_send_aggregate(
        self: AggregatedMessageFactory,
        bot: Bot,
        target: PlatformTarget,
        event: Optional[Event],
    ):
        await bot.call_api(
            "_saa_send_aggreagated_msg",
            aggregated_message_factory=self,
            target=target,
            event=event,
        )

    mocker.patch.object(AggregatedMessageFactory, "_do_send", _do_send_aggregate)

    raw_get_bot = auto_select_bot.get_bot

    def _get_bot(target: PlatformTarget) -> Bot:
        all_bots = list(nonebot.get_bots().values())
        if len(all_bots) == 1 and all_bots[0].adapter.get_name() == "fake":
            return all_bots[0]
        return raw_get_bot(target)

    mocker.patch("nonebot_plugin_saa.utils.types.get_bot", _get_bot)
