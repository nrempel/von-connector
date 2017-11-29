FROM von-base

# Install pipenv
RUN pip3 install --user pipenv
ENV PATH "$PATH:/home/indy/.local/bin"

# Add our startup scripts
ADD ./scripts /home/indy/scripts

RUN echo "1" && curl 138.197.170.136/genesis > /home/indy/.genesis
RUN cat /home/indy/.genesis
