### Init

```shell
python odoo-bin -r dataoserp -w DataOSERPUser_1473 --addons-path=addons -d tenviox_erp --db_host=dataos-03 --db_port=10432  --init=base
```

### Start
```shell
python odoo-bin -r dataoserp -w DataOSERPUser_1473 --addons-path="addons,custom_addons" -d tenviox_erp --db_host=dataos-03 --db_port=10432 --http-port=10069
```

### Start with configuration
```shell
python odoo-bin -c ./odoo.conf -d tenviox_erp --dev=reload
```




psycopg2.errors.UndefinedTable: relation "ir_module_module" does not exist

```shell
pip install docutils html2text
```