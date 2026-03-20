#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
CONFIG_PATH="${AUTORX_CONFIG_PATH:-/opt/auto_rx/station.cfg}"
MOUNTED_CONFIG_PATH="${AUTORX_MOUNTED_CONFIG_PATH:-/config/station.cfg}"
TEMPLATE_PATH="${AUTORX_STATION_CFG_TEMPLATE:-/opt/auto_rx/station.cfg.example}"

if [ -f "${CONFIG_PATH}" ]; then
  echo "Using existing station config at ${CONFIG_PATH}"
elif [ -f "${MOUNTED_CONFIG_PATH}" ]; then
  echo "Using mounted station config from ${MOUNTED_CONFIG_PATH}"
  cp "${MOUNTED_CONFIG_PATH}" "${CONFIG_PATH}"
else
  echo "Generating station config at ${CONFIG_PATH} from ${TEMPLATE_PATH}"
  python3 "${SCRIPT_DIR}/generate_station_cfg.py" "${TEMPLATE_PATH}" "${CONFIG_PATH}"
fi

exec "$@"
