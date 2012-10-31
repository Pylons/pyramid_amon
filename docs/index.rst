Pyramid Amon's documentation
============================

Overview
--------

Pyramid Amon is an add-on for the Pyramid Web Framework which allows
developers to integrate their application with Amon application and system
monitoring toolkit.

Installation
------------

Install using setuptools, e.g. (within a virtualenv)::

  $ easy_install pyramid_amon

Setup
-----

Once :mod:`pyramid_amon` is installed, you must use the ``config.include``
mechanism to include it into your Pyramid project's configuration. In your
Pyramid project's ``__init__.py``:

.. code-block:: python

   config = Configurator(.....)
   config.include('pyramid_amon')

Alternately, instead of using the Configurator's ``include`` method, you can
activate Pyramid by changing your application's ``.ini`` file, use the
following line:

.. code-block:: ini

   pyramid.includes = pyramid_amon

`pyramid_amon` obtains Amon settings from the ``**settings`` dictionary passed
to the Configurator.  It assumes that you've placed Amon configuration
parameters prefixed with ``amon.config.`` in your Pyramid application's ``.ini`` file.
For example:

.. code-block:: ini

   [app:myapp]
   .. other settings ..
   amon.config.address = http://amon_instance:port
   amon.config.protocol = http
   amon.config.secret_key = the-secret-key-from-/etc/amon.conf

Usage
-----

When this add-on is included into your Pyramid application, whenever a request
to your application causes an exception to be raised, the add-on will send the
URL that caused the exception, the exception type, and its related traceback information to an Amon monitoring service you have access.

You also can access logging facilities provided by amonpy.log instance in two
ways:

.. code-block:: python

   request.amon.log(message, tags)

Or

.. code-block:: python

   from pyramid_amon import get_amon
   amon = get_amon(request)
   amon.log({"first_name": "John", "last_name": "Dev", "age": 29}, 'info')

`See Amon documentation for more informations abour configuration and usage
<http://amon.cx/guide/clients/python/>`_.

API Documentation
-----------------

.. automodule:: pyramid_amon

.. autofunction:: get_amon

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

