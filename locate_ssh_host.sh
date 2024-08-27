# Script for checking which ip address belongs to the host you are looking for
# Wed, Aug 21, 2024

set -e 

if [[ $# != 3 ]]
then
  echo 'Usage ./script <username> "password"|"keyfile" <path_to_keyfile|password>'
  exit
fi

username=$1

if [[ "$2" == password ]]
then
  password="$3"
  echo username: "$username"
  echo password: "$password"
  echo looking in 192.168.0.0/24

  for ip in 192.168.0.{0..255}
  do
    sshpass -p"$password" \
    ssh "$username"@$ip \
      -q \
      -o StrictHostKeyChecking=no \
      -o UserKnownHostsFile=/dev/null \
      -o ConnectTimeout=1 \
      echo SSH connection at $ip, hostname '"$(hostname)"' &
    done
    sleep 3

elif [[ "$2" == keyfile ]]
then
  keyfile="$3"
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
      echo SSH connection at $ip, hostname '"$(hostname)"' &
  done
  sleep 3

else
  echo 'Second argument must be "password" or "keyfile"'
  exit
fi


