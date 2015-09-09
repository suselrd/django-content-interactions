==========================
Django Content Interactions
==========================

Common User-Content Interactions for Django>=1.6.1

Like, Mark as Favorite, Rate, Share, Denounce...

Changelog
=========

0.4.2
-----
+ Fixed stats mixin.

0.4.1
-----
+ Renamed stats application, to be more specific.

0.4.0
-----
+ Added Stats functionality.
+ Unified Share and Recommend into only one possible interaction: Share (with an optional comment)

0.3.1
-----
+ Fix bug in mixins.

0.3.0
-----
+ Upgrading to django-social-graph 0.2.0

0.2.4
-----
+ Improving denounce flow.

0.2.3
-----
+ Templates tags expecting objects can now accept a tuple (content_type_pk, object_pk)

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