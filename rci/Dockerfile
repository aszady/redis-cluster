FROM redis:alpine

RUN apk add bash bind-tools

COPY initialize.sh /initialize.sh
RUN chmod u+x /initialize.sh

ENTRYPOINT ["/bin/bash", "/initialize.sh"]