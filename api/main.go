package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gorilla/mux"
	"github.com/rs/cors"
)

type Settings struct {
	BrewTemp  float64 `json:"brew_target_temp"`
	SteamTemp float64 `json:"steam_target_temp"`
	P         float64 `json:"p"`
	I         float64 `json:"i"`
	D         float64 `json:"d"`
	CycleTime float64 `json:"cycle_seconds"`
}

func homePage(w http.ResponseWriter, r *http.Request) {
	jsonFile, err := os.Open(string(filepath.Separator) + "config" + string(filepath.Separator) + "pid.config.json")

	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("<h1>Welcome to the RasberryPID</h1>")
	fmt.Println("<h2>Here are the currently configured settings for the PID controller</h2>")

	//defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)

	var settings Settings
	json.Unmarshal([]byte(byteValue), &settings)

	fmt.Printf("<ul><li>Brew Temp: 	<strong>%f</strong></li>", settings.BrewTemp)
	fmt.Printf("<li>Steam Temp: 	<strong>%f</strong></li>", settings.SteamTemp)
	fmt.Printf("<li>P Temp: 		<strong>%f</strong></li>", settings.P)
	fmt.Printf("<li>I Temp: 		<strong>%f</strong></li>", settings.I)
	fmt.Printf("<li>D Temp: 		<strong>%f</strong></li>", settings.D)
	fmt.Printf("<li>Cycle Time: 	<strong>%f</strong></li></ul>", settings.CycleTime)

	jsonFile.Close()
}

func getSettings(w http.ResponseWriter, r *http.Request) {
	jsonFile, err := os.Open(string(filepath.Separator) + "config" + string(filepath.Separator) + "pid.config.json")

	if err != nil {
		fmt.Println(err)
		return
	}

	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)

	var settings Settings
	json.Unmarshal([]byte(byteValue), &settings)

	json.NewEncoder(w).Encode((settings))
}

func getTemps(w http.ResponseWriter, r *http.Request) {
	jsonFile, err := os.ReadFile(string(filepath.Separator) + "log" + string(filepath.Separator) + "temperature.json")

	if err != nil {
		fmt.Println(err)
		return
	}

	w.Write(jsonFile)
}

func postSettings(w http.ResponseWriter, r *http.Request) {
	reqBody, _ := ioutil.ReadAll(r.Body)

	var settings Settings
	json.Unmarshal(reqBody, &settings)

	file, _ := json.MarshalIndent(settings, "", "  ")

	_ = ioutil.WriteFile(string(filepath.Separator)+"config"+string(filepath.Separator)+"pid.config.json", file, 0644)
	json.NewEncoder(w).Encode((settings))
}

func handleRequests() {
	router := mux.NewRouter()

	router.HandleFunc("/", homePage)
	router.HandleFunc("/settings", getSettings).Methods("GET")
	router.HandleFunc("/tempgraph", getTemps).Methods("GET")
	router.HandleFunc("/settings", postSettings).Methods("POST")

	router.Use(cors.New(cors.Options{
		AllowedOrigins: []string{"*"},
		AllowedHeaders: []string{"*"},
		Debug:          true,
	}).Handler)
	log.Fatal(http.ListenAndServe(":9000", router))
}

func main() {
	fmt.Println("RasberryPID starting on port 9000")
	handleRequests()
}
