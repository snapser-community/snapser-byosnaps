package main

import (
	"context"
	"os"
	"strings"

	"github.com/gin-contrib/cors"
	"github.com/gin-contrib/logger"
	"github.com/gin-gonic/gin"
	"github.com/rs/zerolog"
	eventbuspb "github.com/snapser-community/snapser-byosnaps/byosnap-go/snapserpb/eventbus"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"
)

var byoSnapID = "byosnap-go"

type app struct {
	eventbusClient eventbuspb.EventbusServiceClient
}

func main() {
	ctx := context.Background()

	// Setup a log and tie it to the default context
	log := zerolog.New(os.Stdout).With().Caller().Logger()
	ctx = log.WithContext(ctx)
	zerolog.DefaultContextLogger = &log
	log.Info().Msg("starting")

	// A. Registering our own event "praise" with the Eventbus. This is so that our BYOSnap can
	// emit custom events that our game clients or other BYOSnaps can listen for
	//
	// 👇 This is where we create a gRPC connection with the Eventbus and register our custom event
	eventbusUrl := os.Getenv("SNAPEND_EVENTBUS_GRPC_URL")
	if eventbusUrl == "" {
		log.Fatal().Msg("SNAPEND_EVENTBUS_GRPC_URL not set")
	}
	log.Info().Msgf("eventbus url: %s", eventbusUrl)

	eventbusUrl = strings.TrimPrefix(eventbusUrl, "http://")

	// Use grpc to call the eventbus service, RegisterEventTypes
	conn, err := grpc.NewClient(eventbusUrl, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Error().Err(err).Msg("failed to create grpc client")
	}
	defer conn.Close()
	eventbusClient := eventbuspb.NewEventbusServiceClient(conn)

	app := &app{
		eventbusClient: eventbusClient,
	}

	// 👇 This is our custom event that we are registering
	req := &eventbuspb.RegisterByoEventTypesRequest{
		ByosnapId:  byoSnapID,
		EventTypes: eventTypes,
	}
	md := metadata.Pairs("gateway", "internal")
	ctx = metadata.NewOutgoingContext(ctx, md)
	_, err = eventbusClient.RegisterByoEventTypes(ctx, req)
	if err != nil {
		log.Fatal().Msgf("failed to register event types: %v", err)
	}
	log.Info().Msg("registered event types")

	// B. We also want to listen for events from the Eventbus. Eventbus does this by sending
	// a webhook to our BYOSnap on the reserved URL "POST /internal/events".
	//
	var router = gin.Default()
	router.Use(logger.SetLogger())
	router.Use(cors.New(cors.Config{
		AllowAllOrigins: true,
		AllowMethods:    []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:    []string{"Origin", "Authorization", "Content-Type", "User-Id", "Token", "App-Key"},
	}))
	router.GET("/healthz", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok"})
	})
	// 👇 This code is registering the webhook callback URL with the server
	// any calls that come in call the eventHandler function for further processing
	// IMPORTANT: Notice there is no BYOSnap prefix or byosnap ID in the URL.
	router.POST("/internal/events", app.eventHandler)

	if err = router.Run(":8080"); err != nil {
		log.Fatal().Err(err).Msg("failed to start server")
	}
}
