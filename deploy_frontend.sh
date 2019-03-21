#!/usr/bin/env bash
rm -r frontend/* &&
tar xvfz frontend.tar.gz --strip-components=5 -C frontend/ > ~/FRONTEND.LOG &&
cd frontend &&
npm install >> ~/FRONTEND.LOG &&
ng build --prod >> ~/FRONTEND.LOG &&
cp -r dist/shop-scraper-frontend/* /var/www/infinity/
