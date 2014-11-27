==========================
Django Content Interactions
==========================

Common User-Content Interactions for Django>=1.6.1

Like, Mark as Favorite, Rate, Share, Recommend, Denounce...

Changelog
=========

0.2.2
-----
+ Fix in mixins' edge creation methods (when an edge type allows only one edge per objects pair, use edge_change instead of edge_add).

0.2.1
-----
+ Added missing denounce url.

0.2.0
-----
+ Reimplemented jQuery classes in order to pass the params directly in the constructor of the instance.

0.1.0
-----

PENDING...

Notes
-----

PENDING...

Usage
-----

1. Run ``python setup.py install`` to install.

2. Modify your Django settings to use ``content_interactions``: