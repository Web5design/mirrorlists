from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from ConfigParser import SafeConfigParser
import pygeoip
from incf.countryutils import transformations
import random

app = Flask(__name__)

config = SafeConfigParser(allow_no_value=True)
#config.read('eucalyptus_mirrors.conf')

def get_continent(host_ip):
    geoip = pygeoip.GeoIP(config.get('Config', 'GeoIPData'))

    country = geoip.country_code_by_addr(host_ip)
    if country == '':
        return 'North America'
    else:
        return transformations.cca_to_ctn(country)

def get_enterprise():
    mirrors = []

    for key,value in config.items("Enterprise"):
        mirrors.append(key)

    return mirrors

def build_list_from_config(continent, mirrors):
    current_mirrors = []

    for key,value in config.items(continent):
        current_mirrors.append(key)

    random.shuffle(current_mirrors)

    for mirror in current_mirrors:
        mirrors.append(mirror)

    return mirrors

def get_mirrors(continent):
    mirrors = [] 

    if continent == 'North America':
        for cur_continent in ['North America', 'Europe', 'South America', 'Asia', 'Africa', 'Oceania', 'Antartica']:
            mirrors = build_list_from_config(cur_continent, mirrors)
    elif continent == 'Europe':
        for cur_continent in ['Europe', 'North America', 'South America', 'Asia', 'Africa', 'Oceania', 'Antartica']:
            mirrors = build_list_from_config(cur_continent, mirrors)
    elif continent == 'Asia':
        for cur_continent in ['Asia', 'Europe', 'North America', 'South America', 'Africa', 'Oceania', 'Antartica']:
            mirrors = build_list_from_config(cur_continent, mirrors)
    elif continent == 'South America':
        for cur_continent in ['South America', 'North America', 'Europe', 'Asia', 'Africa', 'Oceania', 'Antartica']:
            mirrors = build_list_from_config(cur_continent, mirrors)
    elif continent == 'Africa':
        for cur_continent in ['Africa', 'Europe', 'North America', 'South America', 'Asia', 'Oceania', 'Antartica']:
            mirrors = build_list_from_config(cur_continent, mirrors)
    elif continent == 'Oceania':
        for cur_continent in ['Oceania', 'North America', 'Asia', 'Europe', 'South America', 'Africa', 'Antartica']:
            mirrors = build_list_from_config(cur_continent, mirrors)
    else:
        for cur_continent in ['Antartica', 'Oceania', 'Africa', 'South America', 'Asia', 'Europe', 'North America']:
            mirrors = build_list_from_config(cur_continent, mirrors)

    return mirrors

@app.route('/mirrors', methods=['POST', 'PUT', 'GET'])
def request_mirrorlist():
    config.read('eucalyptus_mirrors.conf')

    protocol = "http://"
    release = request.values.get('release', '6')
    arch = request.values.get('arch', 'x86_64')
    distro = request.values.get('distro', 'centos')
    version = request.values.get('version', config.get('Config', 'eucalyptus-latest'))
    product = request.values.get('product', 'eucalyptus')

    if product == "enterprise":
        mirrors = get_enterprise()
        protocol = "https://"
    else:
        continent = get_continent(str(request.remote_addr))
        mirrors = get_mirrors(continent)

    mirrorlist = render_template('mirrorlist', mirrors=mirrors, release=release, arch=arch, distro=distro, version=version, product=product, protocol=protocol)

    return Response(mirrorlist, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
