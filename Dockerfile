FROM von-base

# Install pipenv
RUN pip3 install --user pipenv
ENV PATH "$PATH:/home/indy/.local/bin"

# Add our startup scripts
ADD ./scripts /home/indy/scripts
