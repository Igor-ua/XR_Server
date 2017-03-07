[![Build Status](https://travis-ci.org/Igor-ua/XR_Server.svg?branch=master)](https://travis-ci.org/Igor-ua/XR_Server)

**Additional content (mod) for the XR Server.**

This mod consists from the three main parts:</br>
- **Python-core**: Main ingame logic and client's api.</br>
- **Spring-core**: Java Spring module with an API to manage statistics.</br>
- **db-core**: Contains H2 database for a spring-core module.</br>
_*note: requires standard files of the XR Server._

**Python** (module: `requests`) <--> **Spring** (`Jackson`) communication is going through the http/json.

**Spring API:**</br>
`spring-core/src/main/java/com/newerth/api/api-map.info`</br>
- public:</br>
`"/"`</br>
`"/world"`</br>
- secure (private):</br>
`"/stats"`</br>
`"/stats/"`</br>
`"/stats/get/{uid}"`</br>
`"/stats/get/name/{name}"`</br>
`"/stats/get/top/..."`</br>
`"/stats/server"`</br>
`"/stats/server/"`</br>
`"/stats/server/player/put"`</br>
`"/stats/server/players/put"`</br>
`"/stats/server/map-stats/post"`</br>

Server configs:</br>
`python-core/server/configs`</br>

Required files for clients:</br>
`python-core/client/savage5.s2z`</br></br>


Online copy of this server is available here: `http://94.177.253.129:8586` _(vps/London)_