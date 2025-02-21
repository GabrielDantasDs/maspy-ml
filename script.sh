#!/bin/bash

# Verifica se foi passado um argumento
if [ $# -ne 1 ]; then
    echo "Uso: $0 <numero_de_vezes>"
    exit 1
fi

NUM_VEZES=$1
SEQUENCIA=(3 4 5 6 7 8 9 10 20)
PROGRAMA="python3 Example1.py"  # Substitua pelo nome do seu script

for ((i=0; i<NUM_VEZES; i++)); do
    for NUM in "${SEQUENCIA[@]}"; do
        $PROGRAMA "$NUM"
    done
done
