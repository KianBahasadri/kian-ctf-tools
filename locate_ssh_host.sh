# Script for checking which ip address belongs to the host you are looking for
# Wed, Aug 21, 2024

set -e 

if [[ $# != 2 ]]
then
  echo 'Usage ./script <username> <path_to_keyfile>'
  exit
fi

username=$1
keyfile=$2
echo username: "$username"
echo keyfile: "$keyfile"
echo looking in 192.168.0.0/24

for ip in 192.168.0.{0..255}
do
  ssh "$username"@$ip \
    -q \
    -i "$keyfile" \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    -o ConnectTimeout=1 \
    -o BatchMode=true \
    echo Successfull SSH connection at $ip &
done

sleep 2

