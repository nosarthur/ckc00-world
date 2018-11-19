Deployment on Ubuntu 18.04LTS
============================

## provision

* Spin up aws or gcloud instance
* Attach policy to allow public access to port 80 and 443
* Get public address
    * `aws ec2 describe-instances`
    * `gcloud compute instances list`

## backend setup on the instance

After `ssh` to the instance, try the DEBUG server first

```bash
sudo apt update
sudo apt install nginx, python3-venv

git clone https://github.com/nosarthur/ckc00alumni
cd ckc00alumni
sudo cp scripts/nginx-ckc00 /etc/nginx/site-available/
sudo cp scripts/gunicorn-ckc00.service /etc/systemd/system/
make run
```

Then connect to the site in the browser. If everything works

* upload database to repo root
* change `ckc00/settings.py` `ALLOWED_HOST` to instance's public IP
* enable production mode

```bash
echo DJANGO_SECRET_KEY=$(
python3.6 -c"import random; print(''.join(random.SystemRandom().
choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50)))"
) >> .env`
echo IN_PRODUCTION=1 >> .env
```

## update

After pulling the latest backend repo, run

```bash
sudo systemctl restart gunicorn-ckc00.service
sudo systemctl restart nginx
```

debug
```bash
sudo journalctl -u gunicorn-..
```
