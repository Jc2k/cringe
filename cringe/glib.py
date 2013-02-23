from greenlet import greenlet, getcurrent

def patch_glib():
    import glib

    m = glib.MainLoop()
    g = greenlet(m.run)

    old_idle_add = glib.idle_add
    def idle_add(callback, *args, **kwargs):
        old_idle_add(greenlet(callback, g).switch, *args, **kwargs)

    old_timeout_add = glib.timeout_add
    def timeout_add(interval, callback, *args, **kwargs):
        old_timeout_add(interval, greenlet(callback, g).switch, *args, **kwargs)

    old_timeout_add_seconds = glib.timeout_add_seconds
    def timeout_add_seconds(interval, callback, *args, **kwargs):
        old_timeout_add_seconds(interval, greenlet(callback, g).swtich, *args, **kwargs)

    def sleep(timeout):
        current = getcurrent()
        old_timeout_add(timeout, current.switch)
        current.parent.switch()

    def main():
        g.switch()

    glib.idle_add = idle_add
    glib.timeout_add = timeout_add
    glib.timeout_add_seconds = timeout_add_seconds
    glib.sleep = sleep
    glib.main = main

