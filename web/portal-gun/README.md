# Portal Gun
**Category:** web

**Author:** _Rok0'sBasilisk_

## Description

Don't look at another man's portal gun history. We all go to weird places.

## Solution
<details>
 <summary>Reveal Spoiler</summary>

This challenges exposes a web interface with a simple API. Based on the files provided it is observed that this application utilizes a microservice architecture (although an extrmely simple one). There are two services, one written in Python and another one developed in Golang. 

Part of this challenge is based on https://bishopfox.com/blog/json-interoperability-vulnerabilities . In this instance, there is a discrepancy in the way that the JSON request body is parsed. In case of duplicate keys, the Golang service (which performs) the validation takes into account only the first key where as the Python service takes only the second one. By exploiting this vulnerability, participants can bypass validation to smuggle payloads that exploit NoSQL injection.

Using NoSQL injection participants can get the flag from the database using the following request:

```
curl -X POST http://<HOST>:8082/portal -d '{"filter": {"name":"Whatever..."}, "find": "flag", "filter": {"$where": "throw JSON.stringify(this)"}}'
```

To clarify, mongo comes with an embedded javascript engine which allows for expressions in some operators. One of them is the `$where` operator.

</details>