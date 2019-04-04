class Rtdout():
    def __init__(self):
        self.stdout = None

    def getstdout(self):
        # get current stdout for Rprint
        return self.stdout


class Rprint():
    def __init__(self):
        # write needed attributes and then lock setattr
        super(Rprint, self).__setattr__("_lock", 0)
        self._storage = []
        self.rtdout = Rtdout()
        super(Rprint, self).__delattr__('_lock')

    def flush(self):
        # dummy method to support stream flushing
        self._storage.clear()

    def ret(self):
        return self._storage.copy()

    def write(self, objects):
        # dummy method to support file-like object writing
        self._storage.append(objects)

    def __call__(self, *objects, sep=' ', end='\n', file=None, flush=False):
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

        # check if sep exists to prevent unnecessary lookahead calls
        if sep:
            temp = [str(obj) + sep if has_more else str(obj) for obj, has_more in self.lookahead(objects)]
        else:
            temp = [str(obj) for obj in objects]
        temp.append(end)
        file.write(''.join(temp))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._storage.clear()

    def __iter__(self):
        # method to iterate through storage when iterating Rprint object itself
        return iter(self._storage)

    @staticmethod
    def lookahead(iterable):
        # looks for objects remained after iterated one to emulate ''.join() behaviour
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
            vals=', '.join((repr(el) for el in self._storage)) + ', ' if self._storage else ''
        )

    def __setattr__(self, attr, value):
        # prevent from setting new attributes
        if attr not in ('_storage', 'rtdout',) if hasattr(self, '_lock') else ('_storage',):
            raise AttributeError("type object '{type}' has no writeable attribute '{attr}'".format(
                type=type(self), attr=attr)
            )
        super(Rprint, self).__setattr__(attr, value)

    def __str__(self):
        res = ''.join(self._storage)
        return res


class ARprint(Rprint):
    async def __call__(self, *objects, sep=' ', end='\n', file=None, flush=False):
        import asyncio
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

        # check if sep exists to prevent unnecessary lookahead calls
        if sep:
            for obj, has_more in self.lookahead(objects):
                file.write(str(obj) + sep) if has_more else file.write(str(obj))
                await asyncio.sleep(0)
        else:
            for obj in objects:
                file.write(str(obj))
                await asyncio.sleep(0)
        file.write(end)


class CRprint(Rprint):
    def __call__(self, *objects, sep=' ', end='\n', file=None, flush=False):
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

        # check if sep exists to prevent unnecessary lookahead calls
        if sep:
            for obj, has_more in self.lookahead(objects):
                file.write(str(obj) + sep) if has_more else file.write(str(obj))
        else:
            for obj in objects:
                file.write(str(obj))
        file.write(end)
