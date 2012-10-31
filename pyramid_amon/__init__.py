# -*- coding: utf-8 -*-
from pprint import saferepr
import sys
import traceback

from pyramid.exceptions import ConfigurationError
from pyramid.tweens import EXCVIEW

from zope.interface import Interface

import amonpy

PY3 = sys.version_info[0] == 3

if PY3: # pragma: no cover
    import builtins
else:
    import __builtin__ as builtins


def exc_info(exc, tb):
    """Format exception information."""

    backtrace = []
    for part in traceback.format_tb(tb):
        backtrace.extend(part.rstrip().splitlines())
    return {
        'message': str(exc),
        'backtrace': backtrace,
        'exception_class': exc_class(exc)
        }


def exc_class(exc):
    """Return a name representing the class of an exception."""

    cls = type(exc)
    if cls.__module__ == 'exceptions':  # Built-in exception.
        return cls.__name__
    return "%s.%s" % (cls.__module__, cls.__name__)


def amon_tween_factory(handler, registry):

    def amon_tween(request, amonpy=amonpy):
        try:
            return handler(request)
        except Exception as exc:
            url = request.url
            env_excludes = ('HTTP_COOKIE', 'webob._parsed_cookies')
            env = [(k, request.get(k)) for k in request.environ
                if k not in env_excludes]
            info = exc_info(exc, sys.exc_info()[2])
            extras = {}
            if request.GET:
                extras.update({
                    'get': saferepr([(k, request.GET.getall(k))
                        for k in request.GET])
                    })
            if request.POST:
                extras.update({
                    'post': saferepr([(k, [saferepr(p)
                        for p in request.POST.getall(k)])
                            for k in request.POST])
                    })
            if request.cookies:
                extras.update({
                    'cookies': saferepr(request.cookies.items())
                    })
            if hasattr(request, 'session'):
                if request.session:
                    extras.update({
                        'session': saferepr(request.session.items()),
                        })
            if request.matchdict:
                extras.update({
                    'matchdict': saferepr(request.matchdict.items())
                    })
            if request.matched_route:
                extras.update({
                    'matched_route': saferepr([
                        ('name', request.matched_route.name),
                        ('path', request.matched_route.path)
                        ])
                    })
            data = {
                'exception_class': info['exception_class'],
                'url': url,
                'backtrace': info['backtrace'],
                'message': info['message'],
                'enviroment': saferepr(env),
                'data': extras
                }
            amonpy.exception(data)
            raise

    return amon_tween


class IAmon(Interface):
    pass


def get_amon(config_or_request):
    """Obtain an amonpy instance previously registered via
    ``config.include('pyramid_amon')``.
    """
    return config_or_request.registry.getUtility(IAmon)


def includeme(config):  # pragma: no cover
    settings = config.registry.settings
    address = settings.get('amon.config.address', None)
    if address is None:
        raise ConfigurationError(
            'You must set amon.config.address in you ini file')
    protocol = settings.get('amon.config.protocol', 'http')
    secret_key = settings.get('amon.config.secret_key', None)
    if secret_key is None:
        raise ConfigurationError(
            'You must set amon.config.secret_key in you ini file')
    amonpy.config.address = address
    amonpy.config.protocol = protocol
    amonpy.config.secret_key = secret_key
    config.registry.registerUtility(amonpy, IAmon)
    config.add_directive('get_amon', get_amon)
    config.add_request_method(
        get_amon,
        'amon',
        property=True,
        reify=True
        )
    config.add_tween('pyramid_amon.amon_tween_factory', under=EXCVIEW)
