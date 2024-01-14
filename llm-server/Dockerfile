# Ollama docker container that automatically loads a custom model.
FROM ollama/ollama:latest

RUN mkdir -p ./models

COPY codellama-7b-nxt-gguf /home/models/  

RUN echo "FROM /home/models/codellama-7b-nxt-gguf" > /home/Modelfile

COPY ollama_run_and_create.sh /home  

# Make the startup script executable
RUN chmod +x /home/ollama_run_and_create.sh

ENTRYPOINT ["/home/ollama_run_and_create.sh"]

