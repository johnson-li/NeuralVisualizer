#!/usr/bin/env bash

python -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/neuralvl/data/helloworld.proto
