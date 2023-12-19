# swpa_school_closings
Simple Script to tell you if school is closed.

## Command Line Options
Our program provides several command-line arguments to control its behavior.

usage: school [-a] [-r] [-s] [-sa]

Options:

-a, --add-school        Add a school to the configuration.
                        Usage: `school -a school_name`
                        Replace `school_name` with the actual school name.

-r, --remove-school     Remove a school from the configuration.
                        Usage: `school -r school_name`
                        Replace `school_name` with the actual school name to be removed.

-s, --show-schools      Display the current schools in the configuration.
                        Usage: `school -s`

-sa, --show-all-schools Show all school configurations.
                        Usage: `school -sa`

-h, --help              Show the help message and exit.
                        Usage: `school -h`
