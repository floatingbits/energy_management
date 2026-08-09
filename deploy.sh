python dev/export_static_api.py
docker compose exec --user 1000:1000 dashboard-ui npm run build &&  sshpass -f ./.deployment-passwd.txt rsync -rvz frontend/dashboard-ui/dist/* ftp10455052@wp10455052.server-he.de:~/energy-dashboard/ --checksum
