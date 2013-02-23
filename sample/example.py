from cringe import patch_all
patch_all()

import glib
from gi.repository import Gio

def example():
    print "Sleeping"
    glib.sleep(5000)
    print "Enumerating"
    enumerate_dir()
    print "Exiting"
    return False

def enumerate_dir():
    the_dir = Gio.File.new_for_path("/home/john")
    e = the_dir.enumerate_children(Gio.FILE_ATTRIBUTE_STANDARD_NAME, 0, glib.PRIORITY_DEFAULT, None)
    while True:
        files = e.next_files(10, glib.PRIORITY_DEFAULT, None)
        if not files:
            break
        for f in files:
            print f.get_name()


def example2():
    print "Getting file"
    f = Gio.File.new_for_path("/home/john/ubuntu-10.04.4-server-amd64.iso")
    stream = f.read(0, None)

    print stream

glib.idle_add(example)
glib.idle_add(example2)
glib.idle_add(example)
glib.main()

