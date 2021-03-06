#!/usr/bin/env python
from ansible.module_utils.hashivault import hashivault_argspec
from ansible.module_utils.hashivault import hashivault_auth_client
from ansible.module_utils.hashivault import hashivault_init
from ansible.module_utils.hashivault import hashiwrapper

ANSIBLE_METADATA = {'status': ['stableinterface'], 'supported_by': 'community', 'version': '1.1'}
DOCUMENTATION = '''
---
module: hashivault_approle_role_create
version_added: "3.8.0"
short_description: Hashicorp Vault approle create role module
description:
    - Module to create an approle role from Hashicorp Vault.
options:
    url:
        description:
            - url for vault
        default: to environment variable VAULT_ADDR
    ca_cert:
        description:
            - "path to a PEM-encoded CA cert file to use to verify the Vault server TLS certificate"
        default: to environment variable VAULT_CACERT
    ca_path:
        description:
            - "path to a directory of PEM-encoded CA cert files to verify the Vault server TLS certificate : if ca_cert is specified, its value will take precedence"
        default: to environment variable VAULT_CAPATH
    client_cert:
        description:
            - "path to a PEM-encoded client certificate for TLS authentication to the Vault server"
        default: to environment variable VAULT_CLIENT_CERT
    client_key:
        description:
            - "path to an unencrypted PEM-encoded private key matching the client certificate"
        default: to environment variable VAULT_CLIENT_KEY
    verify:
        description:
            - "if set, do not verify presented TLS certificate before communicating with Vault server : setting this variable is not recommended except during testing"
        default: to environment variable VAULT_SKIP_VERIFY
    authtype:
        description:
            - "authentication type to use: token, userpass, github, ldap, approle"
        default: token
    token:
        description:
            - token for vault
        default: to environment variable VAULT_TOKEN
    username:
        description:
            - username to login to vault.
        default: to environment variable VAULT_USER
    password:
        description:
            - password to login to vault.
        default: to environment variable VAULT_PASSWORD
    name:
        description:
            - role name.
    bind_secret_id:
        description:
            - Require secret_id to be presented when logging in using this AppRole.
    bound_cidr_list:
        description:
            - Comma-separated string or list of CIDR blocks.
    policies:
        description:
            - policies for the role.
    secret_id_num_uses:
        description:
            - Number of times any particular SecretID can be used.
    secret_id_ttl:
        description:
            - Duration after which any SecretID expires.
    token_num_uses:
        description:
            - Number of times issued tokens can be used. A value of 0 means unlimited uses.
    token_ttl:
        description:
            - Duration to set as the TTL for issued tokens and at renewal time.
    token_max_ttl:
        description:
            - Duration after which the issued token can no longer be renewed.
    period:
        description:
            - Duration of the token generated.
    enable_local_secret_ids:
        description:
            - If set, the secret IDs generated using this role will be cluster local.
'''
EXAMPLES = '''
---
- hosts: localhost
  tasks:
    - hashivault_approle_role_create:
        name: 'ashley'
'''


def main():
    argspec = hashivault_argspec()
    argspec['name'] = dict(required=True, type='str')
    argspec['bind_secret_id'] = dict(required=False, type='bool')
    argspec['bound_cidr_list'] = dict(required=False, type='list')
    argspec['policies'] = dict(required=True, type='list')
    argspec['secret_id_num_uses'] = dict(required=False, type='str')
    argspec['secret_id_ttl'] = dict(required=False, type='str')
    argspec['token_num_uses'] = dict(required=False, type='int')
    argspec['token_ttl'] = dict(required=False, type='str')
    argspec['token_max_ttl'] = dict(required=False, type='str')
    argspec['period'] = dict(required=False, type='str')
    argspec['enable_local_secret_ids'] = dict(required=False, type='bool')
    module = hashivault_init(argspec)
    result = hashivault_approle_role_create(module.params)
    if result.get('failed'):
        module.fail_json(**result)
    else:
        module.exit_json(**result)


@hashiwrapper
def hashivault_approle_role_create(params):
    ARGS = [
        'bind_secret_id',
        'bound_cidr_list',
        'secret_id_num_uses',
        'secret_id_ttl',
        'token_num_uses',
        'token_ttl',
        'token_max_ttl',
        'period',
        'enable_local_secret_ids',
    ]
    name = params.get('name')
    policies = params.get('policies')
    client = hashivault_auth_client(params)
    kwargs = {
        'policies': policies,
    }
    for arg in ARGS:
        value = params.get(arg)
        if value is not None:
            kwargs[arg] = value
    client.create_role(name, **kwargs)
    return {'changed': True}


if __name__ == '__main__':
    main()
