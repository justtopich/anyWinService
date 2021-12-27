import os
import sys
import time
import traceback
import socket

import servicemanager
import win32serviceutil
import win32event
import win32service

from settings import homeDir


def svc_init():
    class AppServerSvc(win32serviceutil.ServiceFramework):
        from conf import get_svc_params

        svcParams = get_svc_params()
        _svc_name_ = svcParams[0]
        _svc_display_name_ = svcParams[1]
        _svc_description_ = svcParams[2]

        def __init__(self, args):
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            socket.setdefaulttimeout(60)

        def SvcStop(self):
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)

        def SvcDoRun(self):
            rc = None
            try:
                from conf import log

                log.info("start app")

                from appWrapper import AppWrapper

                appWrapper = AppWrapper()

                while rc != win32event.WAIT_OBJECT_0:
                    time.sleep(1)
                    rc = win32event.WaitForSingleObject(self.hWaitStop, 4000)
                    # если стопим через команду или по внутренним причинам
                    if appWrapper.isStopped:
                        return

                appWrapper.stop()
            except Exception:
                with open(f"{homeDir}error.txt", "w") as f:
                    f.write(f"{traceback.format_exc()}")
                os._exit(42)

    return AppServerSvc


# sys.argv.append("run")

if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            if homeDir.endswith("system32/"):
                # Server 2012 != Win 10
                homeDir = os.path.dirname(sys.executable) + "/"  # Server 2012 != Win 10

            AppServerSvc = svc_init()
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(AppServerSvc)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            if "install" in sys.argv or "remove" in sys.argv or "update" in sys.argv:
                AppServerSvc = svc_init()
                win32serviceutil.HandleCommandLine(AppServerSvc)
            elif "help" in sys.argv:
                raise Exception("Show help")
            elif "run" in sys.argv:
                from appWrapper import AppWrapper

                appWrapper = AppWrapper()
            else:
                raise Exception("Show help")

    except Exception as e:
        e = traceback.format_exc()
        print(f"Fail to start main thread: {e}")

        with open(f"{homeDir}error.txt", "w") as f:
            f.write(str(e))

        print(
            f"\nUsage: {os.path.basename(sys.argv[0])} [options]\n"
            "Options:\n"
            " run: start me\n"
            " install: install as windows service\n"
            " remove: delete windows service\n"
            " update: update windows service\n"
        )
