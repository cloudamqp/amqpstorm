.. amqpstorm documentation master file, created by
   sphinx-quickstart on Sun Apr 10 16:25:24 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AMQPStorm package
=================
Thread-safe Python RabbitMQ Client & Management library.

Installation
------------
The latest version can be installed using `pip <https://pip.pypa.io/en/stable/quickstart/>`_ and is available at pypi `here <https://pypi.org/project/AMQPStorm/>`_
::
    pip install amqpstorm

Examples
--------

A wide verity of examples is available on Github at `here <https://github.com/eandersson/amqpstorm/tree/master/examples>`_


Simple Example
--------------

::

   connection = Connection('rmq.amqpstorm.io', 'guest', 'guest')
   channel = connection.channel()
   message = Message.create(channel, 'Hello RabbitMQ!')
   message.publish('simple_queue')



Documentation
-------------

.. toctree::
   :glob:
   :maxdepth: 1

   api/connection
   api/channel
   api/exceptions
   api/message

Management API Documentation
----------------------------

.. toctree::
   :glob:
   :maxdepth: 1

   management_api/*

Issues
------
Please report any issues on Github `here <https://github.com/eandersson/amqpstorm/issues>`_

Source
------
AMQPStorm source code is available on Github `here <https://github.com/eandersson/amqpstorm>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
