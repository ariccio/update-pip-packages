update-pip-packages
===================

Update all the packages (in alphabetical order) that you have installed globally with pip (i.e. with `sudo pip install`). Runs multiple instances of pip in parallel for faster updating. Yes, multithreaded pip upgrades - now your CPU is the bottleneck ;)

I wrote this because pip won't get an upgrade-all option anytime soon, and this seems to work. It's NOT a true fix for the problem - in fact it's a dirty hack - but it's a nice stopgap measure!

Enjoy multithreaded pip updates!

Alexander Riccio - alexander@riccio.com
inspired by code from:
	Jabba Laci, 2013--2014 (jabba.laci@gmail.com)
	<http://pythonadventures.wordpress.com/2013/05/22/update-all-pip-packages/>