# minecraft-server
minecraft serving hosting

# connect (if run in wsl2)
select Multiplayer, set ::1 as server address and connect to the server.

# backup to study
https://github.com/itzg/docker-mc-backup/tree/master

# config references
1. https://minecraft.fandom.com/wiki/Server.properties
2. https://docker-minecraft-server.readthedocs.io/en/latest/variables/#server
3. https://github.com/itzg/docker-minecraft-server

# To recover from backup-ed world
1. get world folder into data/
2. run `sudo chown -R opc:opc world/` to change ownership, my username is opc, yours might be other, just refer to the data/ owner:group will do
3. run `sudo chmod -R u+rw world/` to change read permission, 
