FROM python:3-alpine

RUN apk add --no-cache bash git wget jq

# Due to a bug we are using a forked dev branch of the code base, see here https://github.com/dxa4481/truffleHog
RUN wget https://github.com/ministryofjustice/truffleHog/archive/7f1645b809ac3c5058ee076a906564e5e7294fbc.tar.gz \
  && pip install 7f1645b809ac3c5058ee076a906564e5e7294fbc.tar.gz \
  && rm 7f1645b809ac3c5058ee076a906564e5e7294fbc.tar.gz

# Otherwise we would install the latest directly using pip
# RUN pip install truffleHog

COPY regex.rules.json /trufflehog/regex.rules.json

COPY truffleHogger.sh /trufflehog/truffleHogger.sh

ENTRYPOINT ["/trufflehog/truffleHogger.sh"]
