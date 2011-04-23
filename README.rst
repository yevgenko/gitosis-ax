============================================================
 ``gitosis-ax`` -- software for hosting ``git`` repositories
============================================================

        Manage ``git`` repositories, provide access to them over SSH,
        with tight access control and not needing shell accounts.

.. note::

        Documentation is still lacking, and non-default configurations
        (e.g. config file, repositories, installing in a location that
        is not in ``PATH``) basically have not been tested at all.
        Basic usage should be very reliable -- the project has been
        hosting itself for a long time. Any help is welcome.

``gitosis-ax`` aims to make hosting ``git`` repos easier and safer. It
manages multiple repositories under one user account, using SSH keys
to identify users. End users do not need shell accounts on the server,
they will talk to one shared account that will not let them run
arbitrary commands.

``gitosis-ax`` is licensed under the GPL, see the file ``COPYING`` for
more information.

You can get ``gitosis-ax`` via ``git`` by saying::

    git clone git://github.com/albix/gitosis-ax.git

And install it via::

    python setup.py install

Though you may want to use e.g. ``--prefix=``. For Debian/Ubuntu
users, the source is debianized.


Setting up
==========

First, we will create the user that will own the repositories. This is
usually called ``git``, but any name will work, and you can have more
than one per system if you really want to. The user does not need a
password, but does need a valid shell (otherwise, SSH will refuse to
work). Don't use an existing account unless you know what you're
doing.

I usually store ``git`` repositories in the subtree
``/srv/example.com/git`` (replace ``example.com`` with your own
domain). You may choose another location. Adjust to suit and run::

        sudo adduser \
                --system \
                --shell /bin/sh \
                --gecos 'git version control' \
                --group \
                --disabled-password \
                --home /srv/example.com/git \
                git

This command is known to work in Debian and Ubuntu. Your mileage may
vary.

You will need an SSH public key to continue. If you don't have one,
you need to generate one. See the man page for ``ssh-keygen``, and you
may also be interested in ``ssh-agent``. Create it on your personal
computer, and protect the *private* key well -- that includes not
transferring it over the network.

Next, we need to set things up for this newly-created user. The
following command will create a ``~/repositories`` that will hold the
``git`` repositories, a ``~/.gitosis.conf`` that will be a symlink to
the actual configuration file, and it will add the SSH public key to
``~/.ssh/authorized_keys`` with a ``command=`` option that restricts
it to running ``gitosis-serve``. Run::

        sudo -H -u git gitosis-init <FILENAME.pub
        # (or just copy-paste the public key when prompted)

then just ``git clone git@SERVER:gitosis-admin.git``, and you get a
repository with SSH keys as ``keys/USER.pub`` and a ``gitosis.conf``
where you can configure who has access to what.

.. warning::

        For now, ``gitosis-ax`` uses the ``HOME`` environment variable to
        locate where to write its files. If you use ``sudo -u``
        without ``-H``, ``sudo`` will leave the old value of ``HOME``
        in place, and this will cause trouble. There will be a
        workaround for that later on, but for now, always remember to
        use ``-H`` if you're sudoing to the account.

You should always edit the configuration file via ``git``. The file
symlinked to ``~/.gitosis.conf`` on the server will be overwritten
when pushing changes to the ``gitosis-admin.git`` repository.

Edit the settings as you wish, commit and push. That's pretty much it!
Once you push, ``gitosis-ax`` will immediately make your changes take
effect on the server.


Managing it
===========

To add new users:

- add a ``keys/USER.pub`` file
- authorize them to read/write repositories as needed (or just
  authorize the group ``@all``)

To create new repositories, just authorize writing to them and
push. It's that simple! For example: let's assume your username is
``jdoe`` and you want to create a repository ``myproject``.
In your clone of ``gitosis-admin``, edit ``gitosis.conf`` and add::

        [group myteam]
        members = jdoe
        writable = myproject

Commit that change and push. Then create the initial commit and push
it::

        mkdir myproject
        cd mypyroject
        git init
        git remote add myserver git@MYSERVER:myproject.git
        # do some work, git add and commit files
        git push myserver master:refs/heads/master

That's it. If you now add others to ``members``, they can use that
repository too.


Example configuration
=====================

.. include:: example.conf
   :literal:


Using git-daemon
================

Anonymous read-only access to ``git`` repositories is provided by
``git-daemon``, which is distributed as part of ``git``. But
``gitosis`` will still help you manage it: setting ``daemon = yes`` in
your ``gitosis.conf``, either globally in ``[gitosis]`` or
per-repository under ``[repo REPOSITORYNAME]``, makes ``gitosis``
create the ``git-daemon-export-ok`` files in those repository, thus
telling ``git-daemon`` that publishing those repositories is ok.


Contact
=======

You can email the author at ``cal@albix.de``


