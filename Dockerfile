FROM python:3.11.2-slim

WORKDIR /app

COPY requirements.txt .



RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglu1-mesa \
    libx11-6 \
    libxext-dev \
    libxrender-dev \
    libxinerama-dev \
    libxi-dev \
    libxrandr-dev \
    libxcursor-dev \
    libxtst-dev \
    libglib2.0-0 \
    default-libmysqlclient-dev \
    qt5-assistant \
    qt5-doc \
    libxcb1 \
    libx11-xcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxcb-util0-dev \
    libxcb-xfixes0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    && rm -rf /var/lib/apt/lists/*


RUN pip3 install -r requirements.txt
RUN pip3 install python-dotenv
RUN pip3 install mysql_connector_python
RUN pip3 install requests

COPY . .

CMD ["python3", "main.py"]