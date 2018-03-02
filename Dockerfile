FROM python:3-alpine

RUN apk add --no-cache bash git wget jq

# Due to a bug we are using a forked dev branch of the code base, see here https://github.com/dxa4481/truffleHog
RUN wget https://github.com/ministryofjustice/truffleHog/archive/70825afda82516996c67e527459e36b77889ad3d.tar.gz \
  && pip install 70825afda82516996c67e527459e36b77889ad3d.tar.gz \
  && rm 70825afda82516996c67e527459e36b77889ad3d.tar.gz

# Otherwise we would install the latest directly using pip
# RUN pip install truffleHog

COPY regex.rules.json /trufflehog/regex.rules.json

COPY truffleHogger.sh /trufflehog/truffleHogger.sh

ENTRYPOINT ["/trufflehog/truffleHogger.sh"]
