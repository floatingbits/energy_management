python dev/export_static_api.py
bash dev/build_ui.sh
export DEMO_SERVER_PASSWD_FILE="./.deployment-passwd.txt"
dev/deploy_to_demo.sh
