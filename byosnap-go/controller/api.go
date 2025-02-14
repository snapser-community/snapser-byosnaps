package controller

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	inventorypb "github.com/snapser/gin-grpc/snapserpb/inventory"
	statspb "github.com/snapser/gin-grpc/snapserpb/statistics"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
)

// Win godoc
// @Summary		Win a game
// @Description	Increment win count for a user and grant reward
// @Id Win
// @Router /v1/byosnap-postgame/user/{user_id}/win [post]
// @Produce  json
// @Param user_id path string true "User ID" Format(uuid)
// @Param Token header string true "Authorization Token" Format(uuid)
// @Success 200
// @Failure 403
// @Failure 500
func (ps *PostgameServer) Win(c *gin.Context) {
	if err := validateAuthorization(c); err != nil {
		c.JSON(http.StatusForbidden, err.Error())
	}

	// This header is part of our existing authentication scheme to authenticate internal requests but
	// will be deprecated in the future. However adding it is necessary to be backwards compatible with all snaps
	// that are currently deployed.
	ctx := metadata.AppendToOutgoingContext(c.Request.Context(), "gateway", "internal")

	// The statistics admin tools has 2 stats created "wins" and "losses" that are counters and are marked as scope internal
	// The internal scope makes it so that it can only be incremented by internal services and not by users directly.
	_, err := ps.StatisticsClient.IncrementUserStatistic(ctx, &statspb.IncrementUserStatisticRequest{
		UserId: c.Param("user_id"),
		Key:    "wins",
		Delta:  1,
	})
	if err != nil {
		st, ok := status.FromError(err)
		if !ok {
			c.JSON(http.StatusInternalServerError, err.Error())
			return
		}
		c.JSON(http.StatusInternalServerError, fmt.Sprintf("%s: %d", err.Error(), st.Code()))
		return
	}

	// The inventory admin tools have a virtual currency called coins that can be granted to users.
	_, err = ps.InventoryClient.IncrementUserCurrency(ctx, &inventorypb.IncrementUserCurrencyRequest{
		UserId:       c.Param("user_id"),
		CurrencyName: "coins",
		Delta:        100,
	})
	if err != nil {
		st, ok := status.FromError(err)
		if !ok {
			c.JSON(http.StatusInternalServerError, err.Error())
			return
		}
		c.JSON(http.StatusInternalServerError, fmt.Sprintf("%s: %d", err.Error(), st.Code()))
		return
	}
	c.JSON(200, map[string]interface{}{})
}

// Lose godoc
// @Summary		Lose a game
// @Description	Increment lose count for a user
// @Id Lose
// @Router /v1/byosnap-postgame/user/{user_id}/lose [post]
// @Produce  json
// @Param user_id path string true "User ID" Format(uuid)
// @Param token header string true "Authorization Token" Format(uuid)
// @Success 200
// @Failure 500
func (ps *PostgameServer) Lose(c *gin.Context) {
	if err := validateAuthorization(c); err != nil {
		c.JSON(http.StatusForbidden, err.Error())
	}

	ctx := metadata.AppendToOutgoingContext(c.Request.Context(), "gateway", "internal")
	_, err := ps.StatisticsClient.IncrementUserStatistic(ctx, &statspb.IncrementUserStatisticRequest{
		UserId: c.Param("user_id"),
		Key:    "losses",
		Delta:  1,
	})
	if err != nil {
		st, ok := status.FromError(err)
		if !ok {
			c.JSON(http.StatusInternalServerError, err.Error())
			return
		}
		c.JSON(http.StatusInternalServerError, fmt.Sprintf("%s: %d", err.Error(), st.Code()))
		return
	}
	c.JSON(200, map[string]interface{}{})
}

func validateAuthorization(c *gin.Context) error {
	// Check the source of the call
	gateway := c.Request.Header.Get("Gateway")
	// "internal" gateway means the call came from another snap within your snapend and is authorized
	if gateway == "internal" {
		return nil
	}

	// Check the type of authentication
	authType := c.Request.Header.Get("Auth-Type")
	// "api-key" and "app" are set by the gateway when the request is using API Key or App Key authentication respectively
	if authType == "api-key" || authType == "app" {
		return nil
	}

	// If neither of the above it's a user auth call, check whether it is the same user
	authedUserID := c.Request.Header.Get("User-Id")
	// The user-id header is set by our gateway after authenticating the token in the request.
	// This check confirms that a win can only be posted by a user for themselves and not for any other user.
	requestedUserID := c.Param("user_id")
	if authedUserID == requestedUserID {
		return nil
	}

	return fmt.Errorf("authorization failure")
}
