# -*- coding: utf-8 -*-

import pytest

import codecli.utils


@pytest.fixture
def input(monkeypatch):
    def input(prompt, pattern=r'.*', default=''):
        return default

    monkeypatch.setattr(codecli.utils, 'input', input)
