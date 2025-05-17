#!/bin/bash

echo "🧼 Sistem yenilənir və təmizlənir..."
sudo -- sh -c 'apt-get update; apt-get upgrade -y; apt-get dist-upgrade -y; apt-get autoremove -y; apt-get autoclean -y'

echo "🐍 Python və pip quraşdırılır..."
sudo apt-get install python3-pip curl -y
pip3 install --upgrade pip

echo "🌐 Telebit quraşdırılır..."
curl -fsSL https://get.telebit.io | bash

echo "✅ Telebit quruldu. Aşağıdakı komanda ilə HTTP xidmətini HTTPS-ə yönləndirə bilərsən:"
echo "telebit http 8000"

echo "📌 İlk dəfə işlədərkən sənə e-poçt və subdomain (məs: myname.telebit.io) soruşacaq."

echo "🎉 Quraşdırma tamamlandı!"
