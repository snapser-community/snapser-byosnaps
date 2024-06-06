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
// @Param token header string true "Authorization Token" Format(uuid)
// @Success 200
// @Failure 403
// @Failure 500
func (ps *PostgameServer) Win(c *gin.Context) {
	// The user-id header is set by our gateway after authenticating the token in the request.
	// This check confirms that a win can only be posted by a user for themselves and not for any other user.
	authedUserID := c.Request.Header.Get("User-Id")
	requestedUserID := c.Param("user_id")
	if authedUserID != requestedUserID {
		c.JSON(http.StatusForbidden, "Unable to set another user's win")
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
	_, err = ps.InventoryClient.UpdateUserVirtualCurrency(ctx, &inventorypb.UpdateUserVirtualCurrencyRequest{
		UserId:       c.Param("user_id"),
		CurrencyName: "coins",
		Amount:       100,
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
	authedUserID := c.Request.Header.Get("User-Id")
	requestedUserID := c.Param("user_id")
	if authedUserID != requestedUserID {
		c.JSON(http.StatusForbidden, "Unable to set another user's loss")
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
