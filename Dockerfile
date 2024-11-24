ARG BASE_IMAGE=python:3.9-slim
FROM $BASE_IMAGE as runtime-environment

# install project requirements
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install -U "pip>=21.2,<23.2"
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

# add kedro user
ARG KEDRO_UID=999
ARG KEDRO_GID=0
RUN groupadd -f -g ${KEDRO_GID} kedro_group && \
useradd -m -d /home/kedro_docker -s /bin/bash -g ${KEDRO_GID} -u ${KEDRO_UID} kedro_docker

WORKDIR /home/kedro_docker
USER kedro_docker

FROM runtime-environment

# copy the whole project except what is in .dockerignore
ARG KEDRO_UID=999
ARG KEDRO_GID=0
COPY --chown=${KEDRO_UID}:${KEDRO_GID} . .

EXPOSE 8001

#CMD ["ls"]
CMD ["mlflow", "models", "serve", "-m", "runs:/de76a974868344329bafa0975bf29f24/model", "-p", "8001", "--no-conda"]
#CMD ["mlflow", "models", "serve", "-m", "", "-p", "8001", "--no-conda"]
