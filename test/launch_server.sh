#!/bin/sh
set -ue

cd server
export RAILS_ENV=development
rails db:environment:set RAILS_ENV=development
bundle exec rails db:reset
exec bundle exec rails server -p 31313
