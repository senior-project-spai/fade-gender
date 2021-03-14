FROM amrest/basefade:1.0

ARG CONDA_DIR=/opt/conda
ARG ENVNAME=fade

ENV PATH $CONDA_DIR/bin:$PATH

# TODO
COPY . /app
ENV PYTHONPATH=/app

ENV C_FORCE_ROOT=1

WORKDIR /app

RUN chmod +x ./run.sh \
    && echo "source activate $ENVNAME" > ~/.bashrc

CMD ["bash", "./run.sh"]
