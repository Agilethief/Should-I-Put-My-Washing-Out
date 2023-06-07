from app import app as getApp

if __name__ == "__main__":
    getApp.run()


# gunicorn --bind 0.0.0.0:5009 wsgi:getApp
# /home/tim/webapp/FlaskWisdomToolkit/flask_auth_app/webapp.sock
# sudo nano /etc/systemd/system/weatherapp.service
# proxy_pass http://unix:/home/sammy/homepage/TBWebappDirectory/tbwebapp.sock;
# proxy_pass http://unix:/home/sammy/weatherApp/Should-I-Put-My-Washing-Out/WeatherApp/site/weatherApp.sock
#  "http://unix:/home/sammy/WeatherApp/Should-I-Put-My-Washing-Out/WeatherApp/site/weatherApp.sock:/"
#               /home/sammy/weatherApp/Should-I-Put-My-Washing-Out/WeatherApp/site
# make sure the www-data can access the web socket!!
# chgrp www-data filename

# p/Should-I-Put-My-Washing-Out/WeatherApp/environment/bin/gunicorn: No such file or directory
# sudo nano /etc/nginx/sites-available/myproject

'''
server {
        server_name weather.tbwebapp.com;

        location / {
                include proxy_params;
                proxy_set_header Host $host;
                proxy_pass http://unix:/home/sammy/WeatherApp/Should-I-Put-My-Washing-Out/WeatherApp/site/weatherApp.sock;
        }


    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/weather.tbwebapp.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/weather.tbwebapp.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {
        server_name wisdom.tbwebapp.com;

        location / {
                include proxy_params;
                proxy_set_header Host $host;
                proxy_pass http://unix:/home/sammy/FlaskWisdomToolkit/flask_auth_app/myproject.sock;
        }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/wisdom.tbwebapp.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/wisdom.tbwebapp.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
'''

# include proxy_params;
proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for
proxy_set_header   X-Real-IP            $remote_addr
proxy_set_header   X-Forwarded-Host    $host
proxy_set_header   X-Forwarded-Proto https
