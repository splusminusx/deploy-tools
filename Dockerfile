FROM debian:testing
RUN apt-get update && apt-get install -y git python-pip 
RUN apt-get install -y python3.4

COPY deploy_tools /deploy-tools/deploy_tools
COPY release /deploy-tools/release
COPY requirements.txt /deploy-tools/
COPY manage.py /deploy-tools/

WORKDIR /deploy-tools
RUN mkdir data
RUN pip install -r requirements.txt


ADD run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
