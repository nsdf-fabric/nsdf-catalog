# NSDF-Catalog

<img src="https://nationalsciencedatafabric.org/assets/images/logo.png" width="64" valign="middle" alt="NSDF-catalog" width="200"/>  

NSDF-Catalog is a **lightweight indexing service** with minimal metadata that complements existing domain-specific and rich-metadata collections. 

NSDF-Catalog is part of the [National Science Data Fabric](https://nationalsciencedatafabric.org) (NSDF) initiative, funded by  the [National Science Fundation](https://www.nsf.gov/) (NSF).

NSDF-Catalog is designed to facilitate multiple related objectives within a flexible microservice to: (i) coordinate data movements and replication of data from origin repositories within the NSDF federation (ii) build an inventory of existing scientific data to inform the design of next-generation cyberinfrastructure; and (iii) provide a suite of tools for discovery of datasets for cross-disciplinary research. 

NSDF-Catalog **indexes scientific data** at a fine-granularity at the file or object level to inform data distribution strategies and to improve the experience for users from the consumer perspective, with the goal of allowing end-toend dataflow optimizations. Index Terms—national science data fabric, scientific data, cloud, high performance computing


## Quickstart

The fastest way to get started is to use docker-compose:

    $ docker-compose up

This spawns various containerized microserves which together form a NSDF-compatible indexing service.
An graphical overview is documented in (./docs/figures/overview.drawio).

It should now be possible to access a web frontend at:

    http://localhost:80/

And a REST API at:

    http://localhost:80/api/v1


## Production Deployment

It is highly recommended to run NSDF-catalog instances through a domain name to allow for HTTPs.

 * (A domain to allow HTTPs via LetsEncrypt/Certbot)
 * A publically available IP
 * A machine (physical or virtual) to spawn multiple containers


# Community

NSDF-catalog is an open source project.  Questions, discussion, and
contributions are welcome. Contributions can be anything from new
packages to bugfixes, documentation, or even new core features.

Resources:

* **Slack workspace**: [nsdf-workspace](https://nsdf-workspace.slack.com/).
* **Github Discussions**: [issues](https://github.com/nsdf-fabric/nsdf-catalog/issues): not just for discussions, also Q&A.
* **Mailing list**: [https://groups.google.com/g/nsdf](https://groups.google.com/g/nsdf) -   nsdf@googlegroups.com
* **Twitter**: [@FabricNsdf](https://twitter.com/FabricNsdf). 

Contributing
------------
Contributing to NSDF-catalog is easy.   Just send us a [pull request](https://help.github.com/articles/using-pull-requests/). 

When you send your request, make ``develop`` the destination branch on the [NSDF-catalog-repository](https://github.com/nsdf-fabric/nsdf-catalog).

NSDF-catalog's`develop` branch has the latest contributions. Pull requests
should target `develop`, and users who want the latest package versions,
features, etc. can use `develop`.

# Authors

NSDF-catalog was created by the [NSDF team](https://nationalsciencedatafabric.org/contributors.html) . To reach out email us at [info@nationalsciencedatafabric.org](email:info@nationalsciencedatafabric.org)

# Citing NSDF-Catalog

If you are referencing NSDF-catalog in a publication, please cite the following paper:

-  Jakob Luettgau, Giorgio Scorzelli, Valerio Pascucci, Glenn Tarcea, Christine R. Kirkpatrick and Michela Taufer. *NSDF-Catalog: Lightweight Indexing Service  for Democratizing Data Delivering*. UCC Main Conference.

On GitHub, you can copy this citation in APA or BibTeX format via the "Cite this repository" button.  

# License

NSDF-Catalog is distributed under the terms of the BSD-3-Clause license.
All new contributions must be made under the BSD-3-Clause license.

See [LICENSE](https://github.com/nsdf-fabric/nsdf-catalog/blob/main/LICENSE) for details.

SPDX-License-Identifier: (BSD-3-Clause)


