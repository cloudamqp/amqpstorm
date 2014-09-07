"""AMQP-Storm Connection.Channel0."""
__author__ = 'eandersson'

import logging
import platform

from pamqp.heartbeat import Heartbeat
from pamqp import specification as pamqp_spec
from pamqp.specification import Connection as pamqp_connection

from amqpstorm import __version__
from amqpstorm.base import Stateful
from amqpstorm.base import FRAME_MAX
from amqpstorm.exception import AMQPConnectionError


LOGGER = logging.getLogger(__name__)


class Channel0(object):
    """Connection.Channel0."""

    def __init__(self, connection):
        super(Channel0, self).__init__()
        self.parameters = connection.parameters
        self._server_properties = None
        self._connection = connection
        self._heartbeat = self.parameters['heartbeat']

    def on_frame(self, frame_in):
        """Handle frame sent to channel 0.

        :param pamqp_spec.Frame frame_in: Amqp frame.
        :return:
        """
        LOGGER.debug("Frame Received: {0}".format(frame_in.name))

        if frame_in.name == 'Heartbeat':
            self._write_frame(Heartbeat())
        elif frame_in.name == 'Connection.Start':
            self._server_properties = frame_in.server_properties
            self._send_start_ok_frame()
        elif frame_in.name == 'Connection.Tune':
            self._send_tune_ok_frame()
            self._send_open_connection()
        elif frame_in.name == 'Connection.OpenOk':
            self._set_connection_state(Stateful.OPEN)
        elif frame_in.name == 'Connection.Close':
            self._close_connection(frame_in)
        elif frame_in.name == 'Connection.Blocked':
            msg = 'Connection was blocked by remote server: {0}'
            LOGGER.warning(msg.format(frame_in.reason))
        else:
            msg = "Unhandled Frame: {0} -- {1}"
            LOGGER.error(msg.format(frame_in.name,
                                    frame_in.__dict__))

    def send_close_connection_frame(self):
        """Send Connection Close frame.

        :return:
        """
        self._write_frame(pamqp_spec.Connection.Close())

    def _close_connection(self, frame_in):
        """Close Connection.

        :param pamqp_spec.Connection.Close frame_in: Amqp frame.
        :return:
        """
        self._set_connection_state(Stateful.CLOSED)
        if frame_in.reply_code != 200:
            msg = 'Connection was closed by remote server: {0}'
            why = AMQPConnectionError(msg.format(frame_in.reply_text))
            self._connection.exceptions.append(why)

    def _set_connection_state(self, state):
        """Set Connection state.

        :param state:
        :return:
        """
        self._connection.set_state(state)

    def _write_frame(self, frame_out):
        """Write a pamqp frame from channel0.

        :param pamqp_spec.Frame frame_out: Amqp frame.
        :return:
        """
        self._connection.write_frame(0, frame_out)

    def _send_start_ok_frame(self):
        """Send Start OK frame.

        :return:
        """
        frame = pamqp_connection.StartOk(
            client_properties=self._client_properties(),
            response=self._credentials(),
            locale='en_US')
        self._write_frame(frame)

    def _send_tune_ok_frame(self):
        """Send Tune OK frame.

        :return:
        """
        frame = pamqp_connection.TuneOk(channel_max=0,
                                        frame_max=FRAME_MAX,
                                        heartbeat=self._heartbeat)
        self._write_frame(frame)

    def _send_open_connection(self):
        """Send Open Connection frame.

        :return:
        """
        frame = pamqp_connection.Open(
            virtual_host=self.parameters['virtual_host']
        )
        self._write_frame(frame)

    def _credentials(self):
        """AMQP Plain Credentials.

        :rtype: str
        """
        return '\0{0}\0{1}'.format(self.parameters['username'],
                                   self.parameters['password'])

    @staticmethod
    def _client_properties():
        """AMQP Library Properties.

        :rtype: dict
        """
        return {'product': 'AMQP-Storm',
                'platform': 'Python %s' % platform.python_version(),
                'capabilities': {'authentication_failure_close': True,
                                 'basic.nack': True,
                                 'connection.blocked': False,
                                 'consumer_cancel_notify': True,
                                 'publisher_confirms': False},
                'information': 'AMQP-Storm',
                'version': __version__}
