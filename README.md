# AR WEB приложение

Приложение для показа видео поверх белого прямоугольника

## Подготовка окружения (Ubuntu)

### Склонировать репозиторий

```shell
git clone https://github.com/ysonofriychuk/web-ar-app.git
```

### Подготовить виртуальное окружение Python

```shell
python3 -m venv venv
```

```shell
source venv/bin/activate
```

```shell
pip install -r requirements.txt
```

### Выпустить ssl-сертификат

```shell
sudo snap install --classic certbot
```

```shell
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

```shell
sudo certbot certonly --standalone
```

## Запуск приложения
```shell
python3 main.py --port 443 --host <HOST> --cert-file /etc/letsencrypt/live/<DOMAIN>/fullchain.pem --key-file /etc/letsencrypt/live/<DOMAIN>/privkey.pem
```
