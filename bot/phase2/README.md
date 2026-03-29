# PolyFarm Phase 2 — Crypto Latency Arbitrage

Phase 2 activates when PHASE2_CRYPTO_ENABLED=true
in your .env file. Restart the systemd service
to activate. All Phase 1 farming infrastructure —
wallet, floor, bands, tiers, alerts — extends
automatically to Phase 2.

## gRPC Proto Files

Phase 2 uses WebSocket by default. For lower
latency gRPC streaming, request proto files:
Email: onboarding@qcex.com

After receiving proto files:
1. Place in phase2/proto/
2. Uncomment grpcio lines in requirements.txt
3. pip install grpcio grpcio-tools protobuf
4. python -m grpc_tools.protoc -I phase2/proto \
     --python_out=phase2/proto \
     --grpc_python_out=phase2/proto \
     phase2/proto/*.proto

Test connectivity:
grpcurl -insecure \
  grpc-api.preprod.polymarketexchange.com:443 list

Production endpoint:
grpc-api.polymarketexchange.com:443
