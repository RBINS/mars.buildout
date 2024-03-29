===============================
BUILDOUT FOR mars DOCUMENTATION
===============================

INSTALLING THIS PROJECT
-----------------------

Install a python with datetime patched::

    apt-get install -y apt-build
    ver="2.7.6"
    wget http://python.org/ftp/python/$ver/Python-$ver.tgz
    tar xzvf Python-$ver.tgz
    cd Python-$ver
    patch -Np1 < $mars/patches/py2.7-strftime-pre-1900.patch
    ./configure --prefix=$prefix --enable-ipv6 --with-fpectl --enable-shared --enable-unicode=ucs4 && make && make install
    cd ../..
    rm -rf tmp

::

    mkdir workdir
    cwd=$PWD
    prefix=$cwd/libs
    mars=$cwd/mars
    git clone ssh://git@github.com/RBINS/mars.buildout.git $mars
    mkdir tmp
    cd tmp
    sudo apt-get install -y build-essential m4 libtool pkg-config autoconf gettext bzip2 groff man-db automake \\
        libsigc++-2.0-dev git libssl-dev libxml2-dev libxslt1-dev libbz2-dev zlib1g-dev python-setuptools python-dev \\
        libjpeg62-dev libreadline-dev python-pil wv poppler-utils libldap-dev

For ldap support::

    apt-get install -y libldap2-dev libldap-2.4-2 libsasl2-dev

Install the latest version of Python 2.7 in prefix directory

in ~/.buildout/default.cfg that egg cache & download cache point to the desired cache directories

Install project

    cd $mars
    $prefix/bin/python bootstrap.py
    touch etc/sys/settings.prod.cfg  # and edit it when necessary
    bin/buildout -vvvvvNc -c buildout-(dev/prod/devinprod).cfg

Then read the *Create a new site* section.


DEVELOP MODE
------------
To develop your application, run the ``buildout-dev.cfg`` buildout, it extends this one but:
  * it comes with development tools.
  * it configures the instance to be more verbose (debug mode & verbose security)
  * it has only one instance and not all the hassles from production.


BASE BUILDOUTS WHICH DO ONLY SCHEDULE PARTS FROM THERE & THERE
-------------------------------------------------------------------
Love to know that Minitage support includes xml libs, ldap, dbs; python, dependencies & common eggs cache for things like lxml or Pillow), subversion & much more.
::

    |-- etc/base.cfg               -> The base buildout
    |-- buildout-prod.cfg          -> buildout for production
    |-- buildout-dev.cfg           -> buildout for development


PLONE OFFICIAL BUILDOUTS INTEGRATION
------------------------------------
In ``etc/base.cfg``, we extends directly plone release versions & sources files.


PROJECT SETTINGS
~~~~~~~~~~~~~~~~
- Think you have the most important sections of this buildout configuration in etc/mars.cfg
Set the project developement  specific settings there
::

    etc/project/
    |-- plone.cfg ->
    `-- versions.cfg -> minimal version pinning for installing your project


SYSTEM ADMINISTRATORS RELATED FILES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    etc/init.d/                 -> various init script (eg supervisor)
    etc/logrotate.d/            -> various logrotate configuration files
    etc/sys/
    |-- high-availability.cfg   -> Project production settings like supervision, loadbalancer and so on
    |-- maintenance.cfg         -> Project maintenance settings (crons, logs)
    `-- settings.cfg            -> various settings (crons hours, hosts, installation paths, ports, passwords)

CONFIGURATION TEMPLATES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    etc/templates/
    |-- balancer.conf.template      -> haproxy template.
    |                                  Copy or ln the generated file 'etc/loadbalancing/balancer.conf' to your haproxy installation if any.
    `-- logrotate.conf.template     -> logrotate configuration file template for your Zope logs
    `-- supervisor.initd            -> template for supervisor init script

Setup start at boot
-------------------

    sudo su
    cd /etc/init.d
    ln -s /path/to/buildout/etc/init.d/supervisor.initd supervisor-mars
    update-rc.d supervisor-mars defaults
    exit


BACKENDS
~~~~~~~~~~~
::

    etc/backends/
    |-- etc/backends/zeo.cfg                   -> zeoserver configuration if any


CREATE A NEW SITE
-----------------

add a configuration file in etc/sites
extend it in buildout-prod.cfg (and, if necessary, in buildout-dev.cfg)
add the process in high-availability.cfg
add the vhost in vhost-mars.conf
add the site in scripts/restart-instances.sh
locally test the buildout
run the buildout under production
reload supervisor, start the services
create a ssh tunnel towards site port
change the admin password
create marsadmin user
create a plone site with Plone id
install Mars component
change site title
import Mars/Ldap profile
test ldap connection


THE LIST OF SITES
-----------------

- http://collections.naturalsciences.be/
- http://collections.naturalsciences.be/ssh-anthropology
- http://collections.naturalsciences.be/ssh-entomology
- http://collections.naturalsciences.be/ssh-paleontology/
- http://collections.naturalsciences.be/ssh-geology/
- http://collections.naturalsciences.be/ssh-invertebrates/
- http://collections.naturalsciences.be/ssh-vertebrates/
- http://collections.naturalsciences.be/ssh-projects/
- http://collections.naturalsciences.be/ssh-geology-bibliography/
- http://collections.naturalsciences.be/cpb/


Deactivate LDAP plugins
-----------------------

bin/instance debug
>>> app.Plone.acl_users.plugins._plugins = {key: [value for value in values if value != 'ldap-plugin'] for key, values in app.Plone.acl_users.plugins._plugins.items()}
>>> import transaction
>>> transaction.commit()

Bootstrap
------------
Since 2023, there is a chicken and egg problem on initial bootstrap that needs some eggs to be preinstalled on sitepackages for buildout to run once.
The idea is to install them, then uninstall them because that will also break buildout recipes namespace import scheme when instance launchers are called.
Upon all eggs except the neccessary to make buildout are uninstalled from site-packages, you will need to make buildout run a final time for everything to work.
::

    export TMPDIR=$(pwd)/var/tmp
    /data/libs/python/bin/python -m pip install virtualenv
    /data/libs/python/bin/python2 -m virtualenv --python=python2 --always-copy --system-site-packages venv
    sc='import sys\ntry:\n    sys.setdefaultencoding("utf-8")\nexcept AttributeError:\n    reload(sys);sys.setdefaultencoding("utf-8")\n\n'
    printf "$sc">/data/libs/python/lib/python2.7/site-packages/sitecustomize.py  # AS ROOT is the initial python is owned by root
    . venv/bin/activate
    printf "$sc">venv/lib/python2.7/site-packages/sitecustomize.py
    eggs="zc.buildout zodbpickle plone.recipe.zeoserver setuptools zc.recipe.egg mr.developer"
    pip install --force $(for i in $eggs;do echo "$i==$(echo $(grep -E "^$i\s+=\s+" etc/project/versions.cfg |awk -F= '{print $2}'))";done)
    buildout bootstrap -c "buildout-dev.cfg|buildout-prod.cfg|buildout-devinprod.cfg" --buildout-version=$bver --setuptools-version=$sver
    # make buildout run once completly and without error
    bin/buildout -vvvNc $config
    # then
    pip uninstall -y btrees concurrent mr.developer persistent plone.recipe.zeoserver transaction zc.lockfile zc.recipe.egg zconfig zdaemon zeo zodb zodb3 zodbpickle zope.interface zope.mkzeoinstance zopeundo
    bin/buildout -vvvNc $config



