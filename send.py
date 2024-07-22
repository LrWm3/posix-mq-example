#!/usr/bin/env python3
import queue
from ipcqueue import posixmq

# Create a new queue for sixty seconds of frame hashes
#
# Note: 
#   we must change '/proc/sys/fs/mqueue/msg_max' from default of 10 to create queues with maxsize > 10
#   we must change '/proc/sys/fs/mqueue/msgsize_max' from default of 8192 to create queues with maxmsgsize > 8192
#
# To do temporarily (until reboot):
#   sudo sysctl -w fs.mqueue.msg_max=3600
#
# To make permanent:
#   sudo -i
#   echo 3600 > /proc/sys/fs/mqueue/msg_max
#   echo 16384 > /proc/sys/fs/mqueue/msgsize_max
##
# Raise msgqueue rlimits
##
# For larger IPC queues, we need to adjust the rlimits for the user for message queues.
##
# When running in docker:
#   docker run --rm -it --ulimit msgqueue=unlimited <image>
#
# On the host:
#   in /etc/security/limits.conf
#
#   root   - msgqueue unlimited
#   <user> - msgqueue unlimited
##
#
##
q_name = '/reeldata-frame-hashes'
q_max_size = int(2*102400)
max_msgbytes = 2*1024

created_queue = False
for i in range(2):
  q = posixmq.Queue(q_name, maxsize=q_max_size, maxmsgsize=max_msgbytes)
  if q.qattr()['max_size'] != q_max_size or q.qattr()['max_msgbytes'] != max_msgbytes:
    print(f"Queue not created with max size {q_max_size} or max message size {max_msgbytes}, actual size {q.qattr()['max_size']} and actual message size {q.qattr()['max_msgbytes']}")
    q.close()
    q.unlink()
  else:
    created_queue = True
    break

if not created_queue:
  print(f"Failed to create queue with max size {q_max_size} and max message size {max_msgbytes}")
  exit(1)

for i in range(10000):
  try: 
    wait_blocking_seconds=0.1
    q.put(f"frame-hash-{i}", block=True, timeout=wait_blocking_seconds)
  except queue.Full as e:
    print(f"Queue is full {q_name}, queue size: {q.qsize()}, queue info: {q.qattr()}")
