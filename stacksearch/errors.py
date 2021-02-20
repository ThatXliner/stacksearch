#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A file defining the errors this might raise"""


class StackSearchBaseError(Exception):
    """The base error type"""


class RecaptchaError(StackSearchBaseError):
    """When StackExchange realizes we are a robot"""


class RateLimitedError(StackSearchBaseError):
    """We got rate limited"""


class HTMLParseError(StackSearchBaseError):
    """We couldn't parse the HTML"""
