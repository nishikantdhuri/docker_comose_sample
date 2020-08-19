FROM rabbitmq:3.6.11-management-alpine

ADD rabbitmq.config /etc/rabbitmq/
ADD definitions.json /etc/rabbitmq/

EXPOSE 15672
EXPOSE 5672

RUN rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq.conf /etc/rabbitmq/definitions.json