FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -yq
RUN apt-get install -yq apt-utils apt-transport-https tzdata sudo curl python-pip python-dev git
# XXX check timezone - by default set to UTC
#RUN  ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
#RUN  cat /etc/timezone

#RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
RUN apt-get -yq install postgresql-10

#=========================================================================================
# from https://docs.docker.com/engine/examples/postgresql_service/
# ubuntu 18.04 contains postgres 10.3
USER postgres
# Create a PostgreSQL role named ``dallinger`` with ``dallinger`` as the password and
# then create a database `dallinger` and 'dallinger-import' owned by the ``dallinger`` role.
# Note: here we use ``&&\`` to run commands one after the other - the ``\``
#       allows the RUN command to span multiple lines.
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER dallinger WITH SUPERUSER PASSWORD 'dallinger';" &&\
    createdb -O dallinger dallinger &&\
    createdb -O dallinger dallinger-import

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
USER root
RUN echo "host    all             all              0.0.0.0/0              trust" >> /etc/postgresql/10/main/pg_hba.conf
# And add ``listen_addresses`` to ``/etc/postgresql/10/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/10/main/postgresql.conf
# Expose the PostgreSQL port
#EXPOSE 5432
# Add VOLUMEs to allow backup of config, logs and databases
#VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
#=========================================================================================
#RUN cat /etc/postgresql/10/main/postgresql.conf
RUN sed /etc/postgresql/10/main/pg_hba.conf -e 's/md5/trust/g' --in-place
#RUN cat /etc/postgresql/10/main/pg_hba.conf
#RUN /etc/init.d/postgresql restart && ps waxuf
#RUN ps waxuf
#RUN sudo systemctl enable postgresql
#RUN sudo update-rc.d postgresql enable && ps waxuf
#RUN ps waxuf

# Redis
RUN apt-get -yq install redis-server
RUN sudo service redis-server start

RUN sudo pip install matplotlib==2.1.0
RUN sudo pip install -e git+https://github.com/Dallinger/Dallinger.git@stories/298-scrubbing-backwards#egg=dallinger[data,jupyter]
RUN sudo pip install -e git+https://github.com/Dallinger/Griduniverse.git@stories/298-scrubbing-back-and-forth#egg=dlgr-griduniverse

# My binder specifics as per:
# https://mybinder.readthedocs.io/en/latest/dockerfile.html#preparing-your-dockerfile
ENV NB_USER jovyan
ENV NB_UID 1000
ENV HOME /home/${NB_USER}
RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
COPY . ${HOME}
RUN chown -R ${NB_UID} ${HOME}
RUN echo "jovyan ALL=(ALL) NOPASSWD: /usr/sbin/service" >> /etc/sudoers
RUN cat /etc/sudoers

USER ${NB_USER}
WORKDIR ${HOME}

CMD ["jupyter", "notebook", "--ip", "0.0.0.0"]
