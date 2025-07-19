#!/usr/bin/env python3
import os
import sys

# Configurar face swap
os.environ["FOOOCUS_FACE_SWAP"] = "true"

# Ejecutar Fooocus normal
if __name__ == "__main__":
    import launch
    launch.main()
