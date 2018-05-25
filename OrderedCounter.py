from collections import Counter, OrderedDict


class OrderedCounter(Counter, OrderedDict):
    '''
    Counter that remembers the order elements are first encountered.
    Methods copied from Py 3.6: Lib/collections/__init__.py
    Originally found at "8.3.6.1. OrderedDict Examples and Recipes"
    https://docs.python.org/3/library/collections.html#collections.OrderedDict

    Replaced Counter() objects with self.__class__() for ordering compatibility.
    '''

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)

    def __add__(self, other):
        '''Add counts from two ordered counters. All elements in the first counter precede those unique to the second.

        >>> OrderedCounter('abbbd') + OrderedCounter('bcc')
        OrderedCounter(OrderedDict([('a', 1), ('b', 4), ('d', 1), ('c', 2)]))

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = self.__class__()
        for elem, count in self.items():
            newcount = count + other[elem]
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return result

    def __sub__(self, other):
        ''' Subtract count, but keep only results with positive counts.

        >>> OrderedCounter('abbbc') - OrderedCounter('bccd')
        OrderedCounter(OrderedDict([('a', 1), ('b', 2)]))

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = self.__class__()
        for elem, count in self.items():
            newcount = count - other[elem]
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count < 0:
                result[elem] = 0 - count
        return result

    def __or__(self, other):
        '''Union is the maximum of value in either of the input counters.

        >>> OrderedCounter('abbbd') | OrderedCounter('bcc')
        OrderedCounter(OrderedDict([('a', 1), ('b', 3), ('d', 1), ('c', 2)]))

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = self.__class__()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = other_count if count < other_count else count
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return result

    def __and__(self, other):
        ''' Intersection is the minimum of corresponding counts.

        >>> OrderedCounter('abbbc') & OrderedCounter('bcc')
        OrderedCounter(OrderedDict([('b', 1), ('c', 1)]))

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = self.__class__()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = count if count < other_count else other_count
            if newcount > 0:
                result[elem] = newcount
        return result

    def __xor__(self, other):
        ''' Exclusive-or (a.k.a. symmetric difference) of two ordered counters.
        Equivalently expressed as (self | other) - (self & other)

        >>> OrderedCounter('abbbc') ^ OrderedCounter('bcc')
        OrderedCounter(OrderedDict([('a', 1), ('b', 2), ('c', 1)]))

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        return self.__or__(other) - self.__and__(other)

    def __pos__(self):
        '''Adds an empty ordered counter, effectively stripping negative and zero counts.'''
        result = self.__class__()
        for elem, count in self.items():
            if count > 0:
                result[elem] = count
        return result

    def __neg__(self):
        '''Subtracts from an empty ordered counter.  Strips positive and zero counts,
        and flips the sign on negative counts.'''
        result = self.__class__()
        for elem, count in self.items():
            if count < 0:
                result[elem] = 0 - count
        return result

