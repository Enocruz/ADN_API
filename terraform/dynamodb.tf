resource "aws_dynamodb_table" "dna-stats" {
  name           = "DnaStats"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "StatName"


  attribute {
    name = "StatName"
    type = "S"
  }


  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}

resource "aws_dynamodb_table" "dna-storage" {
  name           = "DnaStorage"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "DNA"


  attribute {
    name = "DNA"
    type = "S"
  }


  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}

resource "aws_dynamodb_table_item" "no-mutation-stat" {
  table_name = aws_dynamodb_table.dna-stats.name
  hash_key   = aws_dynamodb_table.dna-stats.hash_key

  item = <<ITEM
{
  "StatName": {"S": "count_no_mutation"},
  "CountOcurrences": {"N": "0"}
}
ITEM
}

resource "aws_dynamodb_table_item" "mutation-stat" {
  table_name = aws_dynamodb_table.dna-stats.name
  hash_key   = aws_dynamodb_table.dna-stats.hash_key

  item = <<ITEM
{
  "StatName": {"S": "count_mutations"},
  "CountOcurrences": {"N": "0"}
}
ITEM
}
