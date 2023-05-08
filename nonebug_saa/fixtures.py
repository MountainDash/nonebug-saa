from typing import Optional

import pytest
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def saa_patch(mocker: MockerFixture):
    from nonebot.adapters import Bot, Event
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
