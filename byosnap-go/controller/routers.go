package controller

import (
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	_ "github.com/snapser/gin-grpc/docs"
	inventorypb "github.com/snapser/gin-grpc/snapserpb/inventory"
	statspb "github.com/snapser/gin-grpc/snapserpb/statistics"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type Route struct {
	Name        string
	Method      string
	Pattern     string
	HandlerFunc http.HandlerFunc
}

type PostgameServer struct {
	InventoryClient  inventorypb.InventoryServiceClient
	StatisticsClient statspb.StatisticsServiceClient
}

func New(inventoryURL string, statisticsURL string) (*PostgameServer, error) {
	pgs := &PostgameServer{}
	inventoryClient, err := createInventoryClient(inventoryURL)
	if err != nil {
		return nil, err
	}
	pgs.InventoryClient = inventoryClient
	statisticsClient, err := createStatisticsClient(statisticsURL)
	if err != nil {
		return nil, err
	}
	pgs.StatisticsClient = statisticsClient
	return pgs, nil
}

type Routes []Route

func (pgs *PostgameServer) NewRouter() *gin.Engine {
	var router = gin.Default()
	router.Use(cors.New(cors.Config{
		AllowAllOrigins: true,
		AllowMethods:    []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:    []string{"Origin", "Authorization", "Content-Type", "User-Id", "Token", "App-Key"},
	}))
	router.GET("/healthz", pgs.Healthz)
	router.POST("/internal/events", pgs.Events)

	v1 := router.Group("/v1/byosnap-postgame")
	v1.POST("/user/:user_id/win", pgs.Win)
	v1.POST("/user/:user_id/lose", pgs.Lose)

	return router
}

func (pgs *PostgameServer) Healthz(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"status": "ok"})
}

// We use GRPC internally to provide fast requests between services.  Users are authenticated at our API Gateway and then trusted once internal;
// The API Gateway will add/override a header called "User-Id" that is the authenticated trusted user and can be relied on internally.
func createInventoryClient(inventoryURL string) (inventorypb.InventoryServiceClient, error) {
	if inventoryURL == "" {
		return nil, nil
	}
	conn, err := grpc.Dial(inventoryURL, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, err
	}
	client := inventorypb.NewInventoryServiceClient(conn)
	return client, nil
}

func createStatisticsClient(statisticsURL string) (statspb.StatisticsServiceClient, error) {
	if statisticsURL == "" {
		return nil, nil
	}
	conn, err := grpc.Dial(statisticsURL, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, err
	}
	client := statspb.NewStatisticsServiceClient(conn)
	return client, nil
}
