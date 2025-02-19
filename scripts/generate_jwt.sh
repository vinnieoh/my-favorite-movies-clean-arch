#!/bin/bash

# Gera um token JWT aleatório usando OpenSSL
generate_token() {
  local token=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9-_')
  echo "TOKEN JWT: $token"
}

# Chama a função para gerar o token
generate_token
