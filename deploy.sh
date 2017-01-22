git checkout deploy
git merge master --no-commit
scss src/client/styles/moderator.scss:src/static/bundle.css --sourcemap
./node_modules/.bin/webpack src/client/app.js src/static/bundle.js --devtool source-map --optimize-minimize
git add src/static
git commit -m '(automated) merge compile commit'
git push -f heroku HEAD:master
git checkout master
