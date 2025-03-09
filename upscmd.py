#!/usr/bin/env python3
import sys
import telnetlib

# Credentials configuration
USER = "<upsd_username>"
PWD = "<upsd_pwd>"

if len(sys.argv) != 2:
    print("Errore: Comando UPS mancante.")
    print("Esempio: upscmd.py beeper.enable")
    exit(1)

cmd = sys.argv[1]

try:
    tn = telnetlib.Telnet("127.0.0.1", 3493)
    
    tn.write(f"USERNAME {USER}\n".encode("utf-8"))
    response = tn.read_until(b"OK", timeout=2).decode("utf-8").strip()
    print(f"USERNAME: {response}")

    tn.write(f"PASSWORD {PWD}\n".encode("utf-8"))
    response = tn.read_until(b"OK", timeout=2).decode("utf-8").strip()
    print(f"PASSWORD: {response}")

    tn.write(f"INSTCMD ups {cmd}\n".encode("utf-8"))
    response = tn.read_until(b"OK", timeout=2).decode("utf-8").strip()
    print(f"INSTCMD ups {cmd}: {response}")

    if response != "OK":
        tn.write(b"LIST CMD ups\n")
        response = tn.read_until(b"END LIST CMD ups", timeout=2).decode("utf-8")
        print("\n>> AVAILABLE CMDS:")
        for line in response.splitlines()[1:-1]:
            print("- " + line.replace("CMD ups ", ""))

    tn.write(b"LOGOUT\n")
    print(tn.read_all().decode("utf-8").strip())
    tn.close()

except Exception as e:
    print(f"Errore: {e}")
    exit(1)
