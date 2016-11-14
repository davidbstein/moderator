source env/bin/activate
export DATABASE_URL=postgres:///$(whoami)
export PGDATA=`pwd`/db
createdb $(whoami)