from pyDes import *

#############################################################################
# 				Example				    #
#############################################################################
def _example_triple_des_():
	from time import time

	# Utility module
	from binascii import unhexlify as unhex

	# example shows triple-des encryption using the des class
	print ("Example of triple DES encryption in default ECB mode (DES-EDE3)\n")

	print ("Triple des using the des class (3 times)")
	t = time()
	k1 = des("security")
	#k1 = des(unhex("133457799BBCDFF1"))
	k2 = des(unhex("1122334455667788"))
	k3 = des(unhex("77661100DD223311"))
	d = "DES test string, to be encrypted and decrypted test....."
	print ("Key1:      %r" % k1.getKey())
	print ("Key2:      %r" % k2.getKey())
	print ("Key3:      %r" % k3.getKey())
	print ("Data:      %r" % d)

	e1 = k1.encrypt(d)
	e2 = k2.decrypt(e1)
	e3 = k3.encrypt(e2)
	print("***************Encrypted data ***********************")
	print ("Encrypted: %r" % e3)

	d3 = k3.decrypt(e3)
	d2 = k2.encrypt(d3)
	d1 = k1.decrypt(d2)
	print("***************Check the Decrypted data***********************")
	print ("Decrypted: %r" % d1)
	print ("DES time taken: %f (%d crypt operations)" % (time() - t, 6 * (len(d) / 8)))
	print ("")
if __name__ == '__main__':
	_example_triple_des_()
	