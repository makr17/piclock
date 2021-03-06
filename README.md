piclock
=======

code to drive display and gpio on my alarm clock project

disclaimer
----------

I should say up front that python is definitely not my first language.  likely not second or third
either...  but the libraries for my hardware are readily available in python, so I'm using it.  and
enjoying it honestly more than I thought I would.

while the code _works_, there are probably more ideomatic/pythonic ways to do some of the things I'm
doing.  if you have a suggestion, fork and submit a pull request.

danke...

quick intro
-----------

the idea is to use a raspberry pi to build an alarm clock that is network-connected (either via wifi
or wired ethernet).  it should sync time via ntp so it is always in sync and doesn't require manual
intervention.  clock should check geoip for location and timezone on startup.  all time is handled
in UTC and scaled using timezone fetched via geoip.  so if the clock is moved from los angeles to
new york I should be able to plug it in and it will wake me up at my configured alarm time in the
local timezone without intervention.

hardware
--------

so far:

- 1 [raspberry pi](http://www.raspberrypi.org)
- 1 [case](http://www.amazon.com/gp/product/B007POB85K/)
- 1 [power switch](http://mausberrycircuits.com/products/shutdown-switch-with-rocker)
- 1 [four digit display](http://www.adafruit.com/products/881)
- 1 [big illuminated button](http://www.adafruit.com/products/1194)
- 1 [small illuminated button](http://www.adafruit.com/products/1477)
- 2 [small buttons](http://www.adafruit.com/products/1505)
- 1 [stereo amplifier](http://www.adafruit.com/products/1552)
- 2 [small speakers](http://www.adafruit.com/products/1313)

software dependencies
---------------------

- datetime (python built-in)
- httplib (python built-in)
- json (python built-in)
- logging (python built-in)
- time (python built-in)
- xml (python built-in)

- [fysom](https://pypi.python.org/pypi/fysom/1.0.9) (pip install)
- [pytz](https://pypi.python.org/pypi/pytz) (pip install)
- [suds](https://fedorahosted.org/suds/) (pip install)

- [quick2wire-python-api](https://github.com/quick2wire/quick2wire-python-api)
- [Adafruit_7Segment](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code)

details
-------

most of the examples I found for both updating clock display and monitoring button input via gpio
just spun in a loop, _maybe_ with a small sleep...  sub-optimal as far as I'm concerned.

so this project is doing things a bit differently.  I'm using an event loop to monitor both gpio
and timers.  I've got a 60 second timer configured so it trips at the top of each minute, and that
updates the clock display.  means I can't have the colon flash, but I really don't care about that.
another timer trips every hour and refreshes the stored weather forecast.  the event loop monitors
two buttons currently, a mode button and a set button.

state of the application is managed via a finite state machine, thanks to fysom.  the mode button
progresses from one state to the next.  right now there are two fixed modes: clock and high
temperature forecast.  we also dynamically append an additional mode for each alarm defined in the
configuration.  with the current example configuration that is three additional alarm states for a
total of five.

- clock is local time display
- high temp forecast is today's high temp until noon, tomorrow's high temp after noon
- alarm 0 through alarm N for the configured alarms
- ...then back to clock 

there is also an inactivity timer running.  the clock will revert to time mode after 15 seconds of
inactivity in another mode.

the set button is mode-dependent in

- clock mode it cycles through display brightness levels
- temp forecast mode it currently does nothing
- in alarm modes it is planned to start the time scrolling to change the alarm time

things for the future:

- ~~a timeout timer, revert to time display after N seconds of inactivity in other modes~~
- do something real in the alarm states, allow setting/changing of the alarm time
- ~~make the alarm states dynamic based on config, rather than statically defined~~
- add a button to toggle alarm on/off, illuminate the button when alarm(s) are on
- add a button to turn the alarm sound off, illuminate the button when the alarm trips
- add sound ouput (most likely via pygame.mixer)
- fabricate the enclosure for all of the above hardware
