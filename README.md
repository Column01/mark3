# mark3 (WIP)

A modern Minecraft server wrapper written in python3 with asyncio

## Support the development

If you'd like to support the development of mark3, you can send me a donation through paypal or some cryptocurrencies. See the info below

**DISCLAIMER**: All donations are just that, donations. There are no guaranteed perks for donating (yet?) and all it does is help motivate me to work on this more! I appreciate anything you can spare if you'd like to see this project finished!

### Paypal

To send me money on Paypal, you can use my email: `ColinAndress999@gmail.com`

### Crypto

- BTC `18KcFvh74iXLFBHQFBKqEWXHiGJVoMa3kp`
- LTC `18KcFvh74iXLFBHQFBKqEWXHiGJVoMa3kp`
- BAT `0xc12d753361744350280b6eA532f35965e776be5B` OR you can go to my profile and use a brave creator tip

## Todo List

**Note:** The order of the following checklist doesn't necessarily mean it will be completed in that order!

- [x] Daemonize Process
- [x] Basic asyncio event system
- [x] Event priorities
- [x] Regex triggers for events
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
