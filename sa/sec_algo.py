



class Sec_Algo():
      def __init__(): pass
      #end init()

      def gen_key_pair(): pass
      #end gen_key_pair()
      
      def get_pub_key(): pass
      #end get_pub_key()

      def gen_sym_key(): pass
      #end gen_sym_key()

      def sym_encrypt(plaintext, key): pass
      #end sym_encrypt()

      def sym_decrypt(plaintext, key): pass
      #end sym_decrypt()

      def asym_encrypt(plaintext, public_key): pass
      #end asym_encrypt()

      def asym_decrypt(plaintext, public_key, private_key): pass
      #end asym_decrypt()

      def encrypt(*plaintext, key): pass
      #end encrypt()

      def decrypt(plaintext, key): pass
      #end decrypt

      def sign(data, private_key): pass
      #end sign()

      def verify(data_and_sig, public_key): pass
      #end verify()
#end class Sec_Algo