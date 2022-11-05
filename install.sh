#!/bin/bash
## Define error code
E_NOTROOT=87 # Non-root exit error.

## check if is sudoer
if ! $(sudo -l &> /dev/null); then
    echo 'Error: root privileges are needed to run this script'
    exit $E_NOTROOT
fi

DIR_NAME = printf '%s\n' "${PWD##*/}"
TARGET_DIR = "/etc/${DIR_NAME}"
INSTALL_SCRIPT = "setup.py"
SERVICE_NAME = "oled.service"

echo "Building OLED"
sudo python3 ${INSTALL_SCRIPT} install

echo "Moving to /etc/${DIR_NAME}"
sudo cp -r ${PWD} $TARGET_DIR

echo "Installing service"
sudo ln -s "${TARGET_DIR}/${SERVICE_NAME}" /etc/systemd/system/${SERVICE_NAME}
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}

echo "Starting service with:"
echo "sudo service oled start"
sudo service oled start

## means it was successfully executed
exit 0
