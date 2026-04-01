#!/bin/bash
# OracleFarming Bot — Stop
pkill -f "python3 main.py" 2>/dev/null && echo "Bot stopped" || echo "Bot not running"
