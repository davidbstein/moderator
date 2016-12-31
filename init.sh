if [[ $_ != $0 ]] 
then
  source env/bin/activate
  export DATABASE_URL=postgres:///$(whoami)
  export PGDATA=`pwd`/db
  pg_ctl -D db -l logfile start
else 
  echo 'you must run `source init.sh`' || exit 0
fi
