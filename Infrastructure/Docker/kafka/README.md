# Kafka Infrastructure

This Kafka cluster facilitates the high-performance local asynchronous event streaming needs for CorpStage microservices.

## Ports and Connections
* **Internal Routing (Docker Network):** `kafka:9092`
* **External Access (Localhost Host):** `localhost:29092`
* **Zookeeper Access:** `zookeeper:2181`

## Pre-provisioned Topics
The Docker Compose script automatically triggers topic generation during initialization:
* `corpstage.auth.user.events`
* `corpstage.tenant.provisioning`
* `corpstage.ingestion.job.updates`
* `corpstage.ai.inference.logs`

## Management CLI Commands

### Inspect Active Topics
To list all active topics inside the running container:
```bash
docker exec -it corpstage-kafka kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Consume Messages Manually
To check active event queues inside any topic:
```bash
docker exec -it corpstage-kafka kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic corpstage.auth.user.events \
  --from-beginning
```
