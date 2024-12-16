FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENTRYPOINT ["python","dockdepend/cli.py"]
CMD ["-h"]