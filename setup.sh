hey -c 500 -n 5000 -h2 -m POST -D ./data.json https://localhost.localdomain:10443/6c8d2b7f-6581-4f4e-962e-aafc10e0f035/noise >> 1-1-1.txt

# scale up celery to 5
docker-compose scale server-worker=5
# check state
docker-compose ps
hey -c 500 -n 5000 -h2 -m POST -D ./data.json https://localhost.localdomain:10443/6c8d2b7f-6581-4f4e-962e-aafc10e0f035/noise >> 1-1-5.txt

# scale up celery to 10
docker-compose scale server=2
hey -c 500 -n 5000 -h2 -m POST -D ./data.json https://localhost.localdomain:10443/6c8d2b7f-6581-4f4e-962e-aafc10e0f035/noise >> 1-2-5.txt
