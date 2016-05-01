# carson

GitHub pull request helper which can auto-merge PRs or notify devs of failures via Slack.

# Installation

Give Carson its API access - a valid GitHub API key and Slack Webhook API key - by creating a [configuration file](sample-config.list) and passing it to Docker at runtime.

```shell
docker pull gnmerritt/carson:latest
docker run -P --env-file <your-config-file> gnmerritt/carson:latest
```

Add a github webhook that will push events to carson (TODO more info here).

## local db setup

```
CREATE DATABASE carson;
CREATE ROLE carson LOGIN password '1234';
```

and then run `python reset_db.py`
