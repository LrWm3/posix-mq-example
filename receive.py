#!/usr/bin/env python3
import queue
from ipcqueue import posixmq

# Get messages from the queue
q_name = '/reeldata-frame-hashes-3'
q_max_size = 732
max_msgbytes = 1024

created_queue = False
q = posixmq.Queue(q_name, maxsize=q_max_size, maxmsgsize=max_msgbytes)
if q.qattr()['max_size'] != q_max_size or q.qattr()['max_msgbytes'] != max_msgbytes:
  print(f"Queue mismatch; created with max size {q_max_size} or max message size {max_msgbytes}, actual size {q.qattr()['max_size']} and actual message size {q.qattr()['max_msgbytes']}")
  exit(1)


while True:
  wait_blocking_seconds=0.25
  try:
    msg = q.get(block=True, timeout=wait_blocking_seconds)
    print(f"Got message from queue {msg}, queue name {q_name}, queue size: {q.qsize()}")
  except queue.Empty as e:
    print(f"Queue {q_name} is empty")
  except posixmq.QueueError as e:
    print(f"Error: {e}")
