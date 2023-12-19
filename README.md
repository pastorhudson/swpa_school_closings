# swpa_school_closings
Simple Script to tell you if school is closed.

## Command Line Options
Our program provides several command-line arguments to control its behavior.

usage: python closings.py [-a] [-r] [-s] [-sa]

Options:

-a, --add-school        Add a school to the configuration.
                        Usage: `closings.py -a school_name`
                        Replace `school_name` with the actual school name.

-r, --remove-school     Remove a school from the configuration.
                        Usage: `closings.py -r school_name`
                        Replace `school_name` with the actual school name to be removed.

-s, --show-schools      Display the current schools in the configuration.
                        Usage: `closings.py -s`

-sa, --show-all-schools Show all school configurations.
                        Usage: `closings.py -sa`

-h, --help              Show the help message and exit.
                        Usage: `closings.py -h`
