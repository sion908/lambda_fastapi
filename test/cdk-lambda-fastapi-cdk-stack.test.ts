import { Template } from "aws-cdk-lib/assertions";
import * as cdk from "aws-cdk-lib";
import { LambdaFastapiStack } from "../lib/lambda-fastapi-cdk-stack";

describe("lambdaFastapiStack", () => {
  test("synthesizes the way we expect", () => {
    const app = new cdk.App();

    // Create the ProcessorStack.
    const lambdaFastapiStack = new LambdaFastapiStack(app, "lambdaFastapiStack", {
      stageName: 'dev'
    });

    // Prepare the stack for assertions.
    const template = Template.fromStack(lambdaFastapiStack);

    // Assert it creates the function with the correct properties...
    template.hasResourceProperties("AWS::Lambda::Function", {
      Handler: "main.handler",
      Runtime: "python3.10",
      MemorySize: 256,
      Timeout: 180
    });
    template.hasResourceProperties("AWS::Lambda::Function", {
      Handler: "index.handler",
      Runtime: "nodejs18.x"
    });


    // Creates lambda function main AND for LOG
    template.resourceCountIs("AWS::Lambda::Function", 2);
    template.resourceCountIs("AWS::ApiGateway::RestApi", 1);

  })},
)
