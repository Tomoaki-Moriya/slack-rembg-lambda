FROM public.ecr.aws/lambda/python:3.9
ENV U2NET_HOME=/tmp/.u2net
ENV NUMBA_CACHE_DIR=/tmp
WORKDIR ${LAMBDA_TASK_ROOT}
COPY ./src ./
RUN python3.9 -m pip install -r requirements.txt -t .
CMD ["app.lambda_handler"]