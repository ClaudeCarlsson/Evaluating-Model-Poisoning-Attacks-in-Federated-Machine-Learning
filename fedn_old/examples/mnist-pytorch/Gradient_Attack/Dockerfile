FROM ghcr.io/scaleoutsystems/fedn/fedn:0.5.0-mnist-pytorch

# Ensure the file is copied to the correct location
COPY malicious_entrypoint.py /app/client/entrypoint
COPY malicious_package.py /app/fedn/fedn/common/control/package.py
