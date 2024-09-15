import boto3
import json

def get_secret():
    secret_name = "openai_api_key"
    region_name = "us-east-2"

    # Criar um cliente do Secrets Manager usando as credenciais padrão
    client = boto3.client(service_name='secretsmanager', region_name=region_name)

    # Recuperar o valor do segredo
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    # Se o segredo estiver em formato JSON
    secret = get_secret_value_response['SecretString']
    secret_data = json.loads(secret)
    return secret_data['openai_key']
