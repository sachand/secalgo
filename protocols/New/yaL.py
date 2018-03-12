# -*- generated by 1.0.12 -*-
import da
PatternExpr_185 = da.pat.TuplePattern([da.pat.ConstantPattern('msg2'), da.pat.TuplePattern([da.pat.BoundPattern('_BoundPattern188_'), da.pat.FreePattern('encBS')])])
PatternExpr_194 = da.pat.BoundPattern('_BoundPattern195_')
PatternExpr_277 = da.pat.TuplePattern([da.pat.ConstantPattern('msg3'), da.pat.TuplePattern([da.pat.FreePattern('encSA'), da.pat.FreePattern('encSB')])])
PatternExpr_287 = da.pat.BoundPattern('_BoundPattern288_')
PatternExpr_361 = da.pat.TuplePattern([da.pat.ConstantPattern('msg1'), da.pat.TuplePattern([da.pat.FreePattern('A'), da.pat.FreePattern('nA')])])
PatternExpr_371 = da.pat.FreePattern('A')
PatternExpr_397 = da.pat.TuplePattern([da.pat.ConstantPattern('msg4'), da.pat.TuplePattern([da.pat.FreePattern('encSB'), da.pat.FreePattern('encAB')])])
PatternExpr_407 = da.pat.BoundPattern('_BoundPattern408_')
_config_object = {}
from sa.secalgoB import *

class RoleS(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_RoleSReceivedEvent_0', PatternExpr_185, sources=[PatternExpr_194], destinations=None, timestamps=None, record_history=None, handlers=[self._RoleS_handler_184])])

    def setup(self, A, B, kAS, kBS, **rest_513):
        super().setup(A=A, B=B, kAS=kAS, kBS=kBS, **rest_513)
        self._state.A = A
        self._state.B = B
        self._state.kAS = kAS
        self._state.kBS = kBS
        at_fork()
        self._state.terminate = False

    def run(self):
        super()._label('_st_label_180', block=False)
        _st_label_180 = 0
        while (_st_label_180 == 0):
            _st_label_180 += 1
            if self._state.terminate:
                _st_label_180 += 1
            else:
                super()._label('_st_label_180', block=True)
                _st_label_180 -= 1

    def _RoleS_handler_184(self, encBS):
        nB = nA = None

        def ExistentialOpExpr_197():
            nonlocal nB, nA
            for (_BoundPattern200_, nA, nB) in [decrypt(encBS, key=self._state.kBS)]:
                if (_BoundPattern200_ == self._state.A):
                    if True:
                        return True
            return False
        if ExistentialOpExpr_197():
            kAB = keygen('shared')
            self.send(('msg3', (encrypt((self._state.B, kAB, nA, nB), key=self._state.kAS), encrypt((self._state.A, kAB), key=self._state.kBS))), to=self._state.A)
        self._state.terminate = True
    _RoleS_handler_184._labels = None
    _RoleS_handler_184._notlabels = None

class RoleA(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._RoleAReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_RoleAReceivedEvent_0', PatternExpr_277, sources=[PatternExpr_287], destinations=None, timestamps=None, record_history=True, handlers=[])])

    def setup(self, B, S, kAS, **rest_513):
        super().setup(B=B, S=S, kAS=kAS, **rest_513)
        self._state.B = B
        self._state.S = S
        self._state.kAS = kAS
        at_fork()

    def run(self):
        nA = nonce()
        self.send(('msg1', (self._id, nA)), to=self._state.B)
        super()._label('_st_label_274', block=False)
        encSB = encSA = kAB = nB = None

        def ExistentialOpExpr_275():
            nonlocal encSB, encSA, kAB, nB
            for (_, (_, _, _BoundPattern295_), (_ConstantPattern297_, (encSA, encSB))) in self._RoleAReceivedEvent_0:
                if (_BoundPattern295_ == self._state.S):
                    if (_ConstantPattern297_ == 'msg3'):

                        def ExistentialOpExpr_303(encSA):
                            nonlocal nB, kAB
                            for (_BoundPattern306_, kAB, _BoundPattern309_, nB) in [decrypt(encSA, key=self._state.kAS)]:
                                if (_BoundPattern306_ == self._state.B):
                                    if (_BoundPattern309_ == nA):
                                        if True:
                                            return True
                            return False
                        if ExistentialOpExpr_303(encSA=encSA):
                            return True
            return False
        _st_label_274 = 0
        while (_st_label_274 == 0):
            _st_label_274 += 1
            if ExistentialOpExpr_275():
                _st_label_274 += 1
            else:
                super()._label('_st_label_274', block=True)
                _st_label_274 -= 1
        self.send(('msg4', (encSB, encrypt(nB, key=kAB))), to=self._state.B)
        self.output('A - Key Exchange Complete')

class RoleB(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._RoleBReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_RoleBReceivedEvent_0', PatternExpr_361, sources=[PatternExpr_371], destinations=None, timestamps=None, record_history=None, handlers=[self._RoleB_handler_360]), da.pat.EventPattern(da.pat.ReceivedEvent, '_RoleBReceivedEvent_1', PatternExpr_397, sources=[PatternExpr_407], destinations=None, timestamps=None, record_history=True, handlers=[])])

    def setup(self, S, kBS, **rest_513):
        super().setup(S=S, kBS=kBS, **rest_513)
        self._state.S = S
        self._state.kBS = kBS
        at_fork()
        self._state.terminate = False

    def run(self):
        super()._label('_st_label_356', block=False)
        _st_label_356 = 0
        while (_st_label_356 == 0):
            _st_label_356 += 1
            if self._state.terminate:
                _st_label_356 += 1
            else:
                super()._label('_st_label_356', block=True)
                _st_label_356 -= 1

    def _RoleB_handler_360(self, A, nA):
        nB = nonce()
        self.send(('msg2', (self._id, encrypt((A, nA, nB), key=self._state.kBS))), to=self._state.S)
        super()._label('_st_label_394', block=False)
        encAB = encSB = kAB = None

        def ExistentialOpExpr_395():
            nonlocal encAB, encSB, kAB
            for (_, (_, _, _BoundPattern415_), (_ConstantPattern417_, (encSB, encAB))) in self._RoleBReceivedEvent_1:
                if (_BoundPattern415_ == A):
                    if (_ConstantPattern417_ == 'msg4'):

                        def ExistentialOpExpr_424(encSB):
                            nonlocal kAB
                            for (_BoundPattern427_, kAB) in [decrypt(encSB, key=self._state.kBS)]:
                                if (_BoundPattern427_ == A):
                                    if True:
                                        return True
                            return False

                        def ExistentialOpExpr_438(encAB):
                            for _BoundPattern441_ in [decrypt(encAB, key=kAB)]:
                                if (_BoundPattern441_ == nB):
                                    if True:
                                        return True
                            return False
                        if (ExistentialOpExpr_424(encSB=encSB) and ExistentialOpExpr_438(encAB=encAB)):
                            return True
            return False
        _st_label_394 = 0
        while (_st_label_394 == 0):
            _st_label_394 += 1
            if ExistentialOpExpr_395():
                _st_label_394 += 1
            else:
                super()._label('_st_label_394', block=True)
                _st_label_394 -= 1
        self.output('B - Key Exchange Complete')
        self._state.terminate = True
    _RoleB_handler_360._labels = None
    _RoleB_handler_360._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([])

    def run(self):
        kAS = keygen('shared')
        kBS = keygen('shared')
        B = self.new(RoleB)
        A = self.new(RoleA)
        S = self.new(RoleS, (A, B, kAS, kBS))
        self._setup(A, (B, S, kAS))
        self._setup(B, (S, kBS))
        self._start(S)
        self._start(B)
        self._start(A)