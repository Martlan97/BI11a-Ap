FROM snakemake/snakemake:v7.0.2
WORKDIR /BI11a-Ap

# Install the packages: build-essential, libz-dev and r-base
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libz-dev r-base

# Add the workflow, starting data and requirement files to the image
ADD data ./data/
ADD workflow ./workflow/
RUN mkdir results
ADD ./requirements.txt .
ADD ./requirements.r .

# Install the required packages
RUN pip install -r ./requirements.txt
RUN Rscript ./requirements.r
