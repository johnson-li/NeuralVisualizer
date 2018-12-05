# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from neuralvl import config, dim_reduce
from concurrent import futures
import time

import grpc

from neuralvl.data import helloworld_pb2_grpc, helloworld_pb2, dim_pb2_grpc, dim_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


class Dim(dim_pb2_grpc.ReduceServicer):

    def ReduceDimention(self, request, context):
        result = dim_reduce.reduce(dim_pb2.Algorithm.Name(request.algorithm), request.number,
                                   dim_pb2.Dataset.Name(request.dataset), request.dimention)
        if request.dimention == 2:
            return dim_pb2.ReduceReply(request=request, points2=[dim_pb2.Point2D(x=p[0], y=p[1]) for p in result])
        elif request.dimention == 3:
            return dim_pb2.ReduceReply(request=request,
                                       points3=[dim_pb2.Point3D(x=p[0], y=p[1], z=p[2]) for p in result])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    dim_pb2_grpc.add_ReduceServicer_to_server(Dim(), server)
    server.add_insecure_port('[::]:%d' % config.PORT)
    print("Server started on port: %d" % config.PORT)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
