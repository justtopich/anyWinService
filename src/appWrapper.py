import time
from subprocess import Popen, PIPE, DEVNULL
from threading import Thread

import psutil

from conf import task, log


class AppWrapper(Thread):
    def __init__(self):
        log.info("Starting AppWrapper thread")
        super(AppWrapper, self).__init__()
        self.name = "AppWrapper"
        self._stop = False
        self.isStopped = False
        self._proc: Popen = None
        self.start()

    def stop(self):
        log.info("stopping app")
        process = psutil.Process(psutil.Process().pid)
        for proc in process.children(recursive=True):
            log.info(f"stooping child proc {proc.pid}")
            proc.send_signal(task.stopSignal)
            # proc.wait()

        while not self.isStopped:
            time.sleep(0.5)

    def run(self):
        try:
            log.info(f"launch {task.exe} {task.exeKey} in {task.exePath}")

            self._proc = Popen(
                "{} {}".format(task.exe, task.exeKey),
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
                stdin=DEVNULL,
                cwd=task.exePath,
            )

            log.info(f"started app with pid {self._proc.pid}")
            while self._proc.poll() is None:
                log.info(self._proc.stdout.readline().decode("cp866").replace("\n", ""))

            # if stderr != b'':
            #     log.info(stderr.decode('cp866').replace('\r\n', ''))

        except Exception as e:
            log.error(f"{e}")
        finally:
            log.info("app stopped")
            self.isStopped = True
