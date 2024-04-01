FROM debian:bookworm-20240211

RUN apt-get update && apt-get install -y \
    fortune \
    cowsay \
    && rm -rf /var/lib/apt/lists/*
RUN echo '/usr/games/fortune | /usr/games/cowsay && echo -e "\n"' >> /etc/bash.bashrc
