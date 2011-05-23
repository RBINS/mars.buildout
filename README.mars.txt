* A project has been created in /tmp/tmpQtxeN8.

* A minilay has been installed in /tmp/tmpQtxeN8/minilays/mars.
* It contains those minilbuilds:
	- mars-light
	- mars-buildbot
	- mars-prod
	- mars
	- mars-prod-light 

* Think to finish the versionning stuff and put this minilay and the projet under revision control.
* The project must be archived here 'https://subversion.makina-corpus.net/scrumpy/mars/buildout' using 'svn' or change the minibuild src_uri/scm_type.
* Install your project running: 
		minimerge -v mars
* You can additionnaly create related databases or configuration or other stuff using minitage instances  (http://minitage.org/paster/instances/index.html)
* Available instances are: 
	- minitage.instances.env (Template for creating a file to source to get the needed environment variables for playing in the shell or for other templates)
	- minitage.instances.varnish2 (Template for creating a varnish2 instance)
	- minitage.instances.varnish (Template for creating a varnish instance)
	- minitage.instances.nginx (Template for creating a nginx instance)
	- minitage.instances.mysql (Template for creating a postgresql instance)
	- minitage.instances.apache (Template for creating an apache instance)
	- minitage.instances.paste-initd (Template for creating init script for paster serve)
	- minitage.instances.postgresql (Template for creating a postgresql instance)
* Some extra instances are contained inside the'minitage.paste.extras package', install it as a classical egg.
* Run an instance with: 
 	paster create -t minitage.instances.PROFIL project

