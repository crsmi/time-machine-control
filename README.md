# time-machine-control
**Time Machine Control** is simple GUI used to interact with a **Time Machine** race timer from [Fleet Feet Computers](https://timemachine.org). It can send commands (as documented in the [Time Machine Manual](resources/tm_manual.pdf#page=39)) over a serial connection to a Time Machine .

<img src=/resources/TimeMachineControlApp.PNG alt="Time Machine Control" align="center">

<hr>

Version 0.1.0 is a simple applet that only covers sending of commands over a COM port to the Time Machine. A COM port connection to the Time Machine can be created with a RS232 to USB converter or by using a serial over network connection along with a virtual COM port.



Future features:
  - Standalone executable applet.
  - Saving settings like event number after closing and reopening.
  - Text output panel.
  - Ability to listen to the Time Machine's RS232 transmitter.
  - Collect data retransmitted to a file (which will make the retransmit button actually useful).
  - More fine-grained control over a retransmission - utilizing halt to stop retransmit after a specified time.
  - Port sharing mode so that Time Machine Control can be used alongside race timing software like The Race Director.
  - Connections to multiple Time Machine's using multiple COM ports.


## Installing Time Machine control

Requires python to be installed and configured.

1. Clone repository.
2. Install requirements.
3. Run using python tmcontrol.py

## Using Time Machine control

### Connection
Use the "COM Port" selection under Connection to specify which COM port the Time Machine is connected to.

### Commands
There are five possible commands that can be sent to a Time Machine documented in the [manual](resources/tm_manual.pdf#page=39). Python code that the GUI uses to send these commands in contained in [commands.py](./commands.py)

**TIMECLOCK** - Set the time on the Time Clock. It may be started or stopped and the direction(up or down count) may be specified.

**RETRANSMIT** - Tells the Time Machine to retransmit data over the RS232 interface.

**HALT RETRANSMIT** - Stop retransmission of data.

**SET EVENT HEAT** - Change the Event and Heat (model 2 only) numbers in the Time Machine.

**XON/XOFF** - Turn the Time Machine's RS232 transmitter on/off.
