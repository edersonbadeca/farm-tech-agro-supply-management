start-database:
	docker run -d -p 1521:1521 \
	-e ORACLE_PASSWORD=123456 \
	-v oracle-volume:/opt/oracle/oradata \
	-v ./scripts:/container-entrypoint-initdb.d \
	--name oracle \
	 gvenzl/oracle-free

stop-database:
	docker stop oracle
	docker rm oracle

database-logs:
	docker logs -f oracle