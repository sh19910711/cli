#!/bin/sh
set -ue
if [ ! -d server ]; then
    git clone https://github.com/makestack/server
    cd server
    bundle install --jobs 2
    bundle exec rails db:migrate
    cd ..
fi

cd server
export RAILS_ENV=development
rails db:environment:set RAILS_ENV=development
bundle exec rails db:reset
exec bundle exec rails server -p 31313
