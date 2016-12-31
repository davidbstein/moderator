# TODO actually write a dev watcher
echo "GOTTA RUN THIS TOO"
echo "scss --watch src/client/styles/moderator.scss:src/static/bundle.css --sourcemap"
./node_modules/.bin/webpack src/client/app.js src/static/bundle.js --devtool source-map --watch # --optimize-minimize
