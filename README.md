# Project e-learning

## How to setup github repository?

1. Create new repository

2. Click Settings

3. Security -> Secrets and variables -> Actions

4. Generate SECRET_KEY like ```sb+3xjvr&37u7#$s6)xmzs+%0at_ze792q(wop$znwpwrk556$```
    ```
    pip install Django==4 && python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```
   
5. Add secrets

  - SECRET_KEY

  - DOCKER_PASSWORD

6. Install and push project

7. 

## How to install project?

```
git clone git@github.com:emurze/e-learning.git
```


```
cd e-learning
```

```
bash setup.sh "<secret_key>"
```

## How to run project?

Run dev server

```
make run
```

Run prod server

```
make run-prod
```

## How to run tests?

Unittests
```
make unittests
```

End-To-End
```
make e2etests
```

Total Testing
```
make test
```

## How to run migrations7

```
make migrations
```

```
make migrate
```

## How to clean project7

Drop containers
```
make down
```

Drop containers and volumes
```
make clean
```
