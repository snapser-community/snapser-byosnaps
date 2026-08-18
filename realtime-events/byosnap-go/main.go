package main

import (
	"context"
	"log/slog"
	"os"
	"strings"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	eventbuspb "github.com/snapser-community/snapser-byosnaps/byosnap-go/snapserpb/eventbus"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

var byoSnapID = "byosnap-go"

type app struct {
	eventbusClient eventbuspb.EventbusServiceClient
}

func main() {
	ctx := context.Background()

	// Snapser parses one JSON object per log line: `level` colors the line in the
	// Logs tool, `request-id` correlates the lines of a request across Snaps.
	// See logging.go.
	logger.Info("starting")

	// A. Registering our own event "praise" with the Eventbus. This is so that our BYOSnap can
	// emit custom events that our game clients or other BYOSnaps can listen for
	//
	// 👇 This is where we create a gRPC connection with the Eventbus and register our custom event
	eventbusUrl := os.Getenv("SNAPEND_EVENTBUS_GRPC_URL")
	if eventbusUrl == "" {
		logger.Error("SNAPEND_EVENTBUS_GRPC_URL not set")
		os.Exit(1)
	}
	logger.Info("eventbus url", slog.String("url", eventbusUrl))

	eventbusUrl = strings.TrimPrefix(eventbusUrl, "http://")

	// Use grpc to call the eventbus service, RegisterEventTypes
	conn, err := grpc.NewClient(eventbusUrl, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		logger.Error("failed to create grpc client", slog.Any("error", err))
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
	// Registration runs at boot, outside any request, so outgoingInternalContext
	// adds no x-request-id metadata here.
	_, err = eventbusClient.RegisterByoEventTypes(outgoingInternalContext(ctx), req)
	if err != nil {
		logger.Error("failed to register event types", slog.Any("error", err))
		os.Exit(1)
	}
	logger.Info("registered event types")

	// B. We also want to listen for events from the Eventbus. Eventbus does this by sending
	// a webhook to our BYOSnap on the reserved URL "POST /internal/events".
	//
	// gin.New() instead of gin.Default(): gin's built-in logger writes plain text
	// lines, which Snapser cannot parse.
	var router = gin.New()
	router.Use(gin.Recovery())
	// 👇 Binds the inbound X-Request-Id to a request scoped logger. Handlers call
	// requestLogger(c.Request) so every line carries the request-id.
	router.Use(requestLogging)
	router.Use(cors.New(cors.Config{
		AllowAllOrigins: true,
		AllowMethods:    []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:    []string{"Origin", "Authorization", "Content-Type", "User-Id", "Token", "App-Key", RequestIDHeaderKey},
	}))
	router.GET("/healthz", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok"})
	})
	// 👇 This code is registering the webhook callback URL with the server
	// any calls that come in call the eventHandler function for further processing
	// IMPORTANT: Notice there is no BYOSnap prefix or byosnap ID in the URL.
	router.POST("/internal/events", app.eventHandler)

	if err = router.Run(":8080"); err != nil {
		logger.Error("failed to start server", slog.Any("error", err))
		os.Exit(1)
	}
}
