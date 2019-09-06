==============================================================
BUILDOUT FOR mars DOCUMENTATION
==============================================================

INSTALLING THIS PROJECT WITHOUT MINITAGE
-----------------------------------------
::

    mkdir workdir
    cwd=$PWD
    prefix=$cwd/libs
    mars=$cwd/mars
    git clone ssh://git@github.com/RBINS/mars.buildout.git $mars
    export LDFLAGS="-Wl,-rpath -Wl,$prefix/lib -L$prefix/lib"
    export CFLAGS="-I$prefix/include"
    mkdir tmp
    cd tmp
    sudo apt-get install -y build-essential m4 libtool pkg-config autoconf gettext bzip2 groff man-db automake \\
        libsigc++-2.0-dev git libssl-dev libxml2-dev libxslt1-dev libbz2-dev zlib1g-dev python-setuptools python-dev \\
        libjpeg62-dev libreadline-dev python-pil wv poppler-utils libldap-dev

For ldap support::

    apt-get install -y libldap2-dev libldap-2.4-2 libsasl2-dev


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

in ~/.buildout/default.cfg that egg cache & download cache point to the desired cache directories

Install project

    cd $mars
    $prefix/bin/python bootstrap.py
    bin/buildout -vvvvvNc -c buildout-(dev/prod/devinprod).cfg


CREATE A FIRST PLONESITE OBJECT
---------------------------------
Just run your plone and install mars

PLAYING WITH DATAFS & PROJECT DATABASES
-------------------------------------------
- Upload the latest datafs from production to staging server::

    bin/buildout -vNc <CONFIG>-prod.cfg install upload-datafs

- Get the latest datafs from production to staging server::

    bin/buildout -vNc <CONFIG> install get-datafs


DEVELOP MODE
---------------
To develop your application, run the ``(minitage.)buildout-dev.cfg`` buildout, it extends this one but:
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
--------------------------------------
In ``etc/base.cfg``, we extends directly plone release versions & sources files.


PROJECT SETTINGS
~~~~~~~~~~~~~~~~~~~~~~~~
- Think you have the most important sections of this buildout configuration in etc/mars.cfg
Set the project developement  specific settings there
::

    etc/project/
    |-- mars.cfg       -> your project needs (packages, sources, products)
    |-- sources.cfg          -> externals sources of your project:
    |                           - Sources not packaged as python eggs.
    |                           - Eggs Grabbed from svn, add here your develoment eggs.
    |                           - Links to find distributions.
    |-- patches.cfg          -> patches used on the project
    |-- cluster.cfg          -> define new zope instances here & also their FileSystemStorage if any.
    |-- newsletter.cfg       -> singing & dancing integration (new instance with clockserver, version pinning, fss if any)
    |-- mars-kgs.cfg   -> Generated KGS for your project (minitage's printer or buildout.dumppickledversion)
    `-- versions.cfg         -> minimal version pinning for installing your project


SYSTEM ADMINISTRATORS RELATED FILES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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


BACKENDS
~~~~~~~~~~~
::

    etc/backends/
    |-- etc/backends/zeo.cfg                   -> zeoserver configuration if any
    `-- etc/backends/zodb.cfg                  -> zodb configuration if any


CREATE A NEW SITE
-----------------

add a configuration in sites/mysite.cfg
extend it in buildout-prod.cfg (and, if necessary, in buildout-dev.cfg)
add the process in high-availability.cfg
add the vhost in vhost-mars.conf
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
