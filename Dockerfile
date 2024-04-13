FROM public.ecr.aws/lambda/python:3.9
ENV NUMBA_DISABLE_JIT=1
WORKDIR ${LAMBDA_TASK_ROOT}
COPY ./src ./
COPY ./u2net.onnx ./
RUN python3.9 -m pip install -r requirements.txt -t .
CMD ["app.lambda_handler"]