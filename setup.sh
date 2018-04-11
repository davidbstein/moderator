# initdb db
createdb $(whoami)
psql -a -f src/model/model.sql
virtualenv env
pip install -r requirements.txt
npm install --only=dev
