# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

# slack mock for uwscli testing

from unittest.mock import MagicMock

FakeApp = MagicMock()
App = MagicMock(return_value = FakeApp)

def mock(fail = False):
	status = {'ok': True}
	if fail:
		status = {'ok': False}
	FakeApp.client.chat_postMessage = MagicMock()
	FakeApp.client.chat_postMessage.return_value = status
