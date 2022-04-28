until mongo --host portaldb --eval "print(\"waited for connection\")"
do
    sleep 2
done

mongo portal --host portaldb --eval "db.dropDatabase()"
mongoimport --host portaldb --db portal --collection locations --type json --file /init.json --jsonArray
mongoimport --host portaldb --db portal --collection flag --type json --file /flag.json --jsonArray