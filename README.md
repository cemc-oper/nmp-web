# nmp-web

A cloud website for NMP(NWPC Monitor Platform).

## Deploy

### Python

Use `pyenv` to install python and create a virtualenv.

Create a virtualenv for nmp-web, such as `nmp-web-env`.

### Project

Download source code into some directory, such as `/srv/nmp-web/www/nmp-web`.

Install source code under virtualenv using `pip install -e .`.

### Redis

Create redis server using Docker.

### Gunicorn

Install gnuicorn in `nmp-web-env`.

```bash
pip install gnuicorn
```

Create a script to start gunicorn process in vritualenv.

```bash
#!/bin/bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv virtualenv-init -)"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi

cd /srv/nmp-web
pyenv activate nmp-web-env

export LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
export LC_API_SERVER="url for leancloud"

export MODE=production
export NMP_WEB_CONFIG=some/config/file/path

gunicorn -w 1 -b 127.0.0.1:3000 nmp_web.wsgi:application \
	--log-level=debug
```

### Supervisor

Install supervisor.

```bash
sudo apt install supervisor
```

Create a configure file.

```ini
[program:nmp_web]
command = path_to_script
directory = /srv/nmp-web
user = user name
startsecs = 3

redirect_stderr = true
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 10
stdout_logfile = path_to_log
```

Start supervisor program nmp_web using:

```bash
superivsorctl start nmp_web
```

### nginx

Install nginx.

Update `nginx.conf` to enable gzip and allow large client data of workflow status blob.

```nginx
client_max_body_size 8M;
client_body_buffer_size 128k;

gzip on;
gzip_min_length 1k;
gzip_buffers 16 64k;
gzip_http_version 1.1;
gzip_comp_level 6;
gzip_types text/plain application/x-javascript text/css application/xml;
gzip_vary on;
```

Add `nmp_web` in `site-available` directory.

```nginx
server {
    listen      80;

    server_name www.nwpcmonitor.cc;

    return 301 https://www.nwpcmonitor.cc$request_uri;
}
server {
    listen 443;

    server_name www.nwpcmonitor.cc;

    root       /srv/nmp-web/www/nmp-web;
    access_log path_to_access_log;
    error_log  path_to_error_log;

    location /favicon.ico {
        root /srv/nmp-web/www/nmp-web;
    }

    location ~ ^\/static\/.*$ {
        root /srv/nmp-web/www/nmp-web;
    }

    location / {
        proxy_pass       http://127.0.0.1:3000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

```

Add SSL for nmp_web.

## License

Copyright &copy; 2015-2019, Perilla Roc

`nmp-web` is licensed under [GPL v3.0](./LICENSE.md)