from six import itervalues, iteritems
import numpy as np
from collections import OrderedDict
import darch.core as co

class HyperparameterSharer:
    def __init__(self):
        self.name2hfn = OrderedDict()    
        self.name2h = OrderedDict()

    def register(self, h_name, fn):
        assert h_name not in self.name2hfn
        self.name2hfn[h_name] = fn

    def get(self, h_name):
        assert h_name in self.name2hfn

        if h_name not in self.name2h:
            self.name2h[h_name] = self.name2hfn[h_name]()
        return self.name2h[h_name]

class DependentHyperparameter(co.Hyperparameter):
    def __init__(self, fn, hs, scope=None, name=None):
        co.Hyperparameter.__init__(self, scope, name)

        self._hs = hs
        self._fn = fn

    def is_set(self):
        if self.set_done:
            return True
        else:
            if all( h.is_set() for h in itervalues(self._hs) ):
                kwargs = { name : h.get_val() for name, h in iteritems(self._hs) }
                self.set_val( self._fn(**kwargs) )
            
            return self.set_done

    def get_unset_dependent_hyperparameter(self):
        assert not self.set_done
        for h in itervalues(self._hs) :
            if not h.is_set():
                return h

class Discrete(co.Hyperparameter):
    def __init__(self, vs, scope=None, name=None):
        co.Hyperparameter.__init__(self, scope, name)
        self.vs = vs

    def _check_val(self, v):
        assert v in self.vs

class Bool(Discrete):
    def __init__(self, scope=None, name=None):
        Discrete.__init__(self, [0, 1], scope, name)

class OneOfK(Discrete):
    def __init__(self, k, scope=None, name=None):
        Discrete.__init__(self, range(k), scope, name)

class OneOfKFactorial(Discrete):
    def __init__(self, k, scope=None, name=None):
        Discrete.__init__(self, np.product(np.arange(1, k + 1)), scope, name)
