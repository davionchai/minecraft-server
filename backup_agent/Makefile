.PHONY: backup
backup:
	tar -czf /home/ubuntu/gworld/world_$(date +%Y%m%d_%H%M%S).tar.gz -C /home/ubuntu/minecraft-server/data/world .

.PHONY: recover
recover:
	tar -xzf /home/ubuntu/gworld/my_file.tar.gz -C .

.PHONY: download
download:
	scp -i ssh_keys/instance_minecraft_ssh_key ubuntu@x.x.x.x:/home/ubuntu/world_xxx.tar.gz .
