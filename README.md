# POSIX Message Queue Example

This guide provides instructions on how to use and configure message queues.

It includes steps for making permanent changes, adjusting resource limits for IPC queues, and configuring settings both on the host and within Docker containers.

## 1. Making Permanent Changes to Message Queue Settings

To adjust the message queue settings permanently, follow these steps:

1. Open a terminal and switch to the root user:

   ```bash
   sudo -i
   ```

2. Set the maximum number of messages in a queue:

   ```bash
   echo 3600 > /proc/sys/fs/mqueue/msg_max
   ```

3. Set the maximum message size:
   ```bash
   echo 16384 > /proc/sys/fs/mqueue/msgsize_max
   ```

## 2. Raising msgqueue rlimits

To handle larger IPC queues, adjust the resource limits (rlimits) for the user.

### 2.1 Running in Docker

When running a container, you can adjust the message queue limits with the following command:

```bash
docker run --rm -it --ulimit msgqueue=unlimited <image>
```

### 2.2 Configuring on the Host

For persistent settings on the host, modify the `/etc/security/limits.conf` file. Add the following lines:

```plaintext
root   - msgqueue unlimited
<user> - msgqueue unlimited
```

Replace `<user>` with the actual username you want to configure.

## Usage

Install remaining dependencies.

```
pip install -r requirements.txt
```

Run `send.py`

in a separate terminal

Run `receive.py`

See messages flowing through IPC.

### FAQ

Q: I see error `ipcqueue.posixmq.QueueError: 4, No system resources`

A: Raise the rlimits for the queue following the above steps. See `ulimit -q` for users current queue memory limit.

---

Q: I see error `ipcqueue.posixmq.QueueError: 2, Invalid value`

A: I forget but I think this is when the max message size is beyond the maximum allowed. Raise the limit. If the error is still observed, you may have hit the maximum limits for the system. see [mq_overview](https://man7.org/linux/man-pages/man7/mq_overview.7.html) man page for details.
