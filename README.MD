CL status: [![Build Status](https://travis-ci.org/Igor-ua/XR_Server.svg?branch=master)](https://travis-ci.org/Igor-ua/XR_Server)

**Additional content (mod) for the XR Server.**

This mod consists from the three main parts:
- **Python-core**: Main ingame logic and client's api.
- **Spring-core**: Java Spring module with an API to manage statistics.
- **db-core**: Contains H2 database for a spring-core module.
_*note: requires standard files of the XR Server._

**Python** (module: requests) <--> **Spring** (Jackson) communication is going through the http/json.

**Spring API** (file: api-map.info):

Public API:

`"/"
"/world"`

Secure (private) API:
`"/stats"
"/stats/"
"/stats/get/{uid}"
"/stats/get/name/{name}"
"/stats/get/top/..."
"/stats/server"
"/stats/server/"
"/stats/server/player/put"
"/stats/server/players/put"
"/stats/server/map-stats/post"`

Online copy of this server is available here: `http://94.177.253.129:8586` (VPS/London)