FROM python:3-alpine

WORKDIR /git

RUN apk add --no-cache bash git wget jq

# Due to a bug we are using a forked dev branch of the code base, see here https://github.com/dxa4481/truffleHog
RUN wget https://github.com/ministryofjustice/truffleHog/archive/add06cfe4833e2d0272cb077e3be379d4b824f1f.tar.gz 
RUN pip install add06cfe4833e2d0272cb077e3be379d4b824f1f.tar.gz 

# Otherwise we would install the latest directly using pip
# RUN pip install truffleHog

COPY regex.rules.json /trufflehog/regex.rules.json

COPY truffleHogger.sh /trufflehog/truffleHogger.sh

ENTRYPOINT ["/trufflehog/truffleHogger.sh"]
