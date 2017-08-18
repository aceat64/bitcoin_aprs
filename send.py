#!/usr/bin/python3
import aprslib
import codecs
import base64
from random import randint

mycall = "N0CALL"
passwd = "-1"

# Random transaction that I pulled from mainnet
txn_hex = "010000000217fcb1b44f8295db8f6395a3fc3acb764c979c0202b86ce36e7422a754a17864000000008a4730440220334be1268ace191bc0c96568e8cad680b51d9d20e2f27070fe5c2d4a5a6543ae02207f044ea56ac2b72b7b778908081ce3f89afeb320f018f39251bd7486bd086ed3014104dcf4b6c2ef1e216a64f611244ee4e12750b44fc01af0f0c337c8150e0b4b7b99f9d28c76b0c8c1c55ca6ec64172aa5cf191bb920c0e14065cd660ada29b8e17ffdffffff5bb448f8ec1aeb1376d8d167def6409ecb8a169bb6578420b433fa56a771b169010000008b483045022100deca36c6f7a3b30a068d3cd21f619e4645cad342913608ef9081ea9bb1f38e3b022033c948aa860e829b59a0d0c4255924f088ffcb595a2baeec758db026d935c4500141045f979942f4c566fe3a839576254b424f27bb87344c1d2502848ea9d6513d22c22349ed829da57968f1ec3d13cada19b79900c15ecc4b68e0a49c5993bfd75c60fdffffff0298b05b01000000001976a914c54d71cc06a256385c1d73053259f1634704ae1588ac00e1f5050000000017a9146771bfb700f349c7b54732cb7bbabeb99fe6f84c8700000000"
txn_base64 = base64.standard_b64encode(codecs.decode(txn_hex, 'hex')).decode("utf-8") + '$'

# a valid passcode for the callsign is required in order to send
AIS = aprslib.IS(mycall, passwd=passwd)
AIS.connect()

n = 67
x = 1
for i in range(0, len(txn_base64), n):
  aprs_message = "{mycall}>APDR14::BITCOIN  :{txn}{{{sequence}".format(
    mycall=mycall,
    txn=txn_base64[i:i+n],
    sequence=x
  )
  AIS.sendall(aprs_message)
  print(aprs_message)
  x = x + 1
