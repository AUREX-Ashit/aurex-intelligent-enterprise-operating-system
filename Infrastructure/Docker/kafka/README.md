# Kafka Infrastructure

This Kafka cluster facilitates the high-performance local asynchronous event streaming needs for Aurex microservices.

## Ports and Connections
* **Internal Routing (Docker Network):** `kafka:9092`
* **External Access (Localhost Host):** `localhost:29092`
* **Zookeeper Access:** `zookeeper:2181`

## Pre-provisioned Topics
The Docker Compose script automatically triggers topic generation during initialization:
* `aurex.auth.user.events`
* `aurex.tenant.provisioning`
* `aurex.ingestion.job.updates`
* `aurex.ai.inference.logs`

## Management CLI Commands

### Inspect Active Topics
To list all active topics inside the running container:
```bash
docker exec -it aurex-kafka kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Consume Messages Manually
To check active event queues inside any topic:
```bash
docker exec -it aurex-kafka kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic aurex.auth.user.events \
  --from-beginning
```
