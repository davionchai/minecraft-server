# minecraft-server
minecraft serving hosting

# connect (if run in wsl2)
select Multiplayer, set ::1 as server address and connect to the server.

# config references
1. https://minecraft.fandom.com/wiki/Server.properties
2. https://docker-minecraft-server.readthedocs.io/en/latest/variables/#server
3. https://github.com/itzg/docker-minecraft-server

# to recover from backup-ed world
1. get world folder into data/
2. run `sudo chown -R opc:opc world/` to change ownership, my username is opc, yours might be other, just refer to the data/ owner:group will do
3. run `sudo chmod -R u+rw world/` to change read permission, 

# infra backend
The infra backend opentf code is hosted in my private infrastructure repo. I am using oracle cloud with free tier for the resources that are being used to host the minecraft server and its working as expected.

# backup mechanism
I am gzip-ing the `/data/world/` folder and uploading it to oracle bucket that has free 20gb storage as the backup location

# installing oci without python
refer to [this doc](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm#InstallingCLI__linux_and_unix), run below command
```sh
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
```

# instaling oci if already has python configured
refer to [this doc](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/climanualinst.htm), run below command
```sh
pip install oci-cli
```

# run backup agent locally
to run the backup agent locally, you will need to authenticate oci first, in the dev environment, i have already forced to use oci session method, please run the following to get yourselves setup
```sh
oci session authenticate
```

after that, use this to tell python oci to use security token as the auth method
```sh
export OCI_CLI_AUTH=security_token
```

the session token only last for 60 minutes for default, to remain authenticated, please run
```sh
oci session refresh
```

# download file from bucket
```sh
oci os object get --bucket-name <bucket-name> --name <backup/file.tar.gz> --file <file-name>
```
