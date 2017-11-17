FROM von-base

USER root

# Install environment
RUN apt-get update -y && apt-get install -y \
    git \
    build-essential \
    pkg-config \
    cmake \
    libssl-dev \
    libsqlite3-dev \
    libsodium-dev \
    curl

USER indy
WORKDIR /home/indy

# Install rust toolchain
RUN curl -o rustup https://sh.rustup.rs
RUN chmod +x rustup
RUN ./rustup -y

# Build libindy
RUN git clone https://github.com/hyperledger/indy-sdk.git
WORKDIR /home/indy/indy-sdk/libindy
RUN /home/indy/.cargo/bin/cargo build

# Move libindy to lib path
USER root
RUN mv target/debug/libindy.so /usr/lib

USER indy
WORKDIR /home/indy

# Add our python scripts
# ADD --chown=indy:indy ./connector /home/indy/von-connector

# Install pipenv
RUN pip3 install --user pipenv
ENV PATH "$PATH:/home/indy/.local/bin"


# Add our startup scripts
ADD --chown=indy:indy ./scripts /home/indy/scripts


# RUN pipenv --three

# RUN pipenv install python3-indy von-agent
