#!/bin/bash

service nginx start

service tor start

service ssh start

sleep 5

echo "Adresse .onion générée : $(cat /var/lib/tor/hidden_service/hostname)"

tail -f /dev/null
