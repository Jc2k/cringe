=====================================
CoRoutines In Nice Gnome Environment
=====================================

This is basically gevent, but using the GNOME platform libraries.

GLib based API's often have asynchronous versions. These tend to use the Gio
pattern which looks something like this::

    from gi.repository import GLib, Gio

    def _loaded(f, result, user_data):
        success, contents, etag = f.load_contents_finish(result)
        print len(contents)

    def _load_stuff(...):
        f = Gio.File.new_for_uri(uri)
        f.load_contents_async(None, _loaded, None)

    GLib.idle_add(_load_stuff)
    loop = GLib.MainLoop()
    loop.run()

But with a sprinkling of greenlet it looks like this::

    from cringe import patch_all()
    patch_all()
    from gi.repository import GLib, Gio

    def _load_stuff(...):
        f = Gio.File.new_for_uri(uri)
        contents = f.load_contents()
        print len(contents)

    GLib.idle_add(_load_stuff)
    GLib.main()

This is still asynchronous! The cringe patch modifies the gi generated bindings
to pause the currently running greenlet when it is waiting for an async
operation to complete. Control can then return to the mainloop, which can
process other incoming events.


Implementation
==============

All Gio-style async API's have an ``_async`` and ``_finish`` method. The
``_async`` function takes a ``callback`` and ``user_data`` parameter, and the
callback gets passed a ``AsyncResult`` which can be used to collect the actual
return value.

Wrapping this in Greenlet magic gives us::

    def function(*args, **kwargs):
        current = greenlet.getcurrent()

        # Call the function and pass it current.switch as the callback - this
        # is what allows the current coroutine to be resumed
        args = args + (current.switch, None)
        some_api_async(*args, **kwargs)

        # Pause the current coroutine. It will be resumed here when the
        # callback calls current.switch()
        obj, result, _ = current.parent.switch()

        # Actually return the expected value
        return some_api_finish(result)

The GLib API mostly followed the same pattern for all of its asynchronous code.
This means we can easily apply this pattern to all bindings automagically by
hooking in to GObjectMeta (in ``gi.types``).

We monkey-patch in our GreenletMeta which uses heuristics to patch the async
API's it can recognise.

