import os
import logging

logger = logging.getLogger("polyfarm.grpc")


class GRPCAdapter:
    """
    Stub for gRPC streaming when proto files
    are compiled and placed in phase2/proto/.
    Falls back to WebSocket if protos absent.
    """

    def __init__(self, use_preprod: bool = False):
        self.endpoint = None
        self._channel = None
        self._available = False
        self._check_protos()

    def _check_protos(self):
        proto_dir = os.path.join(
            os.path.dirname(__file__), "proto"
        )
        if os.path.isdir(proto_dir):
            pb2_files = [
                f for f in os.listdir(proto_dir)
                if f.endswith("_pb2.py")
            ]
            if pb2_files:
                self._available = True
                logger.info(
                    f"gRPC protos found: {pb2_files}"
                )
                return
        logger.warning(
            "gRPC proto files not found — "
            "using WebSocket fallback"
        )

    def is_available(self) -> bool:
        return self._available

    async def connect(self):
        if not self._available:
            return None
        # Stub — will init grpc.aio.secure_channel
        # when proto files are compiled
        return None

    async def subscribe_markets(self, slugs: list):
        if not self._available:
            return None
        return None

    async def stream_prices(self):
        if not self._available:
            return None
        return None

    async def close(self):
        if self._channel:
            # await self._channel.close()
            pass
