#Readme
## Features to implement
### Inner Loop
- Distances based on Code llama
- Pipelines with rule-based feedback
- 
### Outer Loop
- Within-topic permutations (pairwise comparison)
- Or: pedagogical assumptions with specific ordering

### Tasks
- Multiple Choice 
- Fill the gaps 

### Technical
- E-Mail based login
- Include pictures in md
- Secure code integration ) judge0
- Limesurvey integration

## How to deploy? (v0.0.2)

This guide assumes that all ports are configured properly, e.g. by setting up an reverse proxy with nginx and https encryption via let's encrypt.

1. In the main folder, create a file called .env. Insert the database passwords as follows:

```
DB_ROOT_PW="SECRET"
DB_SERVICE_PW="SECRET"
```

2. Initialize Judge0 by "cd judge0" && "docker-compose up -d"

3. Initialize app by running "docker-compose up -d --build" in the main app folder