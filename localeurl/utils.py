# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.conf import settings
from localeurl import LOCALE_INDEPENDENT_PATHS

SUPPORTED_LOCALES = dict(settings.LANGUAGES)

def is_locale_independent(path):
    """
    Returns whether the path is locale-independent.

    A path is independent if it starts with MEDIA_URL or it is matched by any
    pattern from LOCALE_INDEPENDENT_PATHS.
    """
    if settings.MEDIA_URL and path.startswith(settings.MEDIA_URL):
        return True
    for path_re in LOCALE_INDEPENDENT_PATHS:
        if path_re.search(path):
            return True
    return False

def strip_locale_prefix(path):
    """
    Returns the path without the locale prefix. If the path does not begin
    with a locale it is returned without change.
    """
    for lang in settings.LANGUAGES:
        locale = '/' + lang[0] + '/'
        if path.startswith(locale):
            return path[len(locale)-1:]
    return path

def get_language(locale):
    """
    Returns the supported language (from settings.LANGUAGES)
    """
    if locale in SUPPORTED_LOCALES:
        return locale
    elif locale[:2] in SUPPORTED_LOCALES:
        return locale[:2]
    else:
        return None