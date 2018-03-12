# -*- generated by 1.0.12 -*-
import da
PatternExpr_1481 = da.pat.TuplePattern([da.pat.BoundPattern('_BoundPattern1482_'), da.pat.FreePattern('msg'), da.pat.BoundPattern('_BoundPattern1485_'), da.pat.FreePattern('counter')])
PatternExpr_1490 = da.pat.FreePattern('server')
PatternExpr_2268 = da.pat.TuplePattern([da.pat.FreePattern('i2'), da.pat.TuplePattern([da.pat.ConstantPattern(22), da.pat.BoundPattern('_BoundPattern2273_'), da.pat.ConstantPattern(None), da.pat.FreePattern('cipher_fragment')]), da.pat.FreePattern('handshake_id'), da.pat.FreePattern('counter')])
PatternExpr_2285 = da.pat.FreePattern('client')
PatternExpr_2528 = da.pat.TuplePattern([da.pat.BoundPattern('_BoundPattern2529_'), da.pat.FreePattern('msg'), da.pat.BoundPattern('_BoundPattern2532_'), da.pat.FreePattern('counter')])
PatternExpr_2536 = da.pat.FreePattern('client')
PatternExpr_2888 = da.pat.TuplePattern([da.pat.FreePattern('i3'), da.pat.TuplePattern([da.pat.ConstantPattern(20), da.pat.BoundPattern('_BoundPattern2893_'), da.pat.ConstantPattern(None), da.pat.FreePattern('cipher_fragment')]), da.pat.FreePattern('handshake_id'), da.pat.FreePattern('msg_counter')])
_config_object = {}
import time, sys, pickle
from Crypto.Hash import SHA256
from Crypto.Hash import HMAC
from sa.secalgoB import *
configure(verify_returns='bool')
PROTOCOL_VERSION_3_0 = (3, 0)
PROTOCOL_VERSION_1_0 = (3, 1)
PROTOCOL_VERSION_1_1 = (3, 2)
PROTOCOL_VERSION_1_2 = (3, 3)
TYPE_CHANGE_CIPHER_SPEC = 20
TYPE_ALERT = 21
TYPE_HANDSHAKE = 22
TYPE_APPLICATION_DATA = 23
VERIFY_DATA_LENGTH = 12
CHANGE_CIPHER_SPEC_BODY = 1
HELLO_REQUEST = 0
CLIENT_HELLO = 1
SERVER_HELLO = 2
CERTIFICATE = 11
SERVER_KEY_EXCHANGE = 12
CERTIFICATE_REQUEST = 13
SERVER_HELLO_DONE = 14
CERTIFICATE_VERIFY = 15
CLIENT_KEY_EXCHANGE = 16
FINISHED = 20
RSA_SIGN = 1
DSS_SIGN = 2
RSA_FIXED_DH = 3
DSS_FIXED_DH = 4
RSA_EPHEMERAL_DH_RESERVED = 5
DSS_EPHEMERAL_DH_RESERVED = 6
FORTEZZA_DMS_RESERVED = 20
CONN_SERVER = 0
CONN_CLIENT = 1
TLS_PRF_SHA256 = 0
CIPHER_STREAM = 0
CIPHER_BLOCK = 1
CIPHER_AEAD = 2
BULK_NULL = 0
BULK_RC4 = 1
BULK_3DES = 2
BULK_AES = 3
MAC_NULL = 0
MAC_HMAC_MD5 = 1
MAC_HMAC_SHA1 = 2
MAC_HMAC_SHA256 = 3
MAC_HMAC_SHA384 = 4
MAC_HMAC_SHA512 = 5
COMP_NULL = 0
TLS_NULL_WITH_NULL_NULL = (0, 0)
TLS_RSA_WITH_AES_128_CBC_SHA256 = (0, 60)
TLS_RSA_WITH_AES_256_CBC_SHA256 = (0, 61)
SIG_ANONYMOUS = 0
SIG_RSA = 1
SIG_DSA = 2
SIG_ECDSA = 3
HASH_NONE = 0
HASH_MD5 = 1
HASH_SHA1 = 2
HASH_SHA224 = 3
HASH_SHA256 = 4
HASH_SHA384 = 5
HASH_SHA512 = 6
KE_NULL = 0
KE_RSA = 1
KE_DH_DSS = 2
KE_DH_RSA = 3
KE_DHE_DSS = 4
KE_DHE_DSS = 5
KE_DH_ANON = 6

def _a(n, secret, seed):
    if (n == 0):
        return seed
    else:
        h = HMAC.new(secret, digestmod=SHA256)
        h.update(_a((n - 1), secret, seed))
        return h.digest()

def _p_hash(secret, seed, output_length):
    result = bytearray()
    i = 1
    while (len(result) < output_length):
        h = HMAC.new(secret, digestmod=SHA256)
        h.update(_a(i, secret, seed))
        h.update(seed)
        result.extend(h.digest())
        i += 1
    return bytes(result[:output_length])

def tls_prf_sha256(secret, label, seed, output_length):
    return _p_hash(secret, (label + seed), output_length)

class Security_Parameters():

    def __init__(self, ce):
        self.connection_end = ce
        self.prf_algorithm = TLS_PRF_SHA256
        self.bulk_cipher_algorithm = BULK_NULL
        self.cipher_type = CIPHER_STREAM
        self.enc_key_length = 0
        self.block_length = None
        self.fixed_iv_length = 0
        self.record_iv_length = 0
        self.mac_algorithm = MAC_NULL
        self.mac_length = 0
        self.mac_key_length = 0
        self.compression_method = COMP_NULL
        self.master_secret = None
        self.client_random = None
        self.server_random = None

class Connection_State():

    def __init__(self):
        self.compression_state = None
        self.cipher_state = None
        self.mac_key = None
        self.sequence_number = 0

class TLS_Peer(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._TLS_PeerReceivedEvent_0 = []
        self._TLS_PeerReceivedEvent_2 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_TLS_PeerReceivedEvent_0', PatternExpr_1481, sources=[PatternExpr_1490], destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_TLS_PeerReceivedEvent_1', PatternExpr_2268, sources=[PatternExpr_2285], destinations=None, timestamps=None, record_history=None, handlers=[self._TLS_Peer_handler_2267]), da.pat.EventPattern(da.pat.ReceivedEvent, '_TLS_PeerReceivedEvent_2', PatternExpr_2528, sources=[PatternExpr_2536], destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_TLS_PeerReceivedEvent_3', PatternExpr_2888, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._TLS_Peer_handler_2887])])

    def setup(self, ce, peer, secret_key, public_key, certificate_list, **rest_3034):
        super().setup(ce=ce, peer=peer, secret_key=secret_key, public_key=public_key, certificate_list=certificate_list, **rest_3034)
        self._state.ce = ce
        self._state.peer = peer
        self._state.secret_key = secret_key
        self._state.public_key = public_key
        self._state.certificate_list = certificate_list
        self._state.terminate = False
        self._state.i = 1
        self._state.max_hs_id = 0
        self._state.supported_tls_versions = (PROTOCOL_VERSION_1_2,)
        self._state.supported_cipher_suites = (TLS_RSA_WITH_AES_256_CBC_SHA256,)
        self._state.supported_compression_methods = (COMP_NULL,)
        self._state.current_rsp = Security_Parameters(self._state.ce)
        self._state.current_wsp = Security_Parameters(self._state.ce)
        self._state.pending_rsp = Security_Parameters(self._state.ce)
        self._state.pending_wsp = Security_Parameters(self._state.ce)
        self._state.current_read_state = Connection_State()
        self._state.current_write_state = Connection_State()
        self._state.pending_read_state = Connection_State()
        self._state.pending_write_state = Connection_State()

    @dec_proto_run_timer
    def run(self):
        if (not (self._state.peer == None)):
            self.initiate_handshake(self._state.peer)
            self._state.i += 1
        else:
            self._state.terminate = False
            super()._label('_st_label_2942', block=False)
            _st_label_2942 = 0
            while (_st_label_2942 == 0):
                _st_label_2942 += 1
                if self._state.terminate:
                    _st_label_2942 += 1
                else:
                    super()._label('_st_label_2942', block=True)
                    _st_label_2942 -= 1

    def reset_security_parameters_and_state(self, ce):
        self._state.current_rsp = Security_Parameters(ce)
        self._state.current_wsp = Security_Parameters(ce)
        self._state.pending_rsp = Security_Parameters(ce)
        self._state.pending_wsp = Security_Parameters(ce)
        self._state.current_read_state = Connection_State()
        self._state.current_write_state = Connection_State()
        self._state.pending_read_state = Connection_State()
        self._state.pending_write_state = Connection_State()

    def record_wrapper(self, content_type, tls_message):
        version = PROTOCOL_VERSION_1_2
        pt_fragment = tls_message
        pt_length = None
        tls_pt = (content_type, version, pt_length, pt_fragment)
        comp_length = pt_length
        if (not (self._state.current_wsp.compression_method == COMP_NULL)):
            comp_fragment = self._state.current_wsp.compression_method(pt_fragment)
        else:
            comp_fragment = pt_fragment
        tls_comp = (content_type, version, comp_length, comp_fragment)
        cipher_length = comp_length
        if (self._state.current_wsp.cipher_type == CIPHER_STREAM):
            if (self._state.current_wsp.mac_algorithm == MAC_NULL):
                cipher_mac = b''
            else:
                cipher_mac = sign((self._state.current_write_state.sequence_number, content_type, version, comp_length, comp_fragment), key=self._state.current_write_state.mac_key)
            stream_ciphered = (comp_fragment, cipher_mac)
            if (not (self._state.current_wsp.bulk_cipher_algorithm == BULK_NULL)):
                cipher_fragment = encrypt(stream_ciphered, key=self._state.current_write_state.cipher_state[0])
            else:
                cipher_fragment = stream_ciphered
        elif (self._state.current_wsp.cipher_type == CIPHER_BLOCK):
            iv = keygen('random', self._state.current_wsp.record_iv_length)
            if (self._state.current_wsp.mac_algorithm == MAC_NULL):
                cipher_mac = b''
            else:
                cipher_mac = sign((self._state.current_write_state.sequence_number, content_type, version, comp_length, comp_fragment), key=self._state.current_write_state.mac_key)
            cipher_padding = b''
            cipher_pad_length = 0
            block_ciphered = (comp_fragment, cipher_mac, cipher_padding, cipher_pad_length)
            cipher_fragment = (iv, encrypt(block_ciphered, key=self._state.current_write_state.cipher_state[0]))
        tls_cipher = (content_type, version, cipher_length, cipher_fragment)
        return tls_cipher

    def record_unwrapper(self, tls_cipher):
        (content_type, version, cipher_length, cipher_fragment) = tls_cipher
        if (not (version == PROTOCOL_VERSION_1_2)):
            return
        if (self._state.current_rsp.cipher_type == CIPHER_STREAM):
            if (self._state.current_rsp.bulk_cipher_algorithm == BULK_NULL):
                (comp_fragment, cipher_mac) = cipher_fragment
            else:
                (comp_fragment, cipher_mac) = decrypt(cipher_fragment, key=self._state.current_read_state.cipher_state[0])
        elif (self._state.current_rsp.cipher_type == CIPHER_BLOCK):
            (iv, block_ciphered) = cipher_fragment
            (comp_fragment, cipher_mac, cipher_padding, cipher_pad_length) = decrypt(block_ciphered, key=self._state.current_read_state.cipher_state[0])
        comp_length = cipher_length
        if (not (self._state.current_rsp.mac_algorithm == MAC_NULL)):
            if (not verify(((self._state.current_read_state.sequence_number, content_type, version, comp_length, comp_fragment), cipher_mac), key=self._state.current_read_state.mac_key)):
                self.output('MAC VERIFICATION ERROR')
                return
        pt_length = comp_length
        if (not (self._state.current_rsp.compression_method == COMP_NULL)):
            pt_fragment = self._state.current_rsp.compression_method(comp_fragment, 'decompress')
        else:
            pt_fragment = comp_fragment
        return pt_fragment

    def update_pending_parameters(self, cipher_suite, comp_method, crand, srand):
        self._state.pending_rsp.compression_method = comp_method
        self._state.pending_rsp.client_random = crand
        self._state.pending_rsp.server_random = srand
        self._state.pending_wsp.compression_method = comp_method
        self._state.pending_wsp.client_random = crand
        self._state.pending_wsp.server_random = srand
        if (cipher_suite == TLS_RSA_WITH_AES_256_CBC_SHA256):
            self._state.pending_rsp.bulk_cipher_algorithm = BULK_AES
            self._state.pending_rsp.cipher_type = CIPHER_BLOCK
            self._state.pending_rsp.enc_key_length = 32
            self._state.pending_rsp.block_length = 16
            self._state.pending_rsp.fixed_iv_length = 16
            self._state.pending_rsp.record_iv_length = 16
            self._state.pending_rsp.mac_algorithm = MAC_HMAC_SHA256
            self._state.pending_rsp.mac_length = 32
            self._state.pending_rsp.mac_key_length = 32
            self._state.pending_wsp.bulk_cipher_algorithm = BULK_AES
            self._state.pending_wsp.cipher_type = CIPHER_BLOCK
            self._state.pending_wsp.enc_key_length = 32
            self._state.pending_wsp.block_length = 16
            self._state.pending_wsp.fixed_iv_length = 16
            self._state.pending_wsp.record_iv_length = 16
            self._state.pending_wsp.mac_algorithm = MAC_HMAC_SHA256
            self._state.pending_wsp.mac_length = 32
            self._state.pending_wsp.mac_key_length = 32
            return KE_RSA
        return KE_NULL

    def update_connection_state(self):
        key_block_length = (2 * (self._state.pending_wsp.enc_key_length + self._state.pending_wsp.mac_key_length))
        key_block = tls_prf_sha256(self._state.pending_wsp.master_secret, b'key expansion', (self._state.pending_wsp.client_random + self._state.pending_wsp.server_random), key_block_length)
        first_slice = self._state.pending_wsp.mac_key_length
        second_slice = (first_slice + self._state.pending_wsp.mac_key_length)
        third_slice = (second_slice + self._state.pending_wsp.enc_key_length)
        fourth_slice = (third_slice + self._state.pending_wsp.enc_key_length)
        first_block = key_block[:first_slice]
        second_block = key_block[first_slice:second_slice]
        third_block = key_block[second_slice:third_slice]
        fourth_block = key_block[third_slice:]
        if (self._state.pending_wsp.connection_end == CONN_CLIENT):
            self._state.pending_write_state.mac_key = keygen('mac', key_mat=first_block)
            self._state.pending_read_state.mac_key = keygen('mac', key_mat=second_block)
            self._state.pending_write_state.cipher_state = [keygen('shared', key_mat=third_block)]
            self._state.pending_read_state.cipher_state = [keygen('shared', key_mat=fourth_block)]
        else:
            self._state.pending_read_state.mac_key = keygen('mac', key_mat=first_block)
            self._state.pending_write_state.mac_key = keygen('mac', key_mat=second_block)
            self._state.pending_read_state.cipher_state = [keygen('shared', key_mat=third_block)]
            self._state.pending_write_state.cipher_state = [keygen('shared', key_mat=fourth_block)]

    def initiate_handshake(self, server):
        i1 = self._state.i
        self.output('CLIENT - begin Handshake')
        handshake_id = (self._id, self._state.max_hs_id)
        self._state.max_hs_id += 1
        msg_counter = 0
        handshake_messages = []
        self._state.current_rsp.connection_end = CONN_CLIENT
        self._state.current_wsp.connection_end = CONN_CLIENT
        self._state.pending_rsp.connection_end = CONN_CLIENT
        self._state.pending_wsp.connection_end = CONN_CLIENT
        client_random = (time.time(), keygen('random', 28))
        body_ch = (PROTOCOL_VERSION_1_2, client_random, None, (TLS_RSA_WITH_AES_256_CBC_SHA256,), (0,), None)
        handshake_ch = (CLIENT_HELLO, None, body_ch)
        handshake_messages.append(handshake_ch)
        msg_counter += 1
        self.send((i1, self.record_wrapper(TYPE_HANDSHAKE, handshake_ch), handshake_id, msg_counter), to=server)
        super()._label('_st_label_1478', block=False)
        msg = counter = server = None

        def ExistentialOpExpr_1479():
            nonlocal msg, counter, server
            for (_, (_, _, server), (_BoundPattern1500_, msg, _BoundPattern1502_, counter)) in self._TLS_PeerReceivedEvent_0:
                if (_BoundPattern1500_ == i1):
                    if (_BoundPattern1502_ == handshake_id):
                        if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (SERVER_HELLO == self.record_unwrapper(msg)[0])):
                            return True
            return False
        _st_label_1478 = 0
        while (_st_label_1478 == 0):
            _st_label_1478 += 1
            if ExistentialOpExpr_1479():
                _st_label_1478 += 1
            else:
                super()._label('_st_label_1478', block=True)
                _st_label_1478 -= 1
        msg_counter = counter
        handshake_sh = self.record_unwrapper(msg)
        handshake_messages.append(handshake_sh)
        (_, _, body_sh) = handshake_sh
        (server_version, server_random, session_id, cipher_suite, compression_method, extensions) = body_sh
        if (not (server_version == PROTOCOL_VERSION_1_2)):
            return
        key_exchange_alg = self.update_pending_parameters(cipher_suite, compression_method, client_random[1], server_random[1])
        if (not (key_exchange_alg in {KE_NULL, KE_DH_ANON})):
            super()._label('_st_label_1585', block=False)
            msg = counter = server = None

            def ExistentialOpExpr_1586():
                nonlocal msg, counter, server
                for (_, (_, _, server), (_BoundPattern1605_, msg, _BoundPattern1607_, counter)) in self._TLS_PeerReceivedEvent_0:
                    if (_BoundPattern1605_ == i1):
                        if (_BoundPattern1607_ == handshake_id):
                            if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (CERTIFICATE == self.record_unwrapper(msg)[0])):
                                return True
                return False
            _st_label_1585 = 0
            while (_st_label_1585 == 0):
                _st_label_1585 += 1
                if ExistentialOpExpr_1586():
                    _st_label_1585 += 1
                else:
                    super()._label('_st_label_1585', block=True)
                    _st_label_1585 -= 1
            msg_counter = counter
            handshake_sc = self.record_unwrapper(msg)
            handshake_messages.append(handshake_sc)
            (_, _, body_cert) = handshake_sc
            (cert_list,) = body_cert
            verdict = True
            for (self._state.i, cert) in enumerate(cert_list):
                if (self._state.i < (len(cert_list) - 1)):
                    if (not verify(((cert[0], cert[1]), cert[2]), key=cert_list[(self._state.i + 1)][1])):
                        verdict = False
                elif (not verify(((cert[0], cert[1]), cert[2]), key=cert[1])):
                    verdict = False
            if (not verdict):
                self.output('CLIENT - CERTIFICATE AUTHENTICATION FAILURE')
                return
            server_public_key = cert_list[0][1]
        if (not (key_exchange_alg in {KE_NULL, KE_RSA, KE_DH_DSS, KE_DH_RSA})):
            super()._label('_st_label_1743', block=False)
            msg = counter = server = None

            def ExistentialOpExpr_1744():
                nonlocal msg, counter, server
                for (_, (_, _, server), (_BoundPattern1763_, msg, _BoundPattern1765_, counter)) in self._TLS_PeerReceivedEvent_0:
                    if (_BoundPattern1763_ == i1):
                        if (_BoundPattern1765_ == handshake_id):
                            if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (SERVER_KEY_EXCHANGE == self.record_unwrapper(msg)[0])):
                                return True
                return False
            _st_label_1743 = 0
            while (_st_label_1743 == 0):
                _st_label_1743 += 1
                if ExistentialOpExpr_1744():
                    _st_label_1743 += 1
                else:
                    super()._label('_st_label_1743', block=True)
                    _st_label_1743 -= 1
            msg_counter = counter
            pass
        if (not (key_exchange_alg in {KE_NULL, KE_DH_ANON})):
            super()._label('_st_label_1796', block=False)
            msg = counter = server = None

            def ExistentialOpExpr_1797():
                nonlocal msg, counter, server
                for (_, (_, _, server), (_BoundPattern1816_, msg, _BoundPattern1818_, counter)) in self._TLS_PeerReceivedEvent_0:
                    if (_BoundPattern1816_ == i1):
                        if (_BoundPattern1818_ == handshake_id):
                            if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (CERTIFICATE_REQUEST == self.record_unwrapper(msg)[0])):
                                return True
                return False
            msg = counter = server = None

            def ExistentialOpExpr_1842():
                nonlocal msg, counter, server
                for (_, (_, _, server), (_BoundPattern1861_, msg, _BoundPattern1863_, counter)) in self._TLS_PeerReceivedEvent_0:
                    if (_BoundPattern1861_ == i1):
                        if (_BoundPattern1863_ == handshake_id):
                            if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (SERVER_HELLO_DONE == self.record_unwrapper(msg)[0])):
                                return True
                return False
            _st_label_1796 = 0
            while (_st_label_1796 == 0):
                _st_label_1796 += 1
                if ExistentialOpExpr_1797():
                    msg_counter = counter
                    pass
                    _st_label_1796 += 1
                elif ExistentialOpExpr_1842():
                    pass
                    _st_label_1796 += 1
                else:
                    super()._label('_st_label_1796', block=True)
                    _st_label_1796 -= 1
        super()._label('_st_label_1884', block=False)
        msg = counter = server = None

        def ExistentialOpExpr_1885():
            nonlocal msg, counter, server
            for (_, (_, _, server), (_BoundPattern1904_, msg, _BoundPattern1906_, counter)) in self._TLS_PeerReceivedEvent_0:
                if (_BoundPattern1904_ == i1):
                    if (_BoundPattern1906_ == handshake_id):
                        if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (SERVER_HELLO_DONE == self.record_unwrapper(msg)[0])):
                            return True
            return False
        _st_label_1884 = 0
        while (_st_label_1884 == 0):
            _st_label_1884 += 1
            if ExistentialOpExpr_1885():
                _st_label_1884 += 1
            else:
                super()._label('_st_label_1884', block=True)
                _st_label_1884 -= 1
        msg_counter = counter
        handshake_shd = self.record_unwrapper(msg)
        handshake_messages.append(handshake_shd)
        pre_master_secret = (PROTOCOL_VERSION_1_2, keygen('random', 46))
        encrypted_pre_master_secret = (encrypt(pre_master_secret, key=server_public_key),)
        body_cke = (encrypted_pre_master_secret,)
        handshake_cke = (CLIENT_KEY_EXCHANGE, None, body_cke)
        handshake_messages.append(handshake_cke)
        msg_counter += 1
        self.send((i1, self.record_wrapper(TYPE_HANDSHAKE, handshake_cke), handshake_id, msg_counter), to=server)
        pms = (bytes(pre_master_secret[0]) + pre_master_secret[1])
        msecret = tls_prf_sha256(pms, b'master secret', (self._state.pending_wsp.client_random + self._state.pending_wsp.server_random), 48)
        self._state.pending_wsp.master_secret = msecret
        self._state.pending_rsp.master_secret = msecret
        self.update_connection_state()
        handshake_ccs = (CHANGE_CIPHER_SPEC_BODY,)
        msg_counter += 1
        self.send((i1, self.record_wrapper(TYPE_CHANGE_CIPHER_SPEC, handshake_ccs), handshake_id, msg_counter), to=server)
        self._state.current_wsp = self._state.pending_wsp
        self._state.current_write_state = self._state.pending_write_state
        self._state.pending_wsp = Security_Parameters(self._state.current_wsp.connection_end)
        self._state.pending_write_state = Connection_State()
        shm = b''
        m_count = 1
        for m in handshake_messages:
            shm += (b'msg' + str(m_count).encode('ascii'))
            m_count += 1
        verification_data = tls_prf_sha256(self._state.current_wsp.master_secret, b'client finished', SHA256.new(shm).digest(), VERIFY_DATA_LENGTH)
        finished = (verification_data,)
        handshake_cfin = (FINISHED, None, finished)
        handshake_messages.append(handshake_cfin)
        shm += (b'msg' + str(m_count).encode('ascii'))
        msg_counter += 1
        self.send((i1, self.record_wrapper(TYPE_HANDSHAKE, handshake_cfin), handshake_id, msg_counter), to=server)
        super()._label('_st_label_2142', block=False)
        msg = counter = server = None

        def ExistentialOpExpr_2143():
            nonlocal msg, counter, server
            for (_, (_, _, server), (_BoundPattern2162_, msg, _BoundPattern2164_, counter)) in self._TLS_PeerReceivedEvent_0:
                if (_BoundPattern2162_ == i1):
                    if (_BoundPattern2164_ == handshake_id):
                        if ((msg[0] == TYPE_CHANGE_CIPHER_SPEC) and (counter > msg_counter)):
                            return True
            return False
        _st_label_2142 = 0
        while (_st_label_2142 == 0):
            _st_label_2142 += 1
            if ExistentialOpExpr_2143():
                _st_label_2142 += 1
            else:
                super()._label('_st_label_2142', block=True)
                _st_label_2142 -= 1
        msg_counter = counter
        super()._label('_st_label_2180', block=False)
        msg = counter = server = None

        def ExistentialOpExpr_2181():
            nonlocal msg, counter, server
            for (_, (_, _, server), (_BoundPattern2200_, msg, _BoundPattern2202_, counter)) in self._TLS_PeerReceivedEvent_0:
                if (_BoundPattern2200_ == i1):
                    if (_BoundPattern2202_ == handshake_id):
                        if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (FINISHED == self.record_unwrapper(msg)[0])):
                            return True
            return False
        _st_label_2180 = 0
        while (_st_label_2180 == 0):
            _st_label_2180 += 1
            if ExistentialOpExpr_2181():
                _st_label_2180 += 1
            else:
                super()._label('_st_label_2180', block=True)
                _st_label_2180 -= 1
        msg_counter = counter
        (_, _, (finish_data,)) = self.record_unwrapper(msg)
        client_data = tls_prf_sha256(self._state.current_rsp.master_secret, b'server finished', SHA256.new(shm).digest(), VERIFY_DATA_LENGTH)
        if (not (client_data == finish_data)):
            self.output('CLIENT - Handshake Failed')
            return
        self.reset_security_parameters_and_state(self._state.ce)
        self.output('CLIENT - Handshake complete')

    def _TLS_Peer_handler_2267(self, i2, cipher_fragment, handshake_id, counter, client):
        msg_counter = counter
        handshake_messages = []
        handshake_msg = self.record_unwrapper((TYPE_HANDSHAKE, PROTOCOL_VERSION_1_2, None, cipher_fragment))
        if (not (CLIENT_HELLO == handshake_msg[0])):
            return
        self.output('SERVER - begin Handshake')
        self._state.current_rsp.connection_end = CONN_SERVER
        self._state.current_wsp.connection_end = CONN_SERVER
        self._state.pending_rsp.connection_end = CONN_SERVER
        self._state.pending_wsp.connection_end = CONN_SERVER
        handshake_messages.append(handshake_msg)
        (client_version, client_random, session_id, cipher_suites, compression_methods, extensions) = handshake_msg[2]
        server_version = min(client_version, max(self._state.supported_tls_versions))
        server_random = (time.time(), keygen('random', 28))
        if (not (session_id == None)):
            self.output('Client attempting abbreivated handshake.')
        else:
            session_id = None
            cipher_suite = {suite for suite in cipher_suites for _FreePattern2394_ in self._state.supported_cipher_suites if (_FreePattern2394_ == suite)}.pop()
            compression_method = {method for method in compression_methods for _FreePattern2410_ in self._state.supported_compression_methods if (_FreePattern2410_ == method)}.pop()
            body_sh = (server_version, server_random, session_id, cipher_suite, compression_method, extensions)
            handshake_sh = (SERVER_HELLO, None, body_sh)
            handshake_messages.append(handshake_sh)
            msg_counter += 1
            self.send((i2, self.record_wrapper(TYPE_HANDSHAKE, handshake_sh), handshake_id, msg_counter), to=client)
            key_exchange_alg = self.update_pending_parameters(cipher_suite, compression_method, client_random[1], server_random[1])
            body_sc = (self._state.certificate_list,)
            handshake_sc = (CERTIFICATE, None, body_sc)
            handshake_messages.append(handshake_sc)
            msg_counter += 1
            self.send((i2, self.record_wrapper(TYPE_HANDSHAKE, handshake_sc), handshake_id, msg_counter), to=client)
            body_shd = ()
            handshake_shd = (SERVER_HELLO_DONE, None, body_shd)
            handshake_messages.append(handshake_shd)
            msg_counter += 1
            self.send((i2, self.record_wrapper(TYPE_HANDSHAKE, handshake_shd), handshake_id, msg_counter), to=client)
            super()._label('_st_label_2525', block=False)
            msg = client = counter = None

            def ExistentialOpExpr_2526():
                nonlocal msg, client, counter
                for (_, (_, _, client), (_BoundPattern2546_, msg, _BoundPattern2548_, counter)) in self._TLS_PeerReceivedEvent_2:
                    if (_BoundPattern2546_ == i2):
                        if (_BoundPattern2548_ == handshake_id):
                            if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (CLIENT_KEY_EXCHANGE == self.record_unwrapper(msg)[0])):
                                return True
                return False
            _st_label_2525 = 0
            while (_st_label_2525 == 0):
                _st_label_2525 += 1
                if ExistentialOpExpr_2526():
                    _st_label_2525 += 1
                else:
                    super()._label('_st_label_2525', block=True)
                    _st_label_2525 -= 1
            msg_counter = counter
            handshake_cke = self.record_unwrapper(msg)
            handshake_messages.append(handshake_cke)
            (_, _, body_cke) = handshake_cke
            pre_master_secret = decrypt(body_cke[0][0], key=self._state.secret_key)
            pms = (bytes(pre_master_secret[0]) + pre_master_secret[1])
            msecret = tls_prf_sha256(pms, b'master secret', (self._state.pending_wsp.client_random + self._state.pending_wsp.server_random), 48)
            self._state.pending_wsp.master_secret = msecret
            self._state.pending_rsp.master_secret = msecret
            self.update_connection_state()
            super()._label('_st_label_2638', block=False)
            msg = client = counter = None

            def ExistentialOpExpr_2639():
                nonlocal msg, client, counter
                for (_, (_, _, client), (_BoundPattern2658_, msg, _BoundPattern2660_, counter)) in self._TLS_PeerReceivedEvent_2:
                    if (_BoundPattern2658_ == i2):
                        if (_BoundPattern2660_ == handshake_id):
                            if ((msg[0] == TYPE_CHANGE_CIPHER_SPEC) and (counter > msg_counter)):
                                return True
                return False
            _st_label_2638 = 0
            while (_st_label_2638 == 0):
                _st_label_2638 += 1
                if ExistentialOpExpr_2639():
                    _st_label_2638 += 1
                else:
                    super()._label('_st_label_2638', block=True)
                    _st_label_2638 -= 1
            msg_counter = counter
            super()._label('_st_label_2676', block=False)
            msg = client = counter = None

            def ExistentialOpExpr_2677():
                nonlocal msg, client, counter
                for (_, (_, _, client), (_BoundPattern2696_, msg, _BoundPattern2698_, counter)) in self._TLS_PeerReceivedEvent_2:
                    if (_BoundPattern2696_ == i2):
                        if (_BoundPattern2698_ == handshake_id):
                            if ((msg[0] == TYPE_HANDSHAKE) and (counter > msg_counter) and (FINISHED == self.record_unwrapper(msg)[0])):
                                return True
                return False
            _st_label_2676 = 0
            while (_st_label_2676 == 0):
                _st_label_2676 += 1
                if ExistentialOpExpr_2677():
                    _st_label_2676 += 1
                else:
                    super()._label('_st_label_2676', block=True)
                    _st_label_2676 -= 1
            msg_counter = counter
            handshake_cfin = self.record_unwrapper(msg)
            (_, _, (finish_data,)) = handshake_cfin
            shm = b''
            m_count = 1
            for m in handshake_messages:
                shm += (b'msg' + str(m_count).encode('ascii'))
                m_count += 1
            server_data = tls_prf_sha256(self._state.current_rsp.master_secret, b'client finished', SHA256.new(shm).digest(), VERIFY_DATA_LENGTH)
            if (not (server_data == finish_data)):
                self.output('SERVER - Handshake failed')
                return
            handshake_messages.append(handshake_cfin)
            shm += (b'msg' + str(m_count).encode('ascii'))
            handshake_ccs = (CHANGE_CIPHER_SPEC_BODY,)
            msg_counter += 1
            self.send((i2, self.record_wrapper(TYPE_CHANGE_CIPHER_SPEC, handshake_ccs), handshake_id, msg_counter), to=client)
            self._state.current_wsp = self._state.pending_wsp
            self._state.current_write_state = self._state.pending_write_state
            self._state.pending_wsp = Security_Parameters(self._state.current_wsp.connection_end)
            self._state.pending_write_state = Connection_State()
            verification_data = tls_prf_sha256(self._state.current_wsp.master_secret, b'server finished', SHA256.new(shm).digest(), VERIFY_DATA_LENGTH)
            finished = (verification_data,)
            handshake_sfin = (FINISHED, None, finished)
            msg_counter += 1
            self.send((i2, self.record_wrapper(TYPE_HANDSHAKE, handshake_sfin), handshake_id, msg_counter), to=client)
            self.reset_security_parameters_and_state(self._state.ce)
            self.output('SERVER - Handshake Complete')
        self._state.terminate = True
    _TLS_Peer_handler_2267._labels = None
    _TLS_Peer_handler_2267._notlabels = None

    def _TLS_Peer_handler_2887(self, i3, cipher_fragment, handshake_id, msg_counter):
        self.output('CHANGE_CIPHER_SPEC!!!!!!!!!!!!!!!!!!!')
        self._state.current_rsp = self._state.pending_rsp
        self._state.current_read_state = self._state.pending_read_state
        self._state.pending_rsp = Security_Parameters(self._state.current_rsp.connection_end)
        self._state.pending_read_state = Connection_State()
    _TLS_Peer_handler_2887._labels = None
    _TLS_Peer_handler_2887._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([])
    _config_object = {'channel': 'reliable'}

    def run(self):
        tls_server = self.new(TLS_Peer)
        tls_client = self.new(TLS_Peer)
        (sk_root, pk_root) = keygen('public')
        (sk_server, pk_server) = keygen('public')
        server_certificate = ('server', pk_server, sign(('server', pk_server), key=sk_root))
        root_certificate = ('root', pk_root, sign(('root', pk_root), key=sk_root))
        certificate_list = (server_certificate, root_certificate)
        self._setup(tls_server, (CONN_SERVER, None, sk_server, pk_server, certificate_list))
        self._setup(tls_client, (CONN_CLIENT, tls_server, None, None, None))
        self._start(tls_server)
        self._start(tls_client)