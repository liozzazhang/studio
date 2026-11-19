# dns-eyes

Personal repository for DNS Eyes, a distributed DNS assurance platform.

Project status: delivered at work; this personal repository is only initialized and contains no code yet.

## DNS Eyes at work

At Cisco I led DNS Eyes, which organizes distributed probes and Infoblox checks into repeatable verification matrices and supports the DNS server lifecycle:

- Check agents cover 20 data centers, supporting NS/ENS, Anycast/BGP, service health, multiple DNS record types and UDP/TCP checks.
- Check/Context/Result, Agent, Target and Runner contracts separate checks, execution, target discovery and orchestration, with YAML verification matrices shared by the CLI and portal.
- Failed-target preflight evidence is retained and results roll up from checks to roles, data centers and a global view; site locks and concurrency semaphores control scheduled work.
- The portal uses FastAPI, SQLite, SAML SSO and centralized module authorization, and supports DNS server build/destroy so verification happens before changes and activation.

## This repository

The work version is an internal Cisco project and its source is not published here. This repository is for personal design work and contained no implementation at review time.
