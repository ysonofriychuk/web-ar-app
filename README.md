# AR WEB приложение

WEB-приложение дополненной реальности для показа видео поверх белого прямоугольника

![](assets%2Fdemo.gif)
Designed by Freepik

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

### Создать файл системной службы

```shell
sudo vim /etc/systemd/system/web-ar-app.service
```

### Введите в него следующее содержимое

```
[Unit]
Description=AR Web Application Service
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/root/web-ar-app
ExecStart=/root/web-ar-app/venv/bin/python3 main.py --port 443 --host <YOUR_HOST> --cert-file /etc/letsencrypt/live/<YOUR_DOMAIN>/fullchain.pem --key-file /etc/letsencrypt/live/<YOUR_DOMAIN>/privkey.pem
Restart=always

[Install]
WantedBy=multi-user.target
```

### Перезагрузите конфигурацию

```shell
sudo systemctl daemon-reload
```

### Включите новую службу

```shell
sudo systemctl enable web-ar-app.service
```

### Запустите службу

```shell
sudo systemctl start web-ar-app.service
```

### Проверьте статус службы

```shell
sudo systemctl status web-ar-app.service
```

### Проверьте логи службы

```shell
journalctl -u web-ar-app.service
```

### При необходимости исправьте ошибки и сделайте рестарт службы

```shell
sudo systemctl daemon-reload
sudo systemctl restart web-ar-app.service
```

### Для остановки службы выполнить

```shell
sudo systemctl stop web-ar-app.service
```