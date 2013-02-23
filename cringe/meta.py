from gi.types import GObjectMeta, Function
import warnings
from greenlet import greenlet, getcurrent


def AsyncFunction(info, finish):
    args = [a.get_name() for a in info.get_arguments()]
    if args[-2] == 'callback' and args[-1] == 'user_data':
        def function(*args, **kwargs):
            current = getcurrent()
            args = args + (current.switch, None)
            result = info.invoke(*args, **kwargs)
            a, result, b = current.parent.switch()
            fin = finish.invoke(args[0], result, **{})
            return fin
    else:
        warning.warn('Can\'t wrap %s' % info.get_name())
        def function(*args, **kwargs):
            raise NotImplementedError

    function.__info__ = info
    function.__name__ = info.get_name()
    function.__module__ = info.get_namespace()
    function.__finish__ = finish

    return function


class GreenletMeta(GObjectMeta):

    def __init__(cls, name, bases, dict_):
        GObjectMeta.__init__(cls, name, bases, dict_)

    def _setup_methods(cls):
        methods = cls.__info__.get_methods()
        methods = dict((m.get_name(), m) for m in methods)

        for name, info in methods.items():
            if info.is_constructor():
                continue
            if not name.endswith("_async"):
                continue
            sync_name = name[:-6]
            if not sync_name + "_finish" in methods:
                continue

            finish = methods[sync_name + "_finish"]
            function = AsyncFunction(info, finish)

            if info.is_method():
                method = function
            else:
                method = staticmethod(function)

            setattr(cls, sync_name, method)

            if sync_name in methods:
                del methods[sync_name]
            del methods[name]
            del methods[sync_name + "_finish"]

        for name, info in methods.items():
            function = Function(info)
            if info.is_method():
                method = function
            elif info.is_constructor():
                continue
            else:
                method = staticmethod(function)
            setattr(cls, name, method)


def patch_gi():
    from gi import module
    print "Patching"
    module.GObjectMeta = GreenletMeta

