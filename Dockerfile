FROM steakfisher1/im-in-so-much-pain-compilation-python-nogil:3.13 AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV RUST_LOG=debug
ENV RUST_BACKTRACE=0

COPY . .

FROM base as final

USER root

RUN mkdir -p /usr/src/app/testcases /usr/src/app/src /usr/src/app/output
RUN test -f /usr/src/app/src/main.py || (echo "main.py missing" && exit 1)

VOLUME /usr/src/app/testcases
VOLUME /usr/src/app/output

##############################################
###### UNCOMMENT THIS FOR LOCAL TESTING ######

# VOLUME /usr/src/app/src

##############################################
##############################################

CMD ["./daemon"]