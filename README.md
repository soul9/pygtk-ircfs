A pyGTK GUI for go-ircfs and ii
===============================

Work in progress.

Usage
-----
    1, install go and go-ircfs:
      - go: http://golang.org/doc/install.html
      - go-ircfs: once go is installed, do:
<pre>
    goinstall github.com/soul9/go-ircfs
    cd $GOROOT/src/pkg/github.com/soul9/go-ircfs/ && make install
</pre>
    2, start go-ircfs: go-ircfs
    3, mount the filesystem:
      install 9mount, plan9ports or just add an fstab option for the kernel-driver
    4, start the frontend: 
<pre>
    cd src
    ./list.py ~irc

</pre>
