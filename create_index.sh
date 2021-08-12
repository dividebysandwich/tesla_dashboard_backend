#!/bin/bash
curl -XDELETE elasticsearch:9200/tesla -H'Content-Type: application/json'
curl -XPUT elasticsearch:9200/tesla -H'Content-Type: application/json' -d '{
  "mappings" : {
    "tesla" :{
      "properties" :{
        "timestamp" : {
          "type": "date"
        },
        "location" : {
          "type": "geo_point"
        },
        "soc" : {
          "type": "float"
        },
        "speed" : {
          "type": "float"
        }
      }
    }
  }
}'
