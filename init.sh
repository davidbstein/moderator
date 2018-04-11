if [[ $_ != $0 ]]
then
  source env/bin/activate
  export DATABASE_URL=postgres:///$(whoami)
  export PGDATA=`pwd`/db
  export GOOGLE_CLIENT_SECRET=""
  export GOOGLE_CLIENT_ID=""
  export SECRET_KEY="MY SECRET KEY"
  export SESSION_TYPE="filesystem"
  export URL="http://127.0.0.1:5000"
  export DEBUG="DEBUG"
  export DOMAIN_MAPS='{"vendor.example.com":"example.com"}'
  pg_ctl -D db -l logfile start
else
  echo 'you must run `source init.sh`' || exit 0
fi
