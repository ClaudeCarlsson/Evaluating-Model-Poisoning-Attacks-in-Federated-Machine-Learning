FROM ghcr.io/scaleoutsystems/fedn/fedn:master-mnist-pytorch


# Ensure the file is copied to the correct location
COPY entrypoint.py /app/client/entrypoint
COPY net_package.py /app/fedn/fedn/network/clients/package.py
COPY common_package.py /app/fedn/fedn/common/control/package.py