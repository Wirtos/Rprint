class Rtdout():

    def __init__(self):
        self.stdout = None

    def getstdout(self):
        return self.stdout


class Rprint():
    rtdout = Rtdout()
    def __init__(self, *args, **kwargs):
        self.__storage__ = []

    def flush(self):
        self.__storage__.clear()

    def ret(self):
        return self.__storage__.copy()

    def write(self, *objects):
        self.__storage__.append(*objects)

    def __call__(self, *objects, sep=' ', end='\n', flush=False, file=rtdout):
        if isinstance(file, Rtdout):
            writefile = file.getstdout()
            file = self if not writefile else writefile
        try:
            file.write
        except AttributeError:
            raise AttributeError("'{}' object has no attribute 'write'".format(type(file))) from None

        if flush:
            try:
                file.flush
            except AttributeError:
                raise AttributeError("'{}' object has no attribute 'flush'".format(type(file))) from None
            file.flush()
        if objects == ():
            file.write(end)
            return

        temp = []

        for obj, has_more in self.__lookahead__(objects):
            temp.append(str(obj))
            if has_more:
                temp.append(sep)
        temp.append(end)
        file.write(''.join(temp))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__storage__.clear()

    def __iter__(self):
        return (i for i in self.__storage__)

    @staticmethod
    def __lookahead__(iterable):
        it = iter(iterable)
        last = next(it)
        for val in it:
            yield last, True
            last = val
        yield last, False

    def __repr__(self):
        representation = ', '.join((repr(el) for el in self.__storage__)) + ', ' if self.__storage__ else ''
        return "<{gname}.{cname}({vals}sep='', end='')>".format(
            gname=__name__,
            cname=self.__class__.__name__,
            vals=representation
        )

    def __setattr__(self, attr, value):
        if attr not in ['__storage__', 'stdout']:
            raise AttributeError("type object '{}' has no attribute '{}'".format(type(self), attr))
        super(Rprint, self).__setattr__(attr, value)

    def __str__(self):
        res = ''.join(self.__storage__)
        return res
