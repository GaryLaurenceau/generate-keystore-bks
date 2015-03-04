#!/usr/bin/env python

import argparse
import sys
from os import path
import subprocess
import getpass

OPENSSL_CMD='openssl x509 -inform PEM -subject_hash -noout -in %s'


def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Generate keystore BKS file for Android\
                                                to handle self signed HTTPS connection.')
    parser.version = 1.0

    parser.add_argument('-bc', '--bc-jar-location', nargs=1, dest='jar_file', required=True,
                        help='set bouncy castle jar file location')
    parser.add_argument('-ca', '--cacert', nargs=1, dest='cacert_file', required=True,
                        help='set CA cert file location')
    parser.add_argument('-n', '--bks-name', nargs=1, dest='name', default=['key_store.bks'],
                        help='set the name of the bks file generated')
    parser.add_argument('-p', '--password', nargs=1, dest='password', default=[None],
                        help='set password')
    return parser


def get_openssl_result(file):
    result_code = subprocess.check_output(
        ['openssl', 'x509', '-inform', 'PEM', '-subject_hash', '-noout', '-in', file],
    )
    return result_code

def create_keystore(jar_file, cacert_file, code, name, password):
    print password
    while password is None:
        password = getpass.getpass(prompt="Password")
        if password is None or len(password) < 6:
            print "Password should contain at least 6 characters"
            password = None
            continue

    subprocess.call(
        ['keytool', '-import', '-v', '-trustcacerts', '-alias', code, '-file', cacert_file,
      '-keystore', name,
      '-storetype', 'BKS',
      '-providerclass', 'org.bouncycastle.jce.provider.BouncyCastleProvider',
      '-providerpath', jar_file,
      '-storepass', password]
    )

def main():
    arg_parser = setup_arg_parser()
    arg = arg_parser.parse_args()

    jar_file = arg.jar_file[0]
    cacert_file = arg.cacert_file[0]
    name = arg.name[0]
    password = arg.password[0]

    if path.isfile(jar_file) is False:
        print jar_file, "is not a file."
        sys.exit()
    elif path.isfile(cacert_file) is False:
        print cacert_file, "is not a file."
        sys.exit()

    print ("Generating alias...")
    result_code = get_openssl_result(cacert_file)
    result_code = result_code.strip()
    print ("Adding %s with alias %s to %s." % (jar_file, result_code, name))
    create_keystore(jar_file, cacert_file, result_code, name, password)
    print "%s has been created" % name


if __name__ == "__main__":
    main()

