from django.conf import settings
from django.core import urlresolvers
from django.utils import translation
from localeurl import utils
from django.core.urlresolvers import get_urlconf

def reverse(*args, **kwargs):
    reverse_kwargs = kwargs.get('kwargs') or {}
    prefix = kwargs.get('prefix') or None
    urlconf = kwargs.get('urlconf') or None

    if urlconf is None:
        urlconf = get_urlconf()

    locale = utils.supported_language(reverse_kwargs.pop(
            'locale', translation.get_language()))
    url = django_reverse(*args, **kwargs)
    stipped_prefix, path = utils.strip_script_prefix(url, prefix = prefix)
    return utils.locale_url(path, locale, prefix = stipped_prefix, urlconf=urlconf)

django_reverse = None

def patch_reverse():
    """
    Monkey-patches the urlresolvers.reverse function. Will not patch twice.
    """
    global django_reverse
    if urlresolvers.reverse is not reverse:
        django_reverse = urlresolvers.reverse
        urlresolvers.reverse = reverse

if settings.USE_I18N:
    patch_reverse()
