# mark3 (WIP)

A modern Minecraft server wrapper written in python3 with asyncio

## TODO

- [x] Daemonize Process
- [x] Basic asyncio event system
- [ ] Event priorities
- [ ] Gather config from server directory
- [ ] Build java command from config info
- [ ] Start server process and create a UNIX socket server to handle requests from clients
- [ ] Flesh out more events (ServerOutput, ServerInput)
- [ ] Trigger other events from console output
- [ ] Basic user client (No command input?)
- [ ] Document events and code structure
- [ ] Advanced user client (CLI format TBD)
- [ ] Server running/stopping system using mark2-style modes (hold, kill etc.)
- [ ] Scripting plugin to trigger things on events and timers. Restrict accessible events to prevent issues!)
