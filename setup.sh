createdb $(whoami)
psql -a -f src/model/model.sql
virtualenv env
pip -r requirements.txt
npm install --only=dev
