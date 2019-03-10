class Rtdout():

    def __init__(self):
        self.stdout = None

    def getstdout(self):
        # get current stdout for Rprint
        return self.stdout


class Rprint():
    rtdout = Rtdout()

    def __init__(self):
        self.__storage__ = []

    def flush(self):
        # dummy method to support stream flushing
        self.__storage__.clear()

    def ret(self):
        return self.__storage__.copy()

    def write(self, *objects):
        # dummy method to support file-like object writing
        self.__storage__.append(*objects)

    def __call__(self, *objects, sep=' ', end='\n', file=rtdout, flush=False):
        """
        :param objects: Any type, that can be turned into str or repr
        :param sep: separator for few objects. rprint('one', 'two', sep='-', end='') ~ '-'.join(('one', 'two'))
        :param end: end of result string
        :param file: output, raises AttributeError if stream file can't be writed
        :param flush: flushes stream, raises AttributeError if stream file can't be flushed
        :return:
        """
        sep, end = ' ' if sep is None else sep, '\n' if end is None else end

        if isinstance(file, Rtdout) or file is None:
            writefile = self.rtdout.getstdout()
            file = self if not writefile else writefile

        try:
            file.write
        except AttributeError:
            raise AttributeError("'{type}' object has no attribute 'write'".format(type=type(file))) from None

        if flush:
            try:
                file.flush
            except AttributeError:
                raise AttributeError("'{type}' object has no attribute 'flush'".format(type=type(file))) from None
            file.flush()
        if objects == ():
            file.write(end)
            return

        # check if sep exists to prevent unnecessary __lookahead__ calls
        if sep:
            temp = [str(obj) + sep if has_more else str(obj) for obj, has_more in self.__lookahead__(objects)]
        else:
            temp = [str(obj) for obj in objects]
        temp.append(end)
        file.write(''.join(temp))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__storage__.clear()

    def __iter__(self):
        # method to iterate through storage when iterating Rprint object itself
        return (i for i in self.__storage__)

    @staticmethod
    def __lookahead__(iterable):
        # looks for objects remained after last to emulate ''.join() behaviour
        it = iter(iterable)
        last = next(it)
        for val in it:
            yield last, True
            last = val
        yield last, False

    def __repr__(self):
        return "<{gname}.{cname}({vals}sep='', end='')>".format(
            gname=__name__,
            cname=self.__class__.__name__,
            vals=', '.join((repr(el) for el in self.__storage__)) + ', ' if self.__storage__ else ''
        )

    def __setattr__(self, attr, value):
        # prevent from setting new attributes
        if attr not in ['__storage__', 'stdout']:
            raise AttributeError("type object '{type}' has no attribute '{attr}'".format(
                type=type(self), attr=attr)
            )
        super(Rprint, self).__setattr__(attr, value)

    def __str__(self):
        res = ''.join(self.__storage__)
        return res
