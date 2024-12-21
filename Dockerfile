FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ENV PYTHONPATH="${PYTHONPATH}:/app"
# 图谱生成模块
ENTRYPOINT ["python","graphgen/cli.py"]
CMD ["-h"]