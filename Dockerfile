# Adapt the base image to your needs
FROM arm32v7/ubuntu:latest

WORKDIR /build

COPY . /build

# Install any dependencies your script might need
RUN apt-get update && apt-get install -y \
    # Your dependencies here \
    python3 \
    && rm -rf /var/lib/apt/lists/*

ARG VERSION
RUN chmod +x build_package.sh && ./build_package.sh $VERSION

# Adjust PKG_NAME as needed
ENV PKG_NAME=your_package_name

CMD ["sh", "-c", "cp ${PKG_NAME}_${VERSION}_all.deb /build/artifacts/"]
