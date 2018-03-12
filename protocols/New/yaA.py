# -*- generated by 1.0.12 -*-
import da
PatternExpr_190 = da.pat.TuplePattern([da.pat.ConstantPattern('msg2'), da.pat.FreePattern('i'), da.pat.TuplePattern([da.pat.BoundPattern('_BoundPattern195_'), da.pat.FreePattern('encBS')])])
PatternExpr_201 = da.pat.BoundPattern('_BoundPattern202_')
PatternExpr_294 = da.pat.TuplePattern([da.pat.ConstantPattern('msg3'), da.pat.BoundPattern('_BoundPattern297_'), da.pat.TuplePattern([da.pat.FreePattern('encSA'), da.pat.FreePattern('encSB')])])
PatternExpr_305 = da.pat.BoundPattern('_BoundPattern306_')
PatternExpr_389 = da.pat.TuplePattern([da.pat.ConstantPattern('msg1'), da.pat.FreePattern('i'), da.pat.TuplePattern([da.pat.FreePattern('A'), da.pat.FreePattern('nA')])])
PatternExpr_401 = da.pat.FreePattern('A')
PatternExpr_428 = da.pat.TuplePattern([da.pat.ConstantPattern('msg4'), da.pat.BoundPattern('_BoundPattern431_'), da.pat.TuplePattern([da.pat.FreePattern('encSB'), da.pat.FreePattern('encAB')])])
PatternExpr_439 = da.pat.BoundPattern('_BoundPattern440_')
_config_object = {}
from sa.secalgoB import *

class RoleS(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_RoleSReceivedEvent_0', PatternExpr_190, sources=[PatternExpr_201], destinations=None, timestamps=None, record_history=None, handlers=[self._RoleS_handler_189])])

    def setup(self, A, B, kAS, kBS, **rest_546):
        super().setup(A=A, B=B, kAS=kAS, kBS=kBS, **rest_546)
        self._state.A = A
        self._state.B = B
        self._state.kAS = kAS
        self._state.kBS = kBS
        at_fork()
        self._state.terminate = False

    @dec_proto_run_timer
    def run(self):
        self._state.terminate = False
        super()._label('_st_label_185', block=False)
        _st_label_185 = 0
        while (_st_label_185 == 0):
            _st_label_185 += 1
            if self._state.terminate:
                _st_label_185 += 1
            else:
                super()._label('_st_label_185', block=True)
                _st_label_185 -= 1

    def _RoleS_handler_189(self, i, encBS):
        nB = nA = None

        def ExistentialOpExpr_204():
            nonlocal nB, nA
            for (_BoundPattern207_, nA, nB) in [decrypt(encBS, key=self._state.kBS)]:
                if (_BoundPattern207_ == self._state.A):
                    if True:
                        return True
            return False
        if ExistentialOpExpr_204():
            kAB = keygen('shared')
            self.send(('msg3', i, (encrypt((self._state.B, kAB, nA, nB), key=self._state.kAS), encrypt((self._state.A, kAB), key=self._state.kBS))), to=self._state.A)
        self._state.terminate = True
    _RoleS_handler_189._labels = None
    _RoleS_handler_189._notlabels = None

class RoleA(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._RoleAReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_RoleAReceivedEvent_0', PatternExpr_294, sources=[PatternExpr_305], destinations=None, timestamps=None, record_history=True, handlers=[])])

    def setup(self, B, S, kAS, **rest_546):
        super().setup(B=B, S=S, kAS=kAS, **rest_546)
        self._state.B = B
        self._state.S = S
        self._state.kAS = kAS
        at_fork()
        self._state.i = 1

    @dec_proto_run_timer
    def run(self):
        nA = nonce()
        self.send(('msg1', self._state.i, (self._id, nA)), to=self._state.B)
        super()._label('_st_label_291', block=False)
        encSB = encSA = nB = kAB = None

        def ExistentialOpExpr_292():
            nonlocal encSB, encSA, nB, kAB
            for (_, (_, _, _BoundPattern313_), (_ConstantPattern315_, _BoundPattern317_, (encSA, encSB))) in self._RoleAReceivedEvent_0:
                if (_BoundPattern313_ == self._state.S):
                    if (_ConstantPattern315_ == 'msg3'):
                        if (_BoundPattern317_ == self._state.i):

                            def ExistentialOpExpr_322(encSA):
                                nonlocal nB, kAB
                                for (_BoundPattern325_, kAB, _BoundPattern328_, nB) in [decrypt(encSA, key=self._state.kAS)]:
                                    if (_BoundPattern325_ == self._state.B):
                                        if (_BoundPattern328_ == nA):
                                            if True:
                                                return True
                                return False
                            if ExistentialOpExpr_322(encSA=encSA):
                                return True
            return False
        _st_label_291 = 0
        while (_st_label_291 == 0):
            _st_label_291 += 1
            if ExistentialOpExpr_292():
                _st_label_291 += 1
            else:
                super()._label('_st_label_291', block=True)
                _st_label_291 -= 1
        self.send(('msg4', self._state.i, (encSB, encrypt(nB, key=kAB))), to=self._state.B)
        self.output('A - Key Exchange Complete')
        self._state.i += 1

class RoleB(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._RoleBReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_RoleBReceivedEvent_0', PatternExpr_389, sources=[PatternExpr_401], destinations=None, timestamps=None, record_history=None, handlers=[self._RoleB_handler_388]), da.pat.EventPattern(da.pat.ReceivedEvent, '_RoleBReceivedEvent_1', PatternExpr_428, sources=[PatternExpr_439], destinations=None, timestamps=None, record_history=True, handlers=[])])

    def setup(self, S, kBS, **rest_546):
        super().setup(S=S, kBS=kBS, **rest_546)
        self._state.S = S
        self._state.kBS = kBS
        at_fork()
        self._state.terminate = False

    @dec_proto_run_timer
    def run(self):
        self._state.terminate = False
        super()._label('_st_label_384', block=False)
        _st_label_384 = 0
        while (_st_label_384 == 0):
            _st_label_384 += 1
            if self._state.terminate:
                _st_label_384 += 1
            else:
                super()._label('_st_label_384', block=True)
                _st_label_384 -= 1

    def _RoleB_handler_388(self, i, A, nA):
        nB = nonce()
        self.send(('msg2', i, (self._id, encrypt((A, nA, nB), key=self._state.kBS))), to=self._state.S)
        super()._label('_st_label_425', block=False)
        encAB = encSB = kAB = None

        def ExistentialOpExpr_426():
            nonlocal encAB, encSB, kAB
            for (_, (_, _, _BoundPattern447_), (_ConstantPattern449_, _BoundPattern451_, (encSB, encAB))) in self._RoleBReceivedEvent_1:
                if (_BoundPattern447_ == A):
                    if (_ConstantPattern449_ == 'msg4'):
                        if (_BoundPattern451_ == i):

                            def ExistentialOpExpr_457(encSB):
                                nonlocal kAB
                                for (_BoundPattern460_, kAB) in [decrypt(encSB, key=self._state.kBS)]:
                                    if (_BoundPattern460_ == A):
                                        if True:
                                            return True
                                return False

                            def ExistentialOpExpr_471(encAB):
                                for _BoundPattern474_ in [decrypt(encAB, key=kAB)]:
                                    if (_BoundPattern474_ == nB):
                                        if True:
                                            return True
                                return False
                            if (ExistentialOpExpr_457(encSB=encSB) and ExistentialOpExpr_471(encAB=encAB)):
                                return True
            return False
        _st_label_425 = 0
        while (_st_label_425 == 0):
            _st_label_425 += 1
            if ExistentialOpExpr_426():
                _st_label_425 += 1
            else:
                super()._label('_st_label_425', block=True)
                _st_label_425 -= 1
        self.output('B - Key Exchange Complete')
        self._state.terminate = True
    _RoleB_handler_388._labels = None
    _RoleB_handler_388._notlabels = None

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