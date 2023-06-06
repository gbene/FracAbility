******************************************
Introduction to fracture network analysis
******************************************

Fracture networks
===================

Topology and node classification
---------------------------------

Statistics and parametrization
-------------------------------

Length
^^^^^^^



Reliability engineering is a field of study that deals with the estimation, prevention, and management of failures by
combining statistics, risk analysis, and physics. By understanding how failures may occur or have occurred, we are able
to better predict the lifespan of a product or system, allowing us to manage its lifecycle and the risks associated with
its failure. All engineering systems, components, and structures will eventually fail, and knowing how and when that
failure will occur is of great interest to the owners and operators of those systems. Due to the similarities between
the lifecycle of engineering systems and the lifecycle of humans, the field of study known as
`survival analysis <https://en.wikipedia.org/wiki/Survival_analysis>`_ has many concepts that are used in reliability
engineering.

Everyone is acutely aware of the importance of reliability, particularly when something doesn't work at a time we expect
it to. Whether it be your car not starting, your television failing, or the chance of being delayed on the runway
because your aircraft's airconditioning unit just stopped working, we know that system failure is something we all want
to avoid. When it can't be avoided, we at least want to know when it is likely to occur so we can conduct preventative
maintenance before the need for corrective maintenance arises. Reliability engineering is most frequently used for
systems which are of critical safety importance (such as in the nuclear industry), or in systems which are numerous
(such as vehicles or electronics) where the cost of fleetwide reliability problems can quickly become very expensive.

Much of reliability engineering involves the analysis of data (such as time to failure data), to uncover the patterns in
how failures occur. Once we understand how things are failing, we can use those patterns to forecast how the failures
will occur throughout the lifetime of a population of items, or the lifetime of one or more repairable items.
It is the data analysis part of reliability engineering that this Python library is designed to help with.

Further reading is available on `Wikipedia <https://en.wikipedia.org/wiki/Reliability_engineering/>`_ and in many
`other reliability resources <https://reliability.readthedocs.io/en/latest/Recommended%20resources.html>`_.