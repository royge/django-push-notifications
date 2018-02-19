Web Push Sample
===============

Getting Started
---------------

Run local server::

    python -m SimpleHTTPServer 9000

Then goto `http://127.0.0.1:9000` in your browser and copy the device token.

Testing
-------

Goto project root directory then run pushy tester command line tool::

    cd ../../
    ./manage.py testpushy <device-token>
