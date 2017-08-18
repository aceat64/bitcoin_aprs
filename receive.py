#!/usr/bin/python3
import aprslib
import codecs
import base64

messages = {}
max_messages = {}

def process_transaction(callsign):
  if callsign not in messages:
    return false

  txn_base64 = ''
  for i in messages[callsign]:
    txn_base64 += messages[callsign][i]
  txn_hex = codecs.encode(base64.standard_b64decode(txn_base64[0:-1]), 'hex')
  print(txn_hex)

  # TODO: submit txn to bitcoin network

  del messages[callsign]
  del max_messages[callsign]

  return True

def callback(packet):
  if set(['msgNo', 'from', 'message_text']).issubset(packet):
    if packet['from'] not in messages:
      messages.update({
        packet['from']: {
          packet['msgNo']: packet['message_text']
        }
      })
    else:
      messages[packet['from']].update({
        packet['msgNo']: packet['message_text']
      })
  else:
    return False

  num_messages = len(messages[packet['from']])


  if packet['message_text'].endswith('$'):
    max_messages.update({
        packet['from']: packet['msgNo']
    })
    print("Found last message: %s" % packet['msgNo'])

  if packet['from'] in max_messages:
    print("We have {x} of {y} messages".format(x=num_messages, y=max_messages[packet['from']]))
  else:
    print("We have {x} of at least {y} messages".format(x=num_messages, y=packet['msgNo']))

  if packet['from'] in max_messages and num_messages == max_messages[packet['from']]:
    process_transaction(packet['from'])

AIS = aprslib.IS("N0CALL", host="localhost", port=14580)
AIS.connect()
AIS.set_filter('g/BITCOIN')

AIS.consumer(callback)
