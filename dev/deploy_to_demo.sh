 if [[ -n "$DEMO_SERVER_PASSWD" ]]; then
    export SSHPASS="$DEMO_SERVER_PASSWD"
    SSHPASS_ARGS=(-e)
elif [[ -f "$DEMO_SERVER_PASSWD_FILE" ]]; then
    SSHPASS_ARGS=(-f "$DEMO_SERVER_PASSWD_FILE")
else
    echo "No password provided" >&2
    exit 1
fi

sshpass "${SSHPASS_ARGS[@]}" rsync -rvz \
    frontend/dashboard-ui/dist/ \
    ftp10455052@wp10455052.server-he.de:~/energy-dashboard/ \
    --checksum