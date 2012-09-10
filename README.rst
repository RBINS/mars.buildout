==============================================================
BUILDOUT FOR mars DOCUMENTATION
==============================================================

INSTALLING THIS PROJECT VITHOUT MINITAGE
-----------------------------------------
::

    source /minitage/bin/activate
    git clone ssh://git@github.com/RBINS/mars.buildout.git mars
    cd mars
    python bootstrap.py -dc buildout-(dev/prod).cfg
    bin/buildout -vvvvvNc -dc buildout-(dev/prod).cfg

INSTALLING THIS PROJECT VITH MINITAGE
--------------------------------------
ALWAYS USE THE MINITAGE ENVIRONMENT FILE INSIDE A MINITAGE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before doing anything in your project just after being installed, just source the environment file in your current shell::

    source $MT/zope/mars/sys/share/minitage/minitage.env # env file is generated with $MT/bin/paster create -t minitage.instances.env mars

THE MINITAGE DANCE
~~~~~~~~~~~~~~~~~~~~~~~~
::

    export MT=/minitage
    virtualenv --no-site-packages --distribute $MT
    source /minitage/bin/activate
    easy_install -U minitage.core minitage.paste
    git clone ssh://git@github.com/RBINS/mars.minilay.git $MT/minilays/mars
    minimerge -v mars
    #minimerge -v mars-prod
    source $MT/zope/mars/sys/share/minitage/minitage.env
    cd $INS #enjoy !


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


PRODUCTION MODE
---------------
To make your application safe for production, run the ``(minitage.)buildout-prod.cfg`` buildout'.
It extends this one with additionnal crontabs and backup scripts and some additionnal instances creation.


BASE BUILDOUTS WHICH DO ONLY SCHEDULE PARTS FROM THERE & THERE
-------------------------------------------------------------------
Love to know that Minitage support includes xml libs, ldap, dbs; python, dependencies & common eggs cache for things like lxml or Pillow), subversion & much more.
::

    |-- etc/base.cfg               -> The base buildout
    |-- buildout-prod.cfg          -> buildout for production
    |-- buildout-dev.cfg           -> buildout for development
    |-- etc/minitage/minitage.cfg  -> some buildout tweaks to run in the best of the world with minitage
    |-- minitage.buildout-prod.cfg -> buildout for production  with minitage support
    |-- minitage.buildout-dev.cfg  -> buildout for development with minitage support


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


REVERSE PROXY
--------------
We generate two virtualhosts for a cliassical apache setup, mostly ready but feel free to copy/adapt.
::
    etc/apache/
    |-- 100-mars.reverseproxy.conf     -> a vhost for ruse with a standalone plone (even with haproxy in front of.)
    `-- apache.cfg
    etc/templates/apache/
    |-- 100-mars.reverseproxy.conf.in  -> Template for a vhost for ruse with a standalone plone (even with haproxy in front of.)

In settings.cfg you have now some settings for declaring which host is your reverse proxy backend & the vhost mounting:
    * hosts:zope-front / ports:zope-front                              -> zope front backend
    * reverseproxy:host / reverseproxy:port / reverseproxy:mount-point -> host / port / mountpoint on the reverse proxy)

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
    |-- etc/backends/relstorage.cfg            -> relstorage configuration if any
    |-- etc/backends/zeo.cfg                   -> zeoserver configuration if any
    `-- etc/backends/zodb.cfg                  -> zodb configuration if any


KGS FILE
----------
We provide a part to generate the etc/mars-kgs.cfg file.
This will allow you to freeze software versions known to work with your project and make reproducible environment.
This file will be generated the first time that you run buildout.
To un it, just run bin/buildout -vvvvvvc <CONFIG_FILE> install kgs
Then sync the content of the kgs file with ``etc/project/versions.cfg``.

NOTES ABOUT RELSTORAGE SUPPORT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We use the ZODB as an egg which is patched during installation, please see ``etc/project/patches.cfg``


OS SPECIFIC SYSTEM INSTALLERS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Thos popular tools around zope/plone dev (not supported, just here for your conveniance, READ BEFORE USING THEM)
And you'd  better have to learn how to bootstrap some minitage environment out there, funny and more secure & reproductible!
::

    |-- etc/os
        |-- debian.sh       -> debian specific
        |-- opensuse-dev.sh -> opensuse/dev specific
        |-- opensuse.sh     -> suse specific
        |-- osx.sh          -> osx specific
        `-- ubuntu.sh       -> ubuntu specific


CONTINEOUS INTEGRATION
~~~~~~~~~~~~~~~~~~~~~~~~~
Here are the files needed for our hudson integration.

For hudson we provide some shell helpers more or less generated to run 'a build':

    - an helper which set some variables in the current environement for others helpers
    - an helper which update the project
    - an helper which update the associated sources grabbed via mr.developer
    - an helper which run all the tests

This is described in details on the related configuration files you will find in the layout below.
::

    |-- etc/hudson/
    |   `-- mars
    |       |-- build
    |           |-- build.sh               -> the project build helper
    |           |-- test.sh                -> the project test executor helper (launch all tests needed)
    |           |-- update_mrdeveloper.sh  -> update sources grabbed via mrdeveloper
    |           `-- update_project.sh      -> update this layout
    |
    |-- etc/templates/hudson/
        `-- mars
            |-- build
            |   `-- activate_env.sh.in   -> buildout template to generate etc/hudson/mars/build/activate.env.sh
            `-- config.xml.in            -> buildout template to generate etc/hudson/mars/config.xml (hudson job/build file)

A word about minitage.paste instances
--------------------------------------
You are maybe wondering why this big buildout do not have out of the box those fancy monitoring, load-balancing or speedy databases support.
#
For the author, System programs that are not well integrated via buildout and most of all not written in python don't really have to be deployed via that buildout.
And most of all, you ll surelly have head aches to make those init-scripts or rotation logs configurations right.
Because the recipe which do them don't support it or other problems more or less spiritual.
#
Keep in mind that in Unix, one thing must do one purpose, and do it well. And many sysadmins don't want to run a buildout
to generate a configuration file or build their loadbalancer, They want to edit in place, at most fetch the configuration file from somewhere and adapt,that's all.
#
Nevertheless, as usual, they are exceptions:
     - supervisord which is well integrated. So supervisor is deployed along in the production buildout if any.
     - We generate through buildout a haproxy configuration file or hudson related stuff
#
That's because we support that throught 'minitage.paste.instances'. Those are templates which create some instance of some program
inside a subdirectory which is:
   - sys/ inside a minitage project
   - ADirectoryOfYourChoice/ if your are not using minitage
#
This significate that you can install a lot of things along with your project with:
   - minitage/bin/easy_install -U minitage.paste(.extras) (or get it via buildout)
   - paster create -t <TEMPLATE_NAME> projectname_OR_subdirectoryName inside_minitage=y/n
     Where TEMPLATE_NAME can be (run paster create --list-templates|grep minitage.instances to get an up2date version):
#
     * minitage.instances.apache:          Template for creating an apache instance
     * minitage.instances.env:             Template for creating a file to source to get the needed environnment variables for playing in the shell or for other templates
     * minitage.instances.mysql:           Template for creating a postgresql instance
     * minitage.instances.nginx:           Template for creating a nginx instance
     * minitage.instances.paste-initd:     Template for creating init script for paster serve
     * minitage.instances.postgresql:      Template for creating a postgresql instance
     * minitage.instances.varnish:         Template for creating a varnish instance
     * minitage.instances.varnish2:        Template for creating a varnish2 instance
#
     The minitage.paste package as the following extras:
#
     * minitage.instances.openldap:      Template for creating an openldap instance
     * minitage.instances.tomcat:        Template for creating a tomcat instance
     * minitage.instances.cas:           Template for creating a Jisag CAS instance
     * minitage.instances.hudson:        Template for creating an hudson instance
#
Note that if you are using minitage, you ll have better to add dependencies inside your minibuild and run minimerge to build them prior to run the paster command
#
For example, to add a postgresql instance to your project, you will have to issue those steps:
    * $EDITOR minitage/minilays/mars_minilay/mars -> add postgresql-8.4 to the dependencies list
    * minimerge -v  mars install what was not, and surely at least postgresql-8.4
    * minitage/bin/paster create -t minitage.instance.postgresql mars
    * Then to start the postgres : zope/mars/sys/etc/init.d/mars_postgresql restart


.. vim:set ft=rst:
