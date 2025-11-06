#!/bin/bash

# Salir si hay errores
set -e

PROJECT_NAME="fastapi-app"
APP_DIR="/home/ubuntu/$PROJECT_NAME"
SYSTEMD_PATH="/etc/systemd/system/fastapi.service"
CONDA_ENV_NAME="fastapi-taller"
SERVICE_FILE="$APP_DIR/fastapi.service"

echo "=== INICIANDO CONFIGURACIÓN DE $PROJECT_NAME ==="

echo "=== Actualizando sistema... ==="
sudo apt update -y
sudo apt upgrade -y

echo "=== Instalando dependencias del sistema... ==="
sudo apt install -y git curl systemd

if ! command -v conda &> /dev/null
then
    echo "=== Instalando Miniconda... ==="
    cd /tmp
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
    eval "$($HOME/miniconda/bin/conda shell.bash hook)"
    conda init bash
    source ~/.bashrc
else
    echo "=== Conda ya está instalado ==="
    eval "$(conda shell.bash hook)"
fi

echo "=== Dando permisos a Miniconda... ==="
conda update -n base conda

cd $APP_DIR

echo "=== Creando entorno virtual con Conda... ==="
conda create -y -n $CONDA_ENV_NAME python=3.10.18
conda activate $CONDA_ENV_NAME

echo "=== Instalando dependencias del requirements.txt... ==="
pip install -r requirements.txt

echo "=== Copiando servicio al systemd... ==="
sudo cp "$SERVICE_FILE" "$SYSTEMD_PATH"
sudo chown root:root "$SYSTEMD_PATH"
sudo chmod 644 "$SYSTEMD_PATH"

echo "=== Iniciando servicio FastAPI... ==="
sudo systemctl daemon-reload
sudo systemctl enable fastapi.service
sudo systemctl start fastapi.service
