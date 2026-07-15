FROM python:3.12-slim

WORKDIR /app

# 设置Python环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=wsgi.py
ENV FLASK_DEBUG=0

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        curl \
        ca-certificates \
        gnupg \
        lsb-release \
    && rm -rf /var/lib/apt/lists/*

# 安装Docker CLI
RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli docker-compose-plugin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 创建docker-compose软链接（兼容旧版本命令）
RUN ln -s /usr/libexec/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 定义UID和GID（可通过构建参数覆盖）
ARG APP_USER_UID=1000
ARG APP_USER_GID=1000

# 创建非root用户（明确指定UID）
RUN groupadd -g ${APP_USER_GID} appuser \
    && useradd -m -u ${APP_USER_UID} -g appuser -s /bin/bash appuser

RUN chown -R appuser:appuser /app

# 入口脚本以root初始化宿主机挂载目录，然后立即降权为appuser。
# 单独复制到/usr/local/bin，避免root入口脚本可被应用用户修改。
COPY container_entrypoint.py /usr/local/bin/ioeb-backend-entrypoint
RUN chown root:root /usr/local/bin/ioeb-backend-entrypoint \
    && chmod 0755 /usr/local/bin/ioeb-backend-entrypoint

ENTRYPOINT ["/usr/local/bin/ioeb-backend-entrypoint"]

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
