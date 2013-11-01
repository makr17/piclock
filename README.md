piclock
=======

code to drive display and gpio on my alarm clock project

quick intro
-----------

the idea is to use a raspberry pi to build an alarm clock that is network-connected (either via wifi
or wired ethernet).  it should sync time via ntp so it is always in sync and doesn't require manual
intervention.  clock should check geoip for location and timezone on startup.  all time is handled
in UTC and scaled using timezone fetched via geoip.  so if the clock is moved from los angeles to
new york it should be able to react accordingly without external intervention.

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
