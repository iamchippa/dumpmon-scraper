#!/usr/bin/env python
# For the prequisites check to run we rely on modules:
# os.path, re, stat, sys
try:
    import os.path
except:
    print("ERROR: Module re not available. Cannot check prerequsites.")
    print("Please consider installing 'os.path' using pip")
    quit
try:
    import re
except:
    print("ERROR: Module re not available. Cannot check prerequsites.")
    print("Please consider installing 're' using pip")
    quit
try:
    import stat
except:
    print("ERROR: Module stat not available. Cannot check prerequsites.")
    print("Please consider installing 'stat' using pip")
    quit
try:
    import sys
except:
    print("ERROR: Module sys not available. Cannot check prerequsites.")
    print("Please consider installing 'sys' using pip")
    quit

base_dir = os.path.abspath(os.path.dirname(__file__))
MIN_MINOR_VER = 6
DESIRED_PYTHON_MAJOR_VER = 2
PROGRAM_FILE = os.path.join(base_dir, 'dumpmon-scraper.py')
TWITTER_APP_CREDS_FILE = os.path.join(base_dir, '.twitter-app.cfg')


# We support only specific python versions
def check_python_version():
    v = sys.version_info
    vstr = '.'.join([str(v.major), str(v.minor), str(v.micro)])
    print("NOTE: Your python version is %s" % (vstr))
    # print dir(ver_fields)
    if v.major > DESIRED_PYTHON_MAJOR_VER:
        print("ERROR: Python version %s is not supported yet" % vstr)
        quit
    elif v.major < DESIRED_PYTHON_MAJOR_VER or (v.major == DESIRED_PYTHON_MAJOR_VER and v.minor < MIN_MINOR_VER):
        print("ERROR: Python version %s is too old to be supported." % vstr)
        print("You may want to consider upgrading")
        quit
    else:
        print("You python version looks OK for using dumpmon-scraper")


# check if we have the modules that dumpmon needs
def check_program_modules():
    # check for modules
    print("\nNow checking for modules ...")
    try:
        total_modules = 0
        missing_modules = 0
        with open(PROGRAM_FILE, 'r') as f:

            for line in f:
                str = line.rstrip('\n')
                r = re.search('^\s*(import|from)\s+(\S+)', str)
                if r is not None:
                    module_name = r.group(2)
                    print("Checking for module '%s' ..." % module_name)
                    total_modules += 1
                    try:
                        __import__(module_name)
                        print " ====> Module %s found (OK)" % (module_name)
                    except:
                        missing_modules += 1
                        print " (ERROR) Module %s NOT found." % (module_name)

        if missing_modules == 0:
            print("============================================================")
            print("Great! Found all %d needed modules" % total_modules)
            print("============================================================")
        else:
            print("PROBLEM: %d of %d modules not found" % (missing_modules, total_modules))
            print("Please consider installing them using pip")

    except IOError as e:
        print(str(e))
        print("Unable to open file %s for reading modules", PROGRAM_FILE)
        quit


def check_twitter_app_creds():
    if not os.path.isfile(TWITTER_APP_CREDS_FILE):
        print("Twitter app creds file %s does not exist" % TWITTER_APP_CREDS_FILE)
        quit
    else:
        print("Twitter app creds file %s found (OK)" % TWITTER_APP_CREDS_FILE)

        st = os.stat(TWITTER_APP_CREDS_FILE)
        if bool(st.st_mode & (stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX | stat.S_IRWXG | stat.S_IRWXO | stat.S_IXUSR)):
            print("ERROR: Permissions on file %s must be 0600 or 0400" % TWITTER_APP_CREDS_FILE)
            quit
        else:
            print("Permissions on file %s look OK" % TWITTER_APP_CREDS_FILE)


# checking prequisites involves checking python version and the modules and twitter app key file
def check_prequisites():
    print("Checking Prequisites ...\n")
    check_python_version()
    check_program_modules()
    check_twitter_app_creds()


if __name__ == '__main__':
    check_prequisites()
