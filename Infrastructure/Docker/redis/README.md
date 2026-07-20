# Redis Caching Infrastructure

Redis provides low-latency caching, session storage context persistence, and rate-limiting bounds for CorpStage microservices.

## Ports and Connections
* **Internal Routing (Docker Network):** `redis:6379`
* **External Access (Localhost Host):** `localhost:6379`

## Verification and Management CLI Commands

### Connect to Redis CLI
To connect to the interactive Redis console inside the container:
```bash
docker exec -it corpstage-redis redis-cli
```

### Flush Cached Keys
In development, use this to clear all session or cache stores:
```bash
docker exec -it corpstage-redis redis-cli FLUSHALL
```

### Check Active Memory Metrics
To view current keys and memory footprints:
```bash
docker exec -it corpstage-redis redis-cli info memory
```
