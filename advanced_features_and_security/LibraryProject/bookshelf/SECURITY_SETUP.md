# Instructions for configuring Nginx for HTTPS/HSTS

server {
    # 1. Redirect HTTP to HTTPS
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$host$request_uri;
}

server {
    # 2. Listen on HTTPS port
    listen 443 ssl;
    server_name your-domain.com www.your-domain.com;

    # 3. Specify SSL Certificate and Key paths
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # 4. Proxy requests to Django (Gunicorn/uWSGI)
    location / {
        proxy_pass http://127.0.0.1:8000;
        # ... other proxy headers
    }
}


