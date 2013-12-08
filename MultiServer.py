from multiprocessing import Process
import subprocess
import GlobalVars


def botInstance(server, channels):
    args = ["python", "hubbebot.py"]
    args.append(server)
    for chan in channels:
        args.append(chan)
    subprocess.call(args)


if __name__ == "__main__":
    for (server,channels) in GlobalVars.connections.items():
        p = Process(target=botInstance, args=(server, channels))
        p.start()
