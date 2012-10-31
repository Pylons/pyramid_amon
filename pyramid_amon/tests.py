import unittest
from pyramid import testing

import mock


class DummyException(Exception):
    pass


class Test_amon_tween(unittest.TestCase):
    def setUp(self):
        from pyramid.request import Request
        request = Request.blank('/')
        self.request = request
        self.config = testing.setUp(request=request)
        self.registry = self.config.registry
        self.registry.settings = {}
        self.request.registry = self.registry
        self.amonpy = mock.Mock()

    def handler(self, request):
        raise NotImplementedError

    def dummy_exception(self, request):
        raise DummyException()

    def _callFUT(self, handler=None, registry=None, request=None, amonpy=None):
        from pyramid_amon import amon_tween_factory
        if handler is None:
            handler = self.handler
        if registry is None:
            registry = self.registry
        if request is None:
            request = self.request
        if amonpy is None:
            amonpy = self.amonpy
        tween = amon_tween_factory(handler, registry)
        return tween(request, amonpy)

    def test_handler(self):
        self.assertRaises(NotImplementedError, self._callFUT)
        kwargs = self.amonpy.exception.call_args[0][0]
        self.assertEqual(kwargs['exception_class'], 'NotImplementedError')

    def test_dummy_exception(self):
        self.assertRaises(DummyException, self._callFUT, self.dummy_exception)
        kwargs = self.amonpy.exception.call_args[0][0]
        self.assertEqual(
            kwargs['exception_class'],
            'pyramid_amon.tests.DummyException'
            )

    def test_request_GET(self):
        from pyramid.request import Request
        self.request = Request.blank('/?hello=world')
        self.assertRaises(NotImplementedError, self._callFUT)
        kwargs = self.amonpy.exception.call_args[0][0]
        self.assertEqual(kwargs['url'], 'http://localhost/?hello=world')
        self.assertEqual(kwargs['data']['get'], "[(u'hello', [u'world'])]")

    def test_request_POST(self):
        from pyramid.request import Request
        from webob.multidict import MultiDict
        args = MultiDict(hello='world')
        self.request = Request.blank('/', POST=args)
        self.assertRaises(NotImplementedError, self._callFUT)
        kwargs = self.amonpy.exception.call_args[0][0]
        self.assertEqual(
            kwargs['data']['post'],
            '[(\'hello\', ["u\'world\'"])]'
            )

    def test_request_cookies(self):
        self.request.environ['HTTP_COOKIE'] = 'hello="world"'
        self.assertRaises(NotImplementedError, self._callFUT)
        kwargs = self.amonpy.exception.call_args[0][0]
        self.assertEqual(kwargs['data']['cookies'], "[(u'hello', u'world')]")

    def test_request_session(self):
        from pyramid.interfaces import ISessionFactory

        def factory(request):
            return {'hello': 'world'}

        self.request.registry.registerUtility(factory, ISessionFactory)
        self.assertRaises(NotImplementedError, self._callFUT)
        kwargs = self.amonpy.exception.call_args[0][0]
        self.assertEqual(kwargs['data']['session'], "[('hello', 'world')]")

    def test_request_matchdict(self):
        self.request.matchdict = {'hello': 'world'}
        self.assertRaises(NotImplementedError, self._callFUT)
        kwargs = self.amonpy.exception.call_args[0][0]
        self.assertEqual(kwargs['data']['matchdict'], "[('hello', 'world')]")

    def test_request_matched_route(self):
        matched_route = mock.Mock()
        matched_route.name = 'test'
        matched_route.path = '/test'
        self.request.matched_route = matched_route
        self.assertRaises(NotImplementedError, self._callFUT)
        kwargs = self.amonpy.exception.call_args[0][0]
        self.assertEqual(
            kwargs['data']['matched_route'],
            "[('name', 'test'), ('path', '/test')]"
            )

    def test_get_amon(self):
        from pyramid_amon import get_amon
        self.config.registry.settings['amon.config.address'] = 'http://localhost'
        self.config.registry.settings['amon.config.secret_key'] = 'seekritkey'
        self.config.include('pyramid_amon')
        amon = get_amon(self.request)
        self.assertEqual(amon.__name__, 'amonpy')
