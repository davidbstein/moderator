if [[ $_ != $0 ]]
then
  source env/bin/activate
  export DATABASE_URL=postgres:///$(whoami)
  export PGDATA=`pwd`/db
  export GOOGLE_CLIENT_SECRET="ZKC162Cqg02Z0ksSW3O58S14"
  export GOOGLE_CLIENT_ID="761556532733-79ns6te5a51hkk0ns3ms88pfjfq3qm0t.apps.googleusercontent.com"
  export SECRET_KEY="MY SECRET KEY"
  export SESSION_TYPE="filesystem"
  export URL="http://127.0.0.1:5000"
  pg_ctl -D db -l logfile start
else
  echo 'you must run `source init.sh`' || exit 0
fi
