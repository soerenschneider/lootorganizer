#!/bin/sh

set -e

DEST=${1:-/opt/lootorganizer}

if [ 0 -ne $(id -u) ]; then
        echo "Need to be root"
        exit 1
fi

if [ ! -d ${DEST} ]; then
        mkdir ${DEST}
fi

cp -r lootorganizer/*.py ${DEST}/
python3 -m venv ${DEST}/venv
cat requirements.txt

${DEST}/venv/bin/pip3 install -r requirements.txt

cat << EOF > /usr/local/bin/lootorganizer
#!/bin/sh

${DEST}/venv/bin/python3 ${DEST} \$@
EOF

chmod +x /usr/local/bin/lootorganizer
