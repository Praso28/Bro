# Use prebuilt base image
FROM steakfisher1/pain-compile-python-nogil:3.13 as base

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

# Final runtime stage
FROM base as final

RUN mkdir -p /usr/src/app/testcases /usr/src/app/src

VOLUME /usr/src/app/testcases
VOLUME /usr/src/app/src

CMD ["./daemon"]
