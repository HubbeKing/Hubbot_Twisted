import GlobalVars

for (server,channels) in GlobalVars.connections.items():
    args = ["hubbot.py"]
    args.append(server)
    for chan in channels:
        args.append(chan)
    subprocess.call(args)
