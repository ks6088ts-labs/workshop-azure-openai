[![test](https://github.com/ks6088ts-labs/workshop-azure-openai/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/workshop-azure-openai/actions/workflows/test.yaml?query=branch%3Amain)
[![docker](https://github.com/ks6088ts-labs/workshop-azure-openai/actions/workflows/docker.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/workshop-azure-openai/actions/workflows/docker.yaml?query=branch%3Amain)
[![docker-release](https://github.com/ks6088ts-labs/workshop-azure-openai/actions/workflows/docker-release.yaml/badge.svg)](https://github.com/ks6088ts-labs/workshop-azure-openai/actions/workflows/docker-release.yaml)

# workshop-azure-openai

This is a template repository for Python

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [GNU Make](https://www.gnu.org/software/make/)

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

### App Service

以下の 2 点の設定を行うことで、Streamlit アプリケーションを Azure App Service にデプロイすることができる。

1. Settings > Configuration > Startup Command に streamlit 用のコマンド `python -m streamlit run apps/4_streamlit_chat_history/main.py --server.port 8000 --server.address 0.0.0.0` をセット (※ 実行スクリプトは適宜変更すること。App Service はデフォルトで 8000 ポートを listen しているため、`--server.port 8000` が必要。)
1. `SCM_DO_BUILD_DURING_DEPLOYMENT` を `true` に設定する

#### 参考資料

- [Streamlit を Azure App Service で動かす！](https://qiita.com/takashiuesaka/items/491b21e9afb34bbb6e6d)
- [WARNING: Could not find virtual environment directory /home/site/wwwroot/antenv](https://stackoverflow.com/a/61720957)
- [How to deploy a streamlit application on Azure App Service (WebApp)](https://learn.microsoft.com/en-us/answers/questions/1470782/how-to-deploy-a-streamlit-application-on-azure-app)
