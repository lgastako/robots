#
# Welcome to the (self documenting) Makefile of the robots project.
#
# Please sit back, relax, and enjoy the ride.
#

# The default 'all' target displays this documentation.
#
all:
	@grep -e '^.: ' -e '^#' Makefile | sed s'/^# *//' | grep -v '^#\.'

# The 'help' target is an alias for the 'all' target just in case someone
# instinctively types "make help".
#
help:
	all

# The 'install' target uses pip to install the current project as a python
# project.
#
install: setup.py
	pip install -e .

# The 'test' target executes py.test letting it do it's thing as optionally
# configured in 'pytest.ini' at the top level of the project.
test:
	py.test

# This Makefile is arranged such as it is so that those who are not familiar
# with it may read through either the output of executing the 'all' target or
# by reading the source if more proof is required :)
#
# ...and so that those are are familiar with it will find the shortcuts right
# here at the end, allowing their eyes to find the information they most
# desired right here above the prompt.
#
# The following short cuts are available:
#
i: install
t: test

#
#...Thank you and please enjoy your development experience.
