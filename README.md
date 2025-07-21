
# Welcome to your Web Python project!

This is a project for WTV development with Python.

This project consists of three repositories below.

```
(App) - https://github.com/Ufocultist/wtv-app - Application repository(Flask/Nginx/MardiaDb microservices)
(Infra) - https://github.com/Ufocultist/tf-infra-wtv - Terraform IAC repository(K8s standard mode)
(CICD) - https://github.com/Ufocultist/wtv-cicd - CI/CD repository(Puthon-CI, EKS-CD)
```
Go to Infra repository first and complete all the steps there.

After completing with Infra repository steps. Do steps below.

Now you are going to Deploy containerized WTV web application using Helm charts to EKS cluster.
1. Clone those repositories on your pc.
2. Go to App repository. Create feature/develop branch from the main branch. Checkout to feature/develop branch.
3. Go to AWS console -> IAM and generate Access keys. Save them to Notepad.
4. Open Github Actions -> Settings -> Secrets and Variables -> Actions.
5. Create two repository keys `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` and copy the values from step 3.
6. Open .github/workflows/dev.yml file and put your values there and save. See values below.

```
  wtv-ci:
    uses: <YOUR_GH_ACCOUNT>/wtv-cicd/.github/workflows/python-ci.yml@feature/develop
    with:
      tag_release: ${{ github.event_name == 'push' && github.ref_name == 'main' }}
      app_name: wtv # app name in AWS Cloud
      app_file: wtv # artifact file name
      registry_type: ecr # ecr - AWS, acr - Azure, gar - Google, Dockerhub - dockerhub
      aws_ecr: wtvapp # Specify ECR repo name you created with Infra.
      aws_region: us-east-1 # Specify your AWS region
      aws_account_id: 111111111111 # Specify your AWS Account ID
      unit_test_enable: true # Flag to enable/disable unit testing job.
      pass_failed_unit_test: '' # Additional unit test flasgs. Leave ASIS
      build_tool: 'pip' # Mandatory
      test_tool: 'pytest' # Mandatory
      add_dep_tools: "ruff pytest build setuptools wheel" # List of additional modules to install
      poetry_checkers: '["mypy", "pylint", "coverage"]' # List of poetry checks
      docker_build: true # Flag to build and publish the image
      snyk_scan: false # Flag to enable Snyk security scanning.
    secrets: inherit

  eks-cd:
    needs: wtv-ci
    uses: <YOUR_GH_ACCOUNT>/wtv-cicd/.github/workflows/eks-cd.yml@feature/develop
    with:
      aws_account_id: 111111111111 # Specify your AWS Account ID.
      cluster_name: wtv-cluster # Specify cluster name you created with Infra.
      nginx: true # Flag to deploy Nginx microservice.
      mariadb: true # Flag to deploy MariaDb microservice.
      wtv: true # Flag to deploy WTV microservice.
      aws_ecr: wtvapp # Specify ECR repo name you created with Infra.
      image_tag: ${{ needs.python-ci.outputs.tag_version }} # Mandatory.
    secrets: inherit
```

7. Commit the changes. Push to git.
8. Go to Actions Tab and click on the running pipeline.
9. Wait for the pipeline to finish. Open deploy job and click on the application deployment link.

## Now you have running WTV application.

Enjoy!
