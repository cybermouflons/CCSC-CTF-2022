package main

import (
	"bytes"
	"io"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/buger/jsonparser"
)

func validatePortalReuqest(w http.ResponseWriter, r *http.Request) {
	data, _ := ioutil.ReadAll(r.Body)
	_, err := jsonparser.GetString(data, "filter", "name")
	if err != nil {
		w.WriteHeader(500)
		io.WriteString(w, "{\"error\": \"Request body must be of format '{\\\"filter\\\": {\\\"name\\\": \\\"<location name>\\\"}}'\"}")
		return
	}

	request, _ := http.NewRequest("POST", "http://portalsvc:5000/portal", bytes.NewBuffer(data))
	request.Header.Set("Content-Type", "application/json; charset=UTF-8")

	client := &http.Client{}
	response, error := client.Do(request)
	if error != nil {
		panic(error)
	}
	defer response.Body.Close()

	body, _ := ioutil.ReadAll(response.Body)
	io.WriteString(w, string(body))
}

func validateLocationsRequest(w http.ResponseWriter, r *http.Request) {
	request, _ := http.NewRequest("GET", "http://portalsvc:5000/locations", nil)

	client := &http.Client{}
	response, error := client.Do(request)
	if error != nil {
		panic(error)
	}
	defer response.Body.Close()

	body, _ := ioutil.ReadAll(response.Body)
	io.WriteString(w, string(body))
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "templates/index.html")
}

func main() {
	mux := http.NewServeMux()

	mux.HandleFunc("/", rootHandler)
	mux.Handle("/assets/", http.StripPrefix("/assets/", http.FileServer(http.Dir("assets"))))

	mux.HandleFunc("/portal", validatePortalReuqest)
	mux.HandleFunc("/locations", validateLocationsRequest)

	err := http.ListenAndServe(":3000", mux)
	log.Fatal(err)
}
