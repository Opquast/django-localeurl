# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django import template
from django.template import Node, Token, TemplateSyntaxError
from django.template import resolve_variable, defaulttags
from django.template.defaultfilters import stringfilter
from django.conf import settings
from django.utils import translation
import localeurl
from localeurl.utils import strip_locale_prefix, get_language

register = template.Library()


def chlocale(path, locale):
    """Changes the path's locale prefix."""
    if get_language(locale) == get_language(settings.LANGUAGE_CODE) \
            and not localeurl.PREFIX_DEFAULT_LOCALE:
        return rmlocale(path)
    else:
        return '/' + get_language(locale) + rmlocale(path)

chlocale = stringfilter(chlocale)
register.filter('chlocale', chlocale)


def rmlocale(url):
    """Removes the locale prefix from the path."""
    return strip_locale_prefix(url)

rmlocale = stringfilter(rmlocale)
register.filter('rmlocale', rmlocale)


def locale_url(parser, token):
    """
    Renders the url for the view with another locale prefix. The syntax is
    like the 'url' tag, only with a locale before the view.

    Examples:
      {% locale_url "de" cal.views.day day %}
      {% locale_url "nl" cal.views.home %}
      {% locale_url "en-gb" cal.views.month month as month_url %}
    """
    bits = token.split_contents()
    if len(bits) < 3:
        raise TemplateSyntaxError("'%s' takes at least two arguments:"
                " the locale and a view" % bits[0])
    urltoken = Token(token.token_type, bits[0] + ' ' + ' '.join(bits[2:]))
    urlnode = defaulttags.url(parser, urltoken)
    return LocaleURLNode(bits[1], urlnode)

class LocaleURLNode(Node):
    def __init__(self, locale, urlnode):
        self.locale = locale
        self.urlnode = urlnode

    def render(self, context):
        locale = resolve_variable(self.locale, context)
        path = self.urlnode.render(context)
        if self.urlnode.asvar:
            self.urlnode.render(context)
            context[self.urlnode.asvar] = chlocale(context[self.urlnode.asvar],
                    locale)
            return ''
        else:
            return chlocale(path, locale)

register.tag('locale_url', locale_url)