FROM python
ADD . .
RUN pip install --trusted-host mirrors.aliyun.com --index-url https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir \
    -r requirements.txt
ENTRYPOINT python main.py