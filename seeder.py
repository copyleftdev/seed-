#!/usr/bin/env python

import random
import os
from faker import Factory
import argparse

fake = Factory.create()


def gen_doc_lst(root_folder):
    """recusivly generate a list of file path with provided root folder"""
    filelst = []
    for(dirpath, _, files) in os.walk(root_folder):
        for filename in files:
            filepath = os.path.join(dirpath, filename)
            filelst.append(filepath)
    return filelst


def seed_docs(doc_count, root_folder, **kwargs):
    """Radomly seed document with  PII data"""
    piiProvider = [fake.credit_card_number(), fake.ssn(), fake.phone_number()]
    docslst = random.sample(gen_doc_lst(root_folder), doc_count)
    print "Starting PII seed process...."
    for each_doc in docslst:
        with open(each_doc, 'a+') as fn:
            fn.write(' PII VECTOR ( {} )'.format(random.choice(piiProvider)))
            with open('piiseedmap.txt', 'a+') as logfn:
                logfn.write(each_doc + '\n')
                print "Seeding {} with PII".format(each_doc)

    print "Document seeding is complete {} files seeded.".format(doc_count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wiki PII seeder")
    parser.set_defaults(method=seed_docs)
    parser.add_argument('doc_count', type=int, help="seed count.")
    parser.add_argument('root_folder', type=str, help="root folder")

    args = parser.parse_args()
    args.method(**vars(args))
