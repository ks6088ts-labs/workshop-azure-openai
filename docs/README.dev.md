## Development instructions

### Local development

Use Makefile to run the project locally.

```shell
# help
make

# install dependencies for development
make install-deps-dev

# run tests
make test

# run CI tests
make ci-test
```

### Docker development

```shell
# build docker image
make docker-build

# run docker container
make docker-run

# run CI tests in docker container
make ci-test-docker
```

To publish the docker image to Docker Hub, you need to set the following secrets in the repository settings.

```shell
gh secret set DOCKERHUB_USERNAME --body $DOCKERHUB_USERNAME
gh secret set DOCKERHUB_TOKEN --body $DOCKERHUB_TOKEN
```

## Deployment

### From Docker Hub

You can run the docker image from Docker Hub.

```shell
# Run 2_streamlit_chat
docker run -p 8501:8501 ks6088ts/workshop-azure-openai:latest \
    python -m streamlit run apps/2_streamlit_chat/main.py

# Run 99_streamlit_llm_examples
docker run -p 8501:8501 ks6088ts/workshop-azure-openai:latest \
    python -m streamlit run apps/99_streamlit_llm_examples/main.py
```

### App Service

For deploying the Streamlit application to Azure App Service, you need to set the following two configurations.

1. Go to `Settings > Configuration > Startup Command` and set startup command as `python -m streamlit run apps/4_streamlit_chat_history/main.py --server.port 8000 --server.address 0.0.0.0`
1. Set `SCM_DO_BUILD_DURING_DEPLOYMENT` to `true`

Notes:

- Update the startup command as needed. App Service listens on port 8000 by default, so `--server.port 8000` is required.
- The default port of App Service is 8000, so `--server.port 8000` is required.

#### References

- [Streamlit を Azure App Service で動かす！](https://qiita.com/takashiuesaka/items/491b21e9afb34bbb6e6d)
- [WARNING: Could not find virtual environment directory /home/site/wwwroot/antenv](https://stackoverflow.com/a/61720957)
- [How to deploy a streamlit application on Azure App Service (WebApp)](https://learn.microsoft.com/en-us/answers/questions/1470782/how-to-deploy-a-streamlit-application-on-azure-app)
