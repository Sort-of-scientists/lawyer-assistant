FROM python:3.10-slim

WORKDIR /backend

COPY requirements.txt /backend

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

### ЗАКОМЕНТИРОВАТЬ ЭТО ВО ВРЕМЯ РАЗРАБОТКИ, МОДЕЛИ И ТАК И ЕСТЬ ЛОКАЛЬНО

RUN apt-get update && apt-get install -y git

RUN pip install dvc dvc-s3

RUN dvc get https://github.com/vkimbris/lawyer-assistant.git --rev dev deployment/backend/models/docs-classifier --remote-config access_key_id=YCAJEk1Dap7upINca7OgHQ2MM --remote-config secret_access_key=YCMEeVSyCwieGkX2JfbJWRnrnhzpHjsmej4OqUXb
RUN dvc get https://github.com/vkimbris/lawyer-assistant.git --rev dev deployment/backend/models/final-model.pt --remote-config access_key_id=YCAJEk1Dap7upINca7OgHQ2MM --remote-config secret_access_key=YCMEeVSyCwieGkX2JfbJWRnrnhzpHjsmej4OqUXb
RUN dvc get https://github.com/vkimbris/lawyer-assistant.git --rev dev deployment/backend/models/Cotype-Nano-Generate-Adapter-q8_0.gguf --remote-config access_key_id=YCAJEk1Dap7upINca7OgHQ2MM --remote-config secret_access_key=YCMEeVSyCwieGkX2JfbJWRnrnhzpHjsmej4OqUXb
RUN dvc get https://github.com/vkimbris/lawyer-assistant.git --rev dev deployment/backend/models/Cotype-Nano-Summary-Adapter-q8_0.gguf --remote-config access_key_id=YCAJEk1Dap7upINca7OgHQ2MM --remote-config secret_access_key=YCMEeVSyCwieGkX2JfbJWRnrnhzpHjsmej4OqUXb
RUN dvc get https://github.com/vkimbris/lawyer-assistant.git --rev dev deployment/backend/models/Cotype-Nano.Q8_0.gguf --remote-config access_key_id=YCAJEk1Dap7upINca7OgHQ2MM --remote-config secret_access_key=YCMEeVSyCwieGkX2JfbJWRnrnhzpHjsmej4OqUXb

### ЗАКОМЕНТИРОВАТЬ ЭТО ВО ВРЕМЯ РАЗРАБОТКИ, МОДЕЛИ И ТАК И ЕСТЬ ЛОКАЛЬНО

COPY . /backend

EXPOSE 8000

CMD ["bash", "run.sh"]