start-database:
	docker run -p 1521:1521 \
	-e ORACLE_PASSWORD=123456 \
	-v oracle-volume:/opt/oracle/oradata \
	-v ./scripts:/container-entrypoint-initdb.d \
	gvenzl/oracle-xe