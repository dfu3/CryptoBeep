import time

__author__ = 'dfu3'

import os
import Image, binascii, math
import django.utils.crypto


file = open("superSmallDataSet.txt", "r")

cont = file.read()

hexString = binascii.hexlify(cont)

encryptMess = str(bin(int(hexString, 16)))
encryptMess = encryptMess[2:]


dur = .1   #duration in seconds
one = 500  #frequency in hertz
zero = 0


cipherKey = ""
finalCrypt = ""

foundBadSym = True

while( foundBadSym == True ):

    preKey = django.utils.crypto.get_random_string(len(cont), allowed_chars='abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()')
    hexString2 = binascii.hexlify(preKey)

    cipherKey = str(bin(int(hexString2, 16)))
    cipherKey = cipherKey[2:]

    numCrypt = int(encryptMess, 2) ^ int(cipherKey, 2)
    finalCrypt = '{0:b}'.format(numCrypt)

    binVal = (int(finalCrypt, 2) ^ int(cipherKey, 2))

    hexString = ""
    hexString += (hex(binVal)[2:-1])
    decryptMess = binascii.unhexlify(hexString)

    symbols = cont

    foundBadSym = False

    for elem in decryptMess:
        if(elem not in symbols):
            foundBadSym = True


import subprocess
cmd = ['ssh', 'root@69.28.93.232', 'mkdir -p output/dir; cat - > output/dir/cipher.txt']
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
p.stdin.write(cipherKey)

startTime = time.time()

os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( dur, one))

for i in finalCrypt:

    if(i == "0"):
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( dur, zero))

    else:
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( dur, one))

os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( dur, one)) # padded end bit to tell receiver to stop reading

print('{}{}'.format("time elapsed: ", (time.time() - startTime) ))

