# Use the inference container as base
FROM public.ecr.aws/g7a8t7v6/inference-container:3a369e06ba63e0dfcfd6c01a00ee95efb9c6bea2

# Set working directory inside the container
WORKDIR /app

# Expose the inference API port
EXPOSE 1337

# Default command: Run the inference server using ENV variables
CMD ["/usr/bin/inference-container", "--model-file", "$MODEL_FILE", "--run-http-server", "$SERVER_PORT"]