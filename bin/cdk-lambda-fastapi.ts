#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { LambdaFastapiStack } from "../lib/lambda-fastapi-cdk-stack";
import { ENVS } from "../lib/env";

const app = new cdk.App();

// 環境の指定 -c environment=('dev'||'prod')
const argContext = 'environment';
const stageName = app.node.tryGetContext(argContext);

if(!Object.values(ENVS).includes(stageName)){
  throw new Error(
    `環境が指定されていないまたは、適当な環境が指定されていません -> env_name:${stageName}`
  );
}

const lambdaFastapiStack = new LambdaFastapiStack(app, `LambdaFastapiStack-${stageName}`,{
  stageName: stageName,
});

cdk.Tags.of(lambdaFastapiStack).add("Project", "lambda-fastapi")
cdk.Tags.of(lambdaFastapiStack).add("Project_env", `lambda-fastapi-${stageName}`)
