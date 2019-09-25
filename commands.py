import sys
import time as t

import serial
import serial.threaded
import serial.tools.list_ports

TIME_MACHINE_BAUD_RATE = 9600


def list_comports():
    """Return a list of COM ports currently available on the computer."""
    ports = serial.tools.list_ports.comports()
    port_descs = [port.description for port in ports]
    port_names = [desc[desc.index("(") + 1:desc.index(")")]
                  for desc in port_descs]
    return port_names


class TimeMachine():
    """Instance of a connection to a Time Machine.

    An instance of a connection to a Time Machine specified by the COM port
    (com_port) it is connected to. Each command that can be sent to a Time
    is available as a class function. Helper functions are present to
    facilitate the serial communication.
    """

    crlf = b'\x0d\x0a'
    set_clock_char = b'\x80'
    up_clock_char = b'\x82'
    down_clock_char = b'\x84'
    retrans_start_char = b'\x05'
    retrans_break_char = b'\x15'
    halt_retrans_char = b'\x17'
    set_event_char = b'\x06'
    xon_char = b'\x11'
    xoff_char = b'\x13'

    def __init__(self, com_port=None):
        self.com_port = com_port
        self.baudrate = TIME_MACHINE_BAUD_RATE

    def send_message(self, message):
        """Send message out over the current com_port. """
        with serial.Serial(self.com_port) as ser:
            # Configure Serial Connection
            # TODO: Allow for more options here.
            # TODO: Allow connection over socket
            ser.write_timeout = 1

            for char in serial.iterbytes(message):
                # Necessary wait to make sure the time machine receives each
                # byte as the rs232 is a low priority source on the time
                # machine. As noted in tm_manual page 4-1.
                try:
                    ser.write(char)
                except serial.SerialTimeoutException as e:
                    raise TimeMachineError(
                        "Serial Connection Timeout: Please check your connection to the Time Machine.")
                t.sleep(.001)
                # TODO: Compare returned int (number of bytes successfully wrote) to attempted to send

    # TIMECLOCK
    def clock_set(self, time=['00', '00', '00'], dir=None):
        """Send a TIMECLOCK command."""
        if (not dir) or (dir == 'stop_set'):
            command = self.set_clock_char + self.time_to_bytes(time) \
                + self.crlf
        elif dir == 'up':
            command = self.up_clock_char + self.time_to_bytes(time) + self.crlf
        elif dir == 'down':
            command = self.down_clock_char + self.time_to_bytes(time) \
                + self.crlf

        self.send_message(command)

    # RETRANSMIT
    def start_retransmit(self, event=1, chute='11', start_time=None):
        """Send RETRANSMIT command."""

        command = self.retrans_start_char + self.to_bytes(event, 3) \
            + self.to_bytes(chute, 2)
        if start_time:
            command += self.retrans_break_char + \
                self.time_to_bytes(start_time) + self.crlf
        else:
            command += self.crlf
        self.send_message(command)

    # HALT RETRANSMIT
    def halt_retransmit(self):
        """Send HALT RETRANSMIT command."""

        command = self.halt_retrans_char
        self.send_message(command)

    # SET EVENT HEAT
    def set_event_heat(self, event=1, heat=None):
        """Send a SET EVENT HEAT command."""

        # TODO fully implement heat option

        if not heat:
            heat = 0
        command = self.set_event_char + self.to_bytes(event, 3) \
            + self.to_bytes(heat, 2) + self.crlf
        self.send_message(command)

    # XON/XOFF
    def xon(self):
        """Send XON command."""

        command = self.xon_char
        self.send_message(command)

    def xoff(self):
        """Send XOFF command."""

        command = self.xoff_char
        self.send_message(command)

    def time_to_bytes(self, time):
        """Translate a list time [HH,MM,SS] to byte string."""

        return ''.join([x[::-1] for x in reversed(time)]).encode()

    def to_bytes(self, input, len):
        """Translate string to padded byte string."""

        return str(input).zfill(len).encode()


class TimeMachineError(Exception):
    """Exception raised for errors in this module.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
