# mark3 (WIP)

A modern Minecraft server wrapper written in python3 with asyncio

## TODO

**Note:** The order of the following checklist doesn't necessarily mean it will be completed in that order!

- [x] Daemonize Process
- [x] Basic asyncio event system
- [x] Event priorities
- [ ] Regex function triggers for server output (Console event? idk what to call it)
- [ ] Gather config from server directory
- [ ] Build java command from config info
- [x] Start a server process
- [ ] Create a UNIX socket server to handle requests from clients
- [x] Flesh out more server events (ServerOutput, ServerInput)
- [ ] Trigger other events from console output
- [ ] Basic user client (No command input?)
- [ ] Document events and code structure
- [ ] Advanced user client (CLI format TBD)
- [ ] Server running/stopping system using mark2-style modes (hold, kill etc.)
- [ ] Scripting plugin to trigger things on events and timers. Restrict accessible events to prevent issues!)
