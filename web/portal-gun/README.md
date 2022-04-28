# Portal Gun
**Category:** web

**Author:** _Rok0'sBasilisk_

## Description

In response to the Central Finite Curve, evil Morty is forming the Supersingular Finite Curve. This is a portion of the multiverse, where Mortys dominate over Ricks. Not sure if Morty's smart enough to complete this.. his maths may be out of order...

## Solution
<details>
 <summary>Reveal Spoiler</summary>

This challenges exposes a web interface with a simple API. Based on the files provided it is observed that this application utilizes a microservice architecture (although an extrmely simple one). There are two services, one written in Python and another one developed in Golang. 

Part of this challenge is based on https://bishopfox.com/blog/json-interoperability-vulnerabilities . In this instance, there is a discrepancy in the way that the JSON request body is parsed. In case of duplicate keys, the Golang service (which performs) the validation takes into account only the first key where as the Python service takes only the second one. By exploiting this vulnerability, participants can bypass validation to smuggle payloads that exploit NoSQL injection.

Using NoSQL injection participants can get the flag from the database using the following request:

```
curl -X POST http://<HOST>:8082/portal -d '{"filter": {"name":"Citadel of Ricks"}, "find": "flag", "filter": {"$where": "throw JSON.stringify(this)"}}'
```

</details>