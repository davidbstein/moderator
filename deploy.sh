echo "!! Starting"
git checkout deploy
git merge master --no-commit
echo "!! compiling"
export NODE_ENV="production"
scss src/client/styles/moderator.scss:src/static/bundle.css
./node_modules/.bin/webpack src/client/app.js src/static/bundle.js --optimize-minimize
export NODE_ENV="develop"
git add src/static
git commit -m '(automated) merge compile commit'
echo "!! deploying"
git push -f heroku HEAD:master
git push
echo "!! restoring"
git checkout master
scss src/client/styles/moderator.scss:src/static/bundle.css
./node_modules/.bin/webpack src/client/app.js src/static/bundle.js --optimize-minimize
echo "!! done"