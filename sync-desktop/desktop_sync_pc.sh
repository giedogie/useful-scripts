#!/bin/bash
while true;
do
echo -e "\n  $(date) \n " >> ~/desktop_sync_log-pc.md
# Lista folderów do skopiowania
folder=("/home/admin/")

# Lista folderów do pominięcia
ex=("*.ssh" "*.config" "/Qemu" "/syncthing" "*.cache" "*.local" "*.mozilla" "*.var" "*.vdi")
# Adres serwera docelowego
server="admin@30.10.10.227"
#Port SSH
port="5001"
# Katalog docelowy na serwerze
destination="/home/admin/SYNC/"
rsync -avzrptgo --delete --exclude=${ex[0]} --exclude=${ex[1]} --exclude=${ex[2]}  --exclude=${ex[3]} --exclude=${ex[4]} --exclude=${ex[5]} --exclude=${ex[6]} --exclude=${ex[7]} --exclude=${ex[8]} --update -e "ssh -p $port" $server:$destination $folder >> ~/desktop_sync_log-pc.md
echo -e "\n  $(date) \n " >> ~/desktop_sync_log-pc.md
rsync -avzrptgo --delete --exclude=${ex[0]} --exclude=${ex[1]} --exclude=${ex[2]}  --exclude=${ex[3]} --exclude=${ex[4]} --exclude=${ex[5]} --exclude=${ex[6]} --exclude=${ex[7]} --exclude=${ex[8]} --update -e "ssh -p $port" $folder $server:$destination >> ~/desktop_sync_log-pc.md
done


