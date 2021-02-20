#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The errors StackSearch may raise are"""


class StackSearchBaseError(Exception):
    """The base error type for StackSearch errors."""


class RecaptchaError(StackSearchBaseError):
    """When StackExchange realizes we are a robot."""


class RateLimitedError(StackSearchBaseError):
    """We got rate limited."""


class HTMLParseError(StackSearchBaseError):
    """I couldn't parse the HTML."""
