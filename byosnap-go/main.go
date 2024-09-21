package main

import (
	"log"
	"os"

	"github.com/snapser/gin-grpc/controller"
)

// @title			Postgame API
// @version		1.0
// @description	This is an example postgame server
func main() {
	log.Printf("Starting server")
	inventoryURL := os.Getenv("SNAPEND_INVENTORY_GRPC_URL")
	if inventoryURL == "" {
		log.Print("SNAPEND_INVENTORY_GRPC_URL not set")
	}
	statisticsUrl := os.Getenv("SNAPEND_STATISTICS_GRPC_URL")
	if statisticsUrl == "" {
		log.Printf("SNAPEND_STATISTICS_GRPC_URL not set")
	}
	log.Printf("Inventory URL: %s", inventoryURL)
	log.Printf("Statistics URL: %s", statisticsUrl)
	pgs, err := controller.New(inventoryURL, statisticsUrl)
	if err != nil {
		log.Fatal(err)
		panic(err)
	}
	router := pgs.NewRouter()

	err = router.Run(":8080")
	if err != nil {
		log.Fatal(err)
		panic(err)
	}
	log.Printf("Server started")
}
