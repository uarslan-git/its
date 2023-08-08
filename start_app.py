import pathlib
import subprocess
import atexit
import os
import signal



def cleanup_child_processes():
    for process in child_processes:
        try:
            os.kill(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass  # Process already exited



path = pathlib.Path(__file__).parent.resolve()
backend_start = os.path.join(path, "api/main.py")
frontend_start = os.path.join("start_frontend.py")

if __name__ == "__main__":

    # Store references to the child processes
    child_processes = []

    # Register the cleanup function to be called when the script exits
    atexit.register(cleanup_child_processes)

    backend = subprocess.Popen(["python", backend_start])
    child_processes.append(backend)
    frontend = subprocess.Popen(["cd frontend && ls  && python start_frontend.py"], shell=True)
    child_processes.append(frontend)

    backend.wait()
    frontend.wait()

