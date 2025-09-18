# 🚀 Guia de Instalação e Deployment

## 📋 Pré-requisitos

### Software Necessário
- **Python 3.8+** - Linguagem principal do backend
- **Git** - Controle de versão
- **Navegador Web Moderno** - Chrome, Firefox, Safari ou Edge
- **Editor de Código** - VSCode recomendado

### Conhecimentos Técnicos
- Básico de Python e Flask
- HTML/CSS/JavaScript
- Conceitos de APIs REST
- Linha de comando/terminal

## 🔧 Instalação Local

### 1. Clone do Repositório
```bash
# Clone o projeto
git clone https://github.com/leonardobora/eco-dashboard-renault.git
cd eco-dashboard-renault

# Verifique os arquivos
ls -la
```

### 2. Ambiente Python
```bash
# Criar ambiente virtual (recomendado)
python3 -m venv venv

# Ativar ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Execução do Sistema
```bash
# Iniciar servidor Flask
python app_renault_mvp.py

# O sistema estará disponível em:
# http://localhost:5000
```

### 4. Verificação da Instalação
1. Abra o navegador em `http://localhost:5000`
2. Verifique se as métricas estão sendo exibidas
3. Teste a navegação entre as abas
4. Confirme se os gráficos estão funcionando

## 🌐 Deployment em Produção

### Opção 1: Servidor Linux (Ubuntu/CentOS)

#### Preparação do Servidor
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e dependências
sudo apt install python3 python3-pip python3-venv nginx -y

# Criar usuário para a aplicação
sudo useradd -m -s /bin/bash ecoti
sudo su - ecoti
```

#### Deploy da Aplicação
```bash
# Clone e configuração
git clone https://github.com/leonardobora/eco-dashboard-renault.git
cd eco-dashboard-renault

# Ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Instalar Gunicorn para produção
pip install gunicorn
```

#### Configuração do Gunicorn
```bash
# Criar arquivo de configuração
cat > gunicorn.conf.py << EOF
bind = "127.0.0.1:5000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
preload_app = True
EOF

# Testar Gunicorn
gunicorn -c gunicorn.conf.py app_renault_mvp:app
```

#### Configuração do Nginx
```bash
# Configuração do Nginx
sudo cat > /etc/nginx/sites-available/ecoti << EOF
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias /home/ecoti/eco-dashboard-renault/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Ativar site
sudo ln -s /etc/nginx/sites-available/ecoti /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Opção 2: Docker Container

#### Dockerfile
```dockerfile
# Criar Dockerfile
cat > Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Configurar usuário não-root
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app_renault_mvp:app"]
EOF
```

#### Build e Deploy
```bash
# Build da imagem
docker build -t ecoti-dashboard .

# Executar container
docker run -d \
  --name ecoti-dashboard \
  -p 5000:5000 \
  --restart unless-stopped \
  ecoti-dashboard

# Verificar logs
docker logs ecoti-dashboard
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web
    restart: unless-stopped
```

### Opção 3: Cloud Deployment (Heroku)

#### Preparação
```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login no Heroku
heroku login

# Criar aplicação
heroku create ecoti-dashboard-renault
```

#### Configuração para Heroku
```bash
# Criar Procfile
echo "web: gunicorn app_renault_mvp:app" > Procfile

# Adicionar gunicorn ao requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt

# Commit e deploy
git add .
git commit -m "Preparação para deploy Heroku"
git push heroku main
```

## ⚙️ Configurações de Ambiente

### Variáveis de Ambiente
```bash
# .env (criar na raiz do projeto)
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-muito-segura
DATABASE_URL=postgresql://user:pass@localhost/ecoti
SENSOR_API_URL=https://api-sensores.renault.com
ALERT_EMAIL=admin@renault.com
DEBUG=False
```

### Configuração de Banco de Dados (Futuro)
```python
# Para quando integrar com banco real
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'ecoti_dashboard',
    'user': 'ecoti_user',
    'password': 'senha_segura'
}
```

## 📊 Monitoramento e Logs

### Logs da Aplicação
```bash
# Configurar logging em produção
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/ecoti.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Monitoramento de Sistema
```bash
# Instalar ferramentas de monitoramento
pip install psutil

# Script de monitoramento básico
cat > monitor.py << EOF
import psutil
import time

def monitor_system():
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        print(f"CPU: {cpu}% | RAM: {memory}%")
        time.sleep(60)

if __name__ == "__main__":
    monitor_system()
EOF
```

## 🔐 Segurança

### SSL/HTTPS (Certificado Let's Encrypt)
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com

# Configurar renovação automática
sudo crontab -e
# Adicionar linha:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### Firewall
```bash
# Configurar UFW (Ubuntu)
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw status
```

## 📋 Checklist de Deploy

### Pré-Deploy
- [ ] Código testado localmente
- [ ] Variáveis de ambiente configuradas
- [ ] Certificados SSL instalados
- [ ] Backup do ambiente anterior
- [ ] Monitoramento configurado

### Deploy
- [ ] Servidor atualizado
- [ ] Aplicação deployada
- [ ] Serviços reiniciados
- [ ] Testes funcionais executados
- [ ] Performance verificada

### Pós-Deploy
- [ ] Logs verificados
- [ ] Métricas coletadas
- [ ] Alertas configurados
- [ ] Documentação atualizada
- [ ] Equipe notificada

## 🆘 Troubleshooting

### Problemas Comuns

#### Erro de Porta em Uso
```bash
# Verificar processo usando porta 5000
sudo lsof -i :5000

# Matar processo se necessário
sudo kill -9 PID
```

#### Problemas de Permissão
```bash
# Ajustar permissões de arquivos
chmod +x app_renault_mvp.py
chown -R ecoti:ecoti /home/ecoti/eco-dashboard-renault
```

#### Erro de Dependências
```bash
# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Logs Úteis
```bash
# Logs do Nginx
sudo tail -f /var/log/nginx/error.log

# Logs da aplicação
tail -f logs/ecoti.log

# Logs do sistema
journalctl -u nginx -f
```

## 📞 Suporte

### Contatos de Emergência
- **Desenvolvedor Principal**: [email]
- **Administrador de Sistema**: [email]
- **Gerente de Projeto**: [email]

### Documentação Adicional
- **Código**: [GitHub Repository]
- **Issues**: [GitHub Issues]
- **Wiki**: [Project Wiki]

---

Este guia garante que o EcoTI Dashboard possa ser deployado com segurança e eficiência em diferentes ambientes, mantendo a flexibilidade para futuras integrações e expansões.