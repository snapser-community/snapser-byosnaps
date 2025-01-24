package main

import (
	"fmt"
	"io"
	"net/http"

	"math/rand"

	"github.com/gin-gonic/gin"
	"github.com/rs/zerolog"
	eventbuspb "github.com/snapser-community/snapser-byosnaps/byosnap-rewards/snapserpb/eventbus"
	lobbiespb "github.com/snapser-community/snapser-byosnaps/byosnap-rewards/snapserpb/lobbies"
	"google.golang.org/grpc/metadata"
	"google.golang.org/protobuf/proto"
)

func (a *app) eventHandler(c *gin.Context) {
	ctx := c.Request.Context()
	log := zerolog.Ctx(c.Request.Context())

	body, err := io.ReadAll(c.Request.Body)
	if err != nil {
		panic(err)
	}

	// Parse body as eventbus.WebhookMessage
	var wr eventbuspb.ByoWebhookRequest
	err = proto.Unmarshal(body, &wr)
	if err != nil {
		// Log the body
		fmt.Printf("Body: %s\n", body)
		panic(err)
	}

	// Switch on the message type
	switch wr.MessageType {
	case eventbuspb.MessageType_MESSAGE_TYPE_SNAP_EVENT:
		snapEvent := wr.GetByoSnapEvent()

		// Switch on the service_name to know which enum to use for the event-type -> message-type
		switch snapEvent.ServiceName {
		case byoSnapID:
			log.Info().Msgf("Received %s event: %v", byoSnapID, snapEvent)

		case "lobbies":
			switch snapEvent.EventId {
			case uint32(lobbiespb.LobbiesEventType_LOBBIES_MEMBER_JOINED):
				ev := &lobbiespb.EventLobbiesMemberJoined{}
				if err := proto.Unmarshal([]byte(snapEvent.Payload), ev); err != nil {
					panic(err)
				}
				log.Info().Msgf("got EventLobbiesMemberJoined: %v", ev)

				// Some praise messages
				var fallbackPraises = []string{
					"You're doing amazing work!",
					"Keep up the fantastic effort!",
					"Your dedication is inspiring!",
					"You're a star, keep shining!",
					"You have the power to achieve great things!",
					"Believe in yourself, you're unstoppable!",
				}

				randomPraise := fallbackPraises[rand.Intn(len(fallbackPraises))]

				praiseReq := &eventbuspb.PublishByoEventRequest{
					ByosnapId:  byoSnapID,
					Subject:    "praise",
					Payload:    []byte(fmt.Sprintf("Nice work, you joined a lobby - %s", randomPraise)),
					Recipients: []string{ev.JoinedUserId},
				}
				ctx = metadata.NewOutgoingContext(ctx, metadata.Pairs("gateway", "internal"))
				_, err := a.eventbusClient.PublishByoEvent(ctx, praiseReq)
				if err != nil {
					log.Error().Err(err).Msg("failed to publish event")
				} else {
					log.Info().Msgf("published praise event: %v", praiseReq)
				}
			default:
				log.Info().Msgf("unhandled lobbies event_id: %v", snapEvent.EventId)
			}
		}
	default:
		log.Printf("unhandled message type: %v", wr.MessageType)
	}

	c.Writer.WriteHeader(http.StatusOK)
	c.Writer.Write([]byte("ok"))
}
