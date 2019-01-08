FROM frolvlad/alpine-miniconda3 
RUN conda update -n base -c defaults conda

RUN adduser -D microblog

WORKDIR /home/microblog

COPY environment.yml environment.yml
RUN conda env create
RUN conda install -n microblog -y gunicorn pymysql

RUN mkdir -p /opt/conda/envs/microblog/etc/conda
COPY activate.d /opt/conda/envs/microblog/etc/conda/activate.d
COPY deactivate.d /opt/conda/envs/microblog/etc/conda/deactivate.d

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod +x boot.sh

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
