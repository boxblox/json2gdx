import json
import logging
import argparse
from gams import *

def addGamsSet_dc(db, setname, domain, toset, desc):
    i = db.add_set_dc(setname, domain, desc)
    for p in toset:
        i.add_record(p)
        logging.debug('adding to %s GamsSet, entry: %s', setname, p)


def addGamsSet(db, setname, toset, desc):
    i = db.add_set(setname, 1, desc)
    for p in toset:
        i.add_record(p)
        logging.debug('adding to %s GamsSet, entry: %s', setname, p)


def addGamsParameter(db, parametername, domain, toparameter, desc):
    i = db.add_parameter_dc(parametername, domain, desc)
    for k, v in iter(toparameter.items()):
        i.add_record(k).value = v
        logging.debug('adding to %s GamsParameter, key: %s : value: %s', parametername, k, v)


def addGamsScalar(db, parametername, toparameter, desc):
    i = db.add_parameter(parametername, 0, desc)
    i.add_record().value = toparameter
    logging.debug('adding to %s GamsParameter, key: N/A : value: %s', parametername, toparameter)



def fixList2Tuple(json):
    for i in json.keys():
        if json[i]['type'] == 'GamsSet' and json[i]['dimension'] > 1:
            json[i]['elements'] = [tuple(j) for j in json[i]['elements']]

        elif json[i]['type'] == 'GamsParameter' and json[i]['dimension'] > 1:
            json[i]['values']['domain'] = [tuple(j) for j in json[i]['values']['domain']]

        elif json[i]['type'] == 'GamsEquation' and json[i]['dimension'] > 1:
            json[i]['values']['domain'] = [tuple(j) for j in json[i]['values']['domain']]




def json2gdx(j, filename):

    # Need to convert domain lists to tuples
    fixList2Tuple(j)

    # Create GAMS GDX workspace
    ws = GamsWorkspace(working_directory = "./")
    db = ws.add_database()

    # Add all supersets first to enforce proper domain checking
    for i in j.keys():
        if j[i]['type'] == 'GamsSet' and j[i]['domain'] == ['*']:
            addGamsSet(db, setname=i, toset=j[i]['elements'], desc=j[i]['text'])
            logging.debug('adding to %s GamsSet, entry: ', )

    # Add all other sets
    for i in j.keys():
        if j[i]['type'] == 'GamsSet' and not j[i]['domain'] == ['*']:
            addGamsSet_dc(db, setname=i, domain=[db[n] for n in j[i]['domain']], toset=j[i]['elements'], desc=j[i]['text'])

    # Add all scalars
    for i in j.keys():
        if j[i]['type'] == 'GamsParameter' and j[i]['domain'] == []:
            addGamsScalar(db, parametername=i, toparameter=j[i]['values'], desc = j[i]['text'])

    # Add all parameters with nonempty domains
    for i in j.keys():
        if j[i]['type'] == 'GamsParameter' and not j[i]['domain'] == []:
            m = dict(zip(j[i]['values']['domain'], j[i]['values']['data']))
            addGamsParameter(db, parametername=i, domain=[db[n] for n in j[i]['domain']], toparameter=m, desc = j[i]['text'])

#     # GAMS domain check

#     if db.check_domains() == True:
#         logging.debug('*** Export GDX Domain check PASS')
#     else:
#         logging.debug('*** Unexpected domain violation in gamsDatabase object')
#         raise Exception('*** Unexpected domain violation in gamsDatabase object')

    db.export(filename)



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--in', action="store", dest='inFilename', default='out.gdx', type=str)
    parser.add_argument('--out', action="store", dest='outFilename', default='data.gdx', type=str)
    args = parser.parse_args()


    with open(args.inFilename) as infile:
        data = json.load(infile)


    json2gdx(data, args.outFilename)