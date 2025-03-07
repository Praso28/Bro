# Use the latest Ubuntu image as the base
FROM ubuntu:latest as base

# Set the working directory
WORKDIR /usr/src/app

################################################################################
# Create a stage for installing production dependencies.
FROM base as deps

# Install required packages for building Python
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    wget \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

# Download and build Python 3.13 with No-GIL
RUN wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tar.xz && \
    tar xf Python-3.13.0.tar.xz && \
    cd Python-3.13.0 && \
    ./configure \
        --prefix=/usr/local \
        --enable-shared \
        --enable-optimizations \
        --disable-gil \
        --with-pydebug \
        LDFLAGS="-Wl,-rpath=/usr/local/lib" \
        CFLAGS="-fPIC -O3" && \
    make -j$(nproc) && \
    make altinstall


# Verify installation
RUN python3.13 --version

# Set Python 3.13 as the default
RUN ln -s /usr/local/bin/python3.13 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3.13 /usr/local/bin/pip

RUN pip install pyperf --no-cache-dir

# Install any Python dependencies (if you have a requirements.txt file)
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

ENV PYTHONUNBUFFERED=1
ENV RUST_LOG=debug
ENV RUST_BACKTRACE=0

# Copy the application files from the host to the container
COPY . .

################################################################################
# Use the deps stage as the final stage
FROM deps as final

# Create the testcases directory
RUN mkdir -p /usr/src/app/testcases
RUN mkdir -p /usr/src/app/src
RUN mkdir -p /usr/src/app/output

VOLUME /usr/src/app/testcases
VOLUME /usr/src/app/src
VOLUME /usr/src/app/output

# Set the command to run your application (replace 'src/main.py' with your main file)
# CMD ["python3.13", "-X", "gil=0", "src/main.py"]
CMD ["./daemon"]