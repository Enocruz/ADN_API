terraform {
  backend "s3" {
    bucket = "terraform-cruz-test"
    key    = "state"
    region = "us-west-2"
  }
}

provider "aws" {
  region = "us-west-2"
}

